import html
import re

_REFERENCE_RE = re.compile(r"Ref:\s*(\d{1,3}):(\d{1,3})")


def extract_reference(text: str | None) -> tuple[int, int] | None:
    if not text:
        return None
    match = _REFERENCE_RE.search(text)
    if not match:
        return None
    return int(match.group(1)), int(match.group(2))


def format_selection_message(
    surah: int,
    ayah: int,
    expected_text: str,
) -> str:
    return (
        "📖 <b>Semakan Tahsin</b>\n\n"
        f"Ayat pilihan: <b>{surah}:{ayah}</b>\n"
        f"{html.escape(expected_text)}\n\n"
        "Balas <b>mesej ini</b> dengan voice note bacaan anda.\n"
        f"Ref: {surah}:{ayah}"
    )


def format_analysis(analysis: dict) -> str:
    """Present ASR word comparisons as uncertain evidence, not acoustic diagnoses.

    In particular, if ASR spells a mistaken 'kaf' even though the reciter said
    hamzah in place of 'ain, it must NOT be presented as an observed kaf sound.
    """
    errors = [
        item
        for item in analysis["word_alignment"]
        if item["status"] != "correct"
    ]
    is_ai_transcript = analysis.get("asr_mode") != "manual-transcript"

    lines = [
        f"📖 <b>Semakan Tahsin {analysis['surah']}:{analysis['ayah']}</b>",
        "",
    ]

    if is_ai_transcript:
        lines.extend([
            "🟡 <b>Semakan transkrip AI — keputusan sementara</b>",
            (
                "Padanan perkataan dalam transkrip: "
                f"<b>{analysis['accuracy_pct']}%</b>"
            ),
        ])
    else:
        lines.append(
            f"Padanan perkataan teks: <b>{analysis['accuracy_pct']}%</b>"
        )

    if not errors:
        lines.extend([
            "",
            (
                "✅ Semua perkataan sepadan dalam transkrip AI."
                if is_ai_transcript
                else "✅ Tiada perbezaan perkataan dalam teks."
            ),
        ])
    elif is_ai_transcript:
        lines.extend(["", "<b>Perkataan untuk semakan lanjut:</b>"])
        for index, item in enumerate(errors, start=1):
            status = item["status"]
            expected = html.escape(item.get("expected") or "—")
            heard = html.escape(item.get("heard") or "—")

            if status == "incorrect":
                lines.append(
                    f"{index}. 🔎 <b>{expected}</b> — ejaan dalam transkrip AI "
                    "berbeza daripada teks rujukan. Bunyi/huruf yang "
                    "sebenarnya tersalah <b>belum dapat dipastikan</b>."
                )
            elif status == "missed":
                lines.append(
                    f"{index}. 🔎 <b>{expected}</b> — tidak muncul dalam "
                    "transkrip AI; belum tentu ditinggalkan ketika membaca."
                )
            elif status == "extra":
                lines.append(
                    f"{index}. 🔎 <b>{heard}</b> — muncul sebagai tambahan "
                    "dalam transkrip AI; belum tentu disebut dalam rakaman."
                )
    else:
        lines.extend(["", "<b>Perbezaan dalam teks:</b>"])
        for index, item in enumerate(errors, start=1):
            status = item["status"]
            expected = html.escape(item.get("expected") or "—")
            heard = html.escape(item.get("heard") or "—")

            if status == "incorrect":
                lines.append(
                    f"{index}. ❌ Rujukan: <b>{expected}</b>; "
                    f"teks diberi: <b>{heard}</b>"
                )
            elif status == "missed":
                lines.append(f"{index}. ⛔ <b>{expected}</b> tiada dalam teks")
            elif status == "extra":
                lines.append(f"{index}. ➕ Tambahan dalam teks: <b>{heard}</b>")

    if is_ai_transcript:
        lines.extend([
            "",
            "<b>Transkrip mentah AI (mungkin tersalah dengar):</b>",
            html.escape(analysis.get("transcription") or "—"),
        ])

    lines.extend([
        "",
        "<b>Teks rujukan:</b>",
        html.escape(analysis["expected_text"]),
        "",
    ])

    if is_ai_transcript:
        lines.append(
            "ℹ️ Peratus di atas <b>bukan markah bacaan, tajwid atau makhraj</b>. "
            "Transkrip AI boleh tersilap mengeja bunyi (contoh: ع, ء, ك). "
            "Semakan makhraj/tajwid akustik yang disahkan guru belum tersedia."
        )
    else:
        lines.append(
            "ℹ️ Ini perbandingan teks sahaja, bukan semakan makhraj atau tajwid."
        )

    return "\n".join(lines)
