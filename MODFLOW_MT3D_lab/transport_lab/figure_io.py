"""Display multilingual Matplotlib text using the Picard–Newton Lab SVG approach."""
from base64 import b64encode
from functools import lru_cache
from io import BytesIO, StringIO
from pathlib import Path
from threading import RLock

import streamlit as st
import re
import xml.etree.ElementTree as ET

import matplotlib as mpl
from matplotlib import font_manager
from matplotlib.text import Text
from fontTools import subset
from fontTools.ttLib import TTFont

FONT_DIR = Path(__file__).resolve().parents[1] / "assets" / "fonts"
SCRIPT_FONTS = {
    "ar": "NotoSansArabic-Regular.ttf",
    "hi": "NotoSansDevanagari-Regular.ttf",
    "zh": "NotoSansCJKsc-Regular.otf",
    "bn": "NotoSansBengali-Regular.ttf",
}
SCRIPT_TEXT = re.compile(r"[\u0600-\u06ff\u0900-\u09ff\u3000-\u9fff\uff00-\uffef]")
ARABIC_TEXT = re.compile(r"[\u0600-\u06ff]")
SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")


# 1. Keep font registration/subsetting out of the repeated numerical work.
@lru_cache(maxsize=4)
def script_font(language):
    path = FONT_DIR / SCRIPT_FONTS[language]
    font_manager.fontManager.addfont(str(path))
    return str(path), font_manager.FontProperties(fname=path).get_name()


@lru_cache(maxsize=96)
def _font_face(path, family, characters):
    """Embed only glyphs needed by this figure, retaining shaping tables."""
    font = TTFont(path)
    options = subset.Options()
    options.layout_features = ["*"]
    options.recommended_glyphs = True
    options.drop_tables += ["FFTM"]  # Font timestamps have no display purpose.
    worker = subset.Subsetter(options=options)
    worker.populate(text=characters)
    worker.subset(font)
    stream = BytesIO()
    font.save(stream)
    font.close()
    encoded = b64encode(stream.getvalue()).decode("ascii")
    return (
        "@font-face{font-family:'"
        + family
        + "';src:url(data:font/otf;base64,"
        + encoded
        + ");}"
    )


# 2. Export text as complete runs, not disconnected character outlines.
def svg_figure(figure, language, **savefig_options):
    """Return a self-contained SVG; never modify data, limits or solver state."""
    if language not in SCRIPT_FONTS:
        raise ValueError("SVG script rendering requires ar, hi, zh or bn")
    path, family = script_font(language)
    for artist in figure.findobj(match=Text):
        if SCRIPT_TEXT.search(artist.get_text()):
            # Latin/math first: MathText uses its first family for plain units.
            # Script glyphs fall back to Noto, then shape as whole SVG text runs.
            artist.set_fontfamily(["DejaVu Sans", family])
    stream = StringIO()
    with mpl.rc_context({"svg.fonttype": "none"}):
        figure.savefig(stream, format="svg", **savefig_options)
    root = ET.fromstring(stream.getvalue())
    characters = "".join(sorted(set("".join(root.itertext()))))
    latin_path = font_manager.findfont(
        font_manager.FontProperties(family="DejaVu Sans")
    )
    styles = _font_face(path, family, characters) + _font_face(
        latin_path, "DejaVu Sans", characters
    )
    ET.SubElement(root, f"{{{SVG_NS}}}style").text = styles
    for node in root.iter(f"{{{SVG_NS}}}text"):
        if not len(node) and SCRIPT_TEXT.search(node.text or ""):
            # Use the script font for complete prose runs. In particular,
            # DejaVu's oblique Arabic glyphs can render as disconnected marks.
            # MathText spans keep their own fonts and Latin unit lettering.
            style = re.sub(
                r"font-family:[^;]+",
                f"font-family: '{family}', 'DejaVu Sans'",
                node.get("style", ""),
            )
            if language == "ar":
                style = re.sub(r"font-style:[^;]+", "font-style: normal", style)
            node.set("style", style)
        if ARABIC_TEXT.search("".join(node.itertext())):
            # SVG anchors depend on text direction. Preserve physical alignment.
            style = node.get("style", "")
            style = re.sub(
                r"text-anchor:\s*(start|end)",
                lambda m: "text-anchor: " + ("end" if m[1] == "start" else "start"),
                style,
            )
            if "text-anchor:" not in style:
                # Matplotlib positions multiline text from its left edge.
                style += ";text-anchor:end"
            node.set("style", style + ";direction:rtl;unicode-bidi:plaintext")
    return ET.tostring(root, encoding="unicode")


_RENDER_LOCK = RLock()


def show_figure(figure, language):
    """Serialize Matplotlib's process-wide font settings across Streamlit sessions."""
    with _RENDER_LOCK:
        if language in SCRIPT_FONTS:
            st.image(svg_figure(figure, language), width="stretch")
        else:
            st.pyplot(figure, width="stretch")
