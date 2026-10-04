import os
from typing import Any

import httpx


class SupabaseRecorder:
    def __init__(self, url: str, secret_key: str):
        self.url = url.rstrip("/")
        self.secret_key = secret_key
        self.headers = {
            "apikey": secret_key,
            "Authorization": f"Bearer {secret_key}",
            "Content-Type": "application/json",
        }

    async def _post(
        self,
        path: str,
        payload: Any,
        prefer: str = "return=representation",
    ) -> list[dict]:
        headers = {**self.headers, "Prefer": prefer}
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(
                f"{self.url}/rest/v1/{path}",
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            if not response.content:
                return []
            data = response.json()
            return data if isinstance(data, list) else [data]

    async def upsert_telegram_user(
        self,
        telegram_user_id: int,
        telegram_username: str | None = None,
        display_name: str | None = None,
    ) -> int:
        rows = await self._post(
            "tahsin_users?on_conflict=telegram_user_id&select=id",
            {
                "telegram_user_id": telegram_user_id,
                "telegram_username": telegram_username,
                "display_name": display_name,
            },
            prefer="resolution=merge-duplicates,return=representation",
        )
        return int(rows[0]["id"])

    async def save_analysis(
        self,
        analysis: dict,
        asr_model: str | None = None,
        telegram_user_id: int | None = None,
        telegram_username: str | None = None,
        display_name: str | None = None,
    ) -> str:
        user_id = None
        if telegram_user_id is not None:
            user_id = await self.upsert_telegram_user(
                telegram_user_id=telegram_user_id,
                telegram_username=telegram_username,
                display_name=display_name,
            )

        recitation_rows = await self._post(
            "recitations?select=id",
            {
                "user_id": user_id,
                "surah": analysis["surah"],
                "ayah": analysis["ayah"],
                "transcription": analysis["transcription"],
                "expected_text": analysis["expected_text"],
                "accuracy_pct": analysis["accuracy_pct"],
                "asr_model": asr_model,
                "analysis_version": "m1-word-level",
                "status": "completed",
            },
        )
        recitation_id = str(recitation_rows[0]["id"])

        words = [
            {
                "recitation_id": recitation_id,
                "position": index,
                "expected": item.get("expected"),
                "heard": item.get("heard"),
                "status": item["status"],
            }
            for index, item in enumerate(analysis["word_alignment"])
        ]
        if words:
            await self._post(
                "recitation_words",
                words,
                prefer="return=minimal",
            )

        return recitation_id


def get_supabase_recorder() -> SupabaseRecorder | None:
    url = os.getenv("SUPABASE_URL")
    secret_key = (
        os.getenv("SUPABASE_SECRET_KEY")
        or os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    )
    if not url or not secret_key:
        return None
    return SupabaseRecorder(url=url, secret_key=secret_key)


def persistence_configured() -> bool:
    return get_supabase_recorder() is not None
