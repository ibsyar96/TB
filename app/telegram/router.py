import hmac
import os
import tempfile
from pathlib import Path

import httpx
from fastapi import APIRouter, Header, HTTPException, Request

from app.asr.factory import ASRNotConfigured
from app.quran.data import get_ayah
from app.services.recitation import (
    AyahNotAvailable,
    EmptyTranscription,
    analyze_audio_path,
)
from app.telegram.client import TelegramAPIError, TelegramClient
from app.telegram.formatting import (
    extract_reference,
    format_analysis,
    format_selection_message,
)

router = APIRouter(tags=["telegram"])


def _get_client() -> TelegramClient:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise HTTPException(
            status_code=503,
            detail="TELEGRAM_BOT_TOKEN is not configured",
        )
    return TelegramClient(token=token)


def _verify_webhook_secret(received: str | None) -> None:
    expected = os.getenv("TELEGRAM_WEBHOOK_SECRET")
    if not expected:
        return
    if not received or not hmac.compare_digest(received, expected):
        raise HTTPException(status_code=403, detail="Invalid Telegram webhook secret")


def _parse_tahsin_command(text: str) -> tuple[int, int] | None:
    parts = text.strip().split()
    if not parts or not parts[0].split("@")[0] == "/tahsin":
        return None
    if len(parts) != 3:
        return None
    try:
        return int(parts[1]), int(parts[2])
    except ValueError:
        return None


def _display_name(user: dict) -> str | None:
    parts = [
        user.get("first_name"),
        user.get("last_name"),
    ]
    name = " ".join(part for part in parts if part)
    return name or None


@router.post("/telegram/webhook")
async def telegram_webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str | None = Header(default=None),
):
    _verify_webhook_secret(x_telegram_bot_api_secret_token)
    update = await request.json()

    message = update.get("message")
    if not message:
        return {"ok": True}

    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    if chat_id is None:
        return {"ok": True}

    client = _get_client()
    text = (message.get("text") or "").strip()

    if text.startswith("/start"):
        await client.send_message(
            chat_id,
            "Assalamualaikum. Saya <b>Tahsin Bot</b>.\n\n"
            "Untuk MVP, pilih ayat dengan arahan seperti:\n"
            "<code>/tahsin 1 2</code>\n\n"
            "Kemudian balas mesej ayat yang bot hantar dengan voice note bacaan anda.",
        )
        return {"ok": True}

    if text.startswith("/tahsin"):
        reference = _parse_tahsin_command(text)
        if reference is None:
            await client.send_message(
                chat_id,
                "Format arahan: <code>/tahsin SURAH AYAT</code>\n"
                "Contoh: <code>/tahsin 1 2</code>",
            )
            return {"ok": True}

        surah, ayah = reference
        expected = get_ayah(surah, ayah)
        if not expected:
            await client.send_message(
                chat_id,
                "Ayat itu belum tersedia dalam MVP. "
                "Sekarang kita sedang menguji Surah Al-Fatihah.",
            )
            return {"ok": True}

        await client.send_message(
            chat_id,
            format_selection_message(surah, ayah, expected),
        )
        return {"ok": True}

    voice = message.get("voice")
    if voice:
        reply_text = (
            (message.get("reply_to_message") or {}).get("text")
            or (message.get("reply_to_message") or {}).get("caption")
        )
        reference = extract_reference(reply_text)
        if reference is None:
            await client.send_message(
                chat_id,
                "Saya perlukan rujukan ayat. Gunakan "
                "<code>/tahsin 1 2</code>, kemudian <b>reply</b> "
                "mesej ayat itu dengan voice note.",
                reply_to_message_id=message.get("message_id"),
            )
            return {"ok": True}

        max_bytes = int(
            os.getenv("TELEGRAM_MAX_VOICE_BYTES", "4000000")
        )
        declared_size = int(voice.get("file_size") or 0)
        if declared_size and declared_size > max_bytes:
            await client.send_message(
                chat_id,
                "Voice note terlalu besar untuk MVP. "
                "Cuba baca satu ayat atau potongan pendek dahulu.",
            )
            return {"ok": True}

        await client.send_chat_action(chat_id, "typing")

        try:
            audio_bytes = await client.download_file(voice["file_id"])
        except (TelegramAPIError, httpx.HTTPError):
            await client.send_message(
                chat_id,
                "Saya tak berjaya memuat turun voice note itu. Cuba hantar semula.",
            )
            return {"ok": True}

        if len(audio_bytes) > max_bytes:
            await client.send_message(
                chat_id,
                "Voice note terlalu besar untuk MVP. "
                "Cuba bacaan yang lebih pendek.",
            )
            return {"ok": True}

        surah, ayah = reference
        suffix = ".ogg"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
            temp.write(audio_bytes)
            temp_path = Path(temp.name)

        user = message.get("from") or {}
        try:
            analysis = await analyze_audio_path(
                temp_path,
                surah=surah,
                ayah=ayah,
                telegram_user_id=user.get("id"),
                telegram_username=user.get("username"),
                display_name=_display_name(user),
                persist=True,
            )
        except AyahNotAvailable:
            await client.send_message(
                chat_id,
                "Ayat itu belum tersedia dalam MVP.",
            )
            return {"ok": True}
        except ASRNotConfigured:
            await client.send_message(
                chat_id,
                "Enjin suara belum dikonfigurasi pada server.",
            )
            return {"ok": True}
        except EmptyTranscription:
            await client.send_message(
                chat_id,
                "Saya tak dapat mengenal pasti bacaan daripada audio itu. "
                "Cuba rakam semula dengan suara yang lebih jelas.",
            )
            return {"ok": True}
        except httpx.HTTPError:
            await client.send_message(
                chat_id,
                "Enjin semakan suara sedang gagal dihubungi. Cuba lagi.",
            )
            return {"ok": True}
        finally:
            temp_path.unlink(missing_ok=True)

        await client.send_message(
            chat_id,
            format_analysis(analysis),
            reply_to_message_id=message.get("message_id"),
        )
        return {"ok": True}

    return {"ok": True}
