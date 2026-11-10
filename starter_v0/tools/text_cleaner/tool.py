from __future__ import annotations

import html
import re
from typing import Any


def clean_text(text: str) -> dict[str, Any]:
    if not isinstance(text, str) or not text.strip():
        return {
            "tool": "text_cleaner",
            "error": "invalid_input",
            "message": "text must be a non-empty string",
        }

    cleaned = re.sub(
        r"<(script|style)\b[^>]*>.*?</\1>",
        " ",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    cleaned = re.sub(r"<[^>]+>", " ", cleaned)
    cleaned = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", cleaned)
    cleaned = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cleaned)
    cleaned = re.sub(r"^#{1,6}\s+", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"[*_~`>]+", "", cleaned)
    cleaned = html.unescape(cleaned)
    cleaned = re.sub(r"[ \t]+", " ", cleaned)
    cleaned = re.sub(r" *\n *", "\n", cleaned)
    cleaned = re.sub(r" +([.,!?;:])", r"\1", cleaned)
    cleaned = re.sub(r"\n\s*\n+", "\n\n", cleaned).strip()

    return {"tool": "text_cleaner", "text": cleaned}
