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
    errors = [
        item
        for item in analysis["word_alignment"]
        if item["status"] != "correct"
    ]

    lines = [
        f"📖 <b>Semakan Tahsin {analysis['surah']}:{analysis['ayah']}</b>",
        "",
        f"Ketepatan perkataan: <b>{analysis['accuracy_pct']}%</b>",
    ]

    if not errors:
        lines.extend([
            "",
            "✅ Tiada kesalahan perkataan dikesan.",
        ])
    else:
        lines.extend(["", "<b>Perkara yang dikesan:</b>"])
        for index, item in enumerate(errors, start=1):
            status = item["status"]
            expected = html.escape(item.get("expected") or "—")
            heard = html.escape(item.get("heard") or "—")

            if status == "incorrect":
                lines.append(
                    f"{index}. ❌ Sepatutnya <b>{expected}</b>; "
                    f"dikesan <b>{heard}</b>"
                )
            elif status == "missed":
                lines.append(
                    f"{index}. ⛔ <b>{expected}</b> tertinggal"
                )
            elif status == "extra":
                lines.append(
                    f"{index}. ➕ Bacaan tambahan: <b>{heard}</b>"
                )

    lines.extend([
        "",
        "<b>Teks rujukan:</b>",
        html.escape(analysis["expected_text"]),
        "",
        "ℹ️ Versi ini masih menilai kesalahan pada tahap perkataan. "
        "Semakan makhraj dan tajwid akustik akan ditambah selepas fasa ini stabil.",
    ])

    return "\n".join(lines)
