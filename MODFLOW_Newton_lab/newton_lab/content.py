"""Editable Markdown resources with per-document and per-key language fallback.

Derived from the MODFLOW Solver Lab content convention (## stable_key).
Add assets/md/de, for example; translated keys override English independently.
"""

import re
from pathlib import Path

DEFAULT_LANGUAGE = "en"
MD_DIRECTORY = Path(__file__).parent / "assets" / "md"
SECTION_HEADER = re.compile(r"^## ([a-z][a-z0-9_]*)[ \t]*$", re.MULTILINE)


class ContentError(ValueError):
    """Missing or inconsistent text resources."""


def load_md(filename, language=DEFAULT_LANGUAGE):
    if Path(filename).name != filename or not filename.endswith(".md"):
        raise ContentError("Expected a Markdown resource filename.")
    if not re.fullmatch(r"[a-z]{2,3}(?:-[A-Z]{2})?", language):
        raise ContentError("Invalid language code.")
    path = MD_DIRECTORY / language / filename
    if not path.exists():
        path = MD_DIRECTORY / DEFAULT_LANGUAGE / filename
    return path.read_text(encoding="utf-8")


def _sections(markdown):
    headers = list(SECTION_HEADER.finditer(markdown))
    result = {}
    for index, header in enumerate(headers):
        key = header.group(1)
        end = headers[index + 1].start() if index + 1 < len(headers) else len(markdown)
        value = markdown[header.end() : end].strip()
        if key in result or not value:
            raise ContentError(f"Duplicate or empty Markdown key: {key}")
        result[key] = value
    return result


def load_text(language=DEFAULT_LANGUAGE):
    result = _sections(load_md("ui.md"))
    if language != DEFAULT_LANGUAGE:
        result.update(_sections(load_md("ui.md", language)))
    return result


def available_languages():
    return sorted(
        p.name
        for p in MD_DIRECTORY.iterdir()
        if p.is_dir() and re.fullmatch(r"[a-z]{2,3}(?:-[A-Z]{2})?", p.name)
    )
