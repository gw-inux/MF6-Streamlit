"""Editable Markdown documents and keyed interface strings with English fallback."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1] / "assets" / "md"
LANGUAGES = {
    "en": "🇬🇧 English",
    "de": "🇩🇪 Deutsch",
    "fr": "🇫🇷 Français",
    "es": "🇪🇸 Español",
    "it": "🇮🇹 Italiano",
    "hi": "🇮🇳 हिन्दी",
    "ar": "🌐 العربية",
    "zh": "🇨🇳 简体中文",
    "pt": "🇵🇹 Português",
    "bn": "🇧🇩 বাংলা (Bengali)",
}
HEADER = re.compile(r"^## ([a-z][a-z0-9_]*)[ \t]*$", re.MULTILINE)


def _sections(text):
    matches = list(HEADER.finditer(text))
    result = {}
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        key = match.group(1)
        if key in result:
            raise ValueError(f"Duplicate Markdown key: {key}")
        value = text[match.end():end].strip()
        if value:
            result[key] = value
    return result


def load_text(language, root=ROOT):
    """A missing translation of a file or individual section inherits English."""
    base = {}
    for filename in ("interface.md", "learning.md"):
        base.update(_sections((root / "en" / filename).read_text(encoding="utf-8")))
        if language in LANGUAGES and language != "en":
            path = root / language / filename
            if path.is_file():
                base.update(_sections(path.read_text(encoding="utf-8")))
    return base
