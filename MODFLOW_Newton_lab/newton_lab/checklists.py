"""Render authored Markdown task lists without changing any model settings.

Stable task IDs stay in invisible Markdown comments during translation. Check
marks belong to the browser session and survive ordinary model-input reruns.
"""

import re
from dataclasses import dataclass

import streamlit as st

from .content import DEFAULT_LANGUAGE, ContentError, load_text

TASK_LINE = re.compile(
    r"^- \[([ xX])\] (.+?)\s+<!--\s*task:\s*([a-z][a-z0-9_]*)\s*-->\s*$"
)
FENCE_LINE = re.compile(r"^\s*(`{3,}|~{3,})")
PROGRESS_KEY = "learning_checklists"


@dataclass(frozen=True)
class ChecklistTask:
    """A translatable label and an identity independent of its wording."""

    identifier: str
    label: str
    initial: bool = False


def parse_checklist(markdown):
    """Split Markdown into prose and explicitly identified task rows.

    Ordinary paragraphs, tables, equations and fenced examples remain intact.
    Duplicate/missing IDs fail clearly instead of sharing a checkbox by mistake.
    """
    blocks, prose, seen = [], [], set()
    fence = None
    for line in markdown.splitlines(keepends=True):
        fence_match = FENCE_LINE.match(line)
        if fence_match:
            marker = fence_match.group(1)
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            prose.append(line)
            continue
        task = TASK_LINE.fullmatch(line.rstrip("\r\n")) if fence is None else None
        if task:
            mark, label, identifier = task.groups()
            if identifier in seen:
                raise ContentError(f"Repeated checklist task ID: {identifier}.")
            seen.add(identifier)
            if prose:
                blocks.append("".join(prose))
                prose = []
            blocks.append(ChecklistTask(identifier, label, mark.lower() == "x"))
        else:
            if fence is None and re.match(r"^- \[[ xX]\]", line):
                raise ContentError(
                    "Each checklist row needs a unique <!-- task: identifier --> comment."
                )
            prose.append(line)
    if prose:
        blocks.append("".join(prose))
    return blocks


def remember_check(namespace, identifier, widget_key):
    """Copy widget state to durable learning state; never touch model state."""
    progress = st.session_state.setdefault(PROGRESS_KEY, {})
    progress.setdefault(namespace, {})[identifier] = bool(st.session_state[widget_key])


def render_checklist(markdown, namespace, language=DEFAULT_LANGUAGE):
    """Show a completion checkbox for each marked practical step."""
    TEXT = load_text(language)
    blocks = parse_checklist(markdown)
    tasks = [block for block in blocks if isinstance(block, ChecklistTask)]
    progress = st.session_state.get(PROGRESS_KEY, {}).get(namespace, {})
    if tasks:
        completed = sum(progress.get(task.identifier, task.initial) for task in tasks)
        st.caption(
            TEXT["checklist_progress"].format(completed=completed, total=len(tasks))
        )
    for block in blocks:
        if isinstance(block, ChecklistTask):
            widget_key = f"learning_check_{namespace}_{block.identifier}"
            st.checkbox(
                block.label,
                value=progress.get(block.identifier, block.initial),
                key=widget_key,
                on_change=remember_check,
                args=(namespace, block.identifier, widget_key),
                help=TEXT["checklist_item_help"],
            )
        elif block.strip():
            st.markdown(block, unsafe_allow_html=True)
