"""
Excel-based knowledge retrieval for WeST / FB4 university data.

Usage:
    from chatbot.services.knowledge import get_context
    snippet = get_context("What projects are about knowledge graphs?")

Retrieval strategy: keyword overlap between query tokens and indexed text rows.
No ML model needed — fast, transparent, and fully offline.
"""
import os
import logging
import re
from functools import lru_cache

import pandas as pd

logger = logging.getLogger(__name__)

EXCEL_PATH = os.path.join(
    os.path.dirname(__file__), "..", "rag_data", "university_data.xlsx"
)

# ── Data loading (cached at module level) ────────────────────────────────────

@lru_cache(maxsize=1)
def _load_data():
    try:
        path = os.path.abspath(EXCEL_PATH)
        profs   = pd.read_excel(path, sheet_name="professors")
        members = pd.read_excel(path, sheet_name="team_members")
        projects  = pd.read_excel(path, sheet_name="projects")
        topics    = pd.read_excel(path, sheet_name="research_topics")
        return profs, members, projects, topics
    except Exception:
        logger.exception("Failed to load university_data.xlsx")
        return None, None, None, None


# ── Text normalisation helpers ───────────────────────────────────────────────

def _tokenize(text: str) -> set:
    """Lowercase alphanumeric tokens of length >= 3."""
    if not text:
        return set()
    return {w for w in re.findall(r"[a-z0-9äöüß]+", str(text).lower()) if len(w) >= 3}


def _row_text(row: pd.Series, cols: list) -> str:
    """Concatenate specified columns into a single searchable string."""
    return " ".join(str(row[c]) for c in cols if c in row.index and pd.notna(row[c]))


# ── Score and rank rows ──────────────────────────────────────────────────────

def _score_rows(df: pd.DataFrame, query_tokens: set, text_cols: list) -> pd.DataFrame:
    if df is None or df.empty:
        return pd.DataFrame()
    scores = []
    for _, row in df.iterrows():
        row_tokens = _tokenize(_row_text(row, text_cols))
        scores.append(len(query_tokens & row_tokens))
    df = df.copy()
    df["_score"] = scores
    return df[df["_score"] > 0].sort_values("_score", ascending=False)


# ── Format results as readable text ─────────────────────────────────────────

def _format_professors(df: pd.DataFrame, n: int) -> str:
    lines = []
    for _, row in df.head(n).iterrows():
        name    = row.get("name", "")
        pos     = row.get("position_chair", "")
        inst    = row.get("institute", "")
        area    = row.get("research_area", "")
        lines.append(f"• Prof. {name} ({inst}){' — ' + pos if pos else ''}")
        if area:
            lines.append(f"  Research areas: {area}")
    return "\n".join(lines)


def _format_members(df: pd.DataFrame, n: int) -> str:
    lines = []
    for _, row in df.head(n).iterrows():
        name   = row.get("name", "")
        role   = row.get("role", "")
        sup    = row.get("supervisor_professor", "")
        inst   = row.get("institute", "")
        focus  = row.get("research_focus", "")
        lines.append(f"• {name} — {role}, {inst}" + (f" (supervisor: {sup})" if sup else ""))
        if focus:
            lines.append(f"  Focus: {focus}")
    return "\n".join(lines)


def _format_projects(df: pd.DataFrame, n: int) -> str:
    lines = []
    for _, row in df.head(n).iterrows():
        name   = row.get("project_name", "")
        prof   = row.get("professor_name", "")
        inst   = row.get("institute", "")
        desc   = row.get("description", "")
        status = row.get("status", "")
        lines.append(f"• {name} ({inst}, {prof})" + (f" [{status}]" if status else ""))
        if desc:
            lines.append(f"  {str(desc)[:200]}")
    return "\n".join(lines)


def _format_topics(df: pd.DataFrame, n: int) -> str:
    lines = []
    for _, row in df.head(n).iterrows():
        title  = row.get("topic_title", "")
        prof   = row.get("professor_name", "")
        inst   = row.get("institute", "")
        desc   = row.get("description", "")
        lines.append(f"• {title} — {prof} ({inst})")
        if desc:
            lines.append(f"  {str(desc)[:200]}")
    return "\n".join(lines)


# ── Public API ───────────────────────────────────────────────────────────────

def get_context(query: str, max_items_per_section: int = 3) -> str:
    """
    Return a formatted context string (or empty string on failure) based on
    keyword overlap between *query* and each Excel sheet.
    """
    try:
        profs, members, projects, topics = _load_data()
        if profs is None:
            return ""

        query_tokens = _tokenize(query)
        if not query_tokens:
            return ""

        parts = []

        # Research topics — highest priority for thesis ideas
        t_df = _score_rows(topics, query_tokens,
                           ["topic_title", "description", "keywords",
                            "professor_name", "institute"])
        if not t_df.empty:
            parts.append("**Relevant Research Topics at the University:**\n"
                         + _format_topics(t_df, max_items_per_section))

        # Projects
        p_df = _score_rows(projects, query_tokens,
                           ["project_name", "description", "keywords",
                            "professor_name", "institute"])
        if not p_df.empty:
            parts.append("**Relevant Research Projects:**\n"
                         + _format_projects(p_df, max_items_per_section))

        # Professors
        pr_df = _score_rows(profs, query_tokens,
                            ["name", "research_area", "position_chair",
                             "institute", "notes"])
        if not pr_df.empty:
            parts.append("**Related Faculty Members:**\n"
                         + _format_professors(pr_df, max_items_per_section))

        # Team members (postdocs / doctoral candidates)
        m_df = _score_rows(members, query_tokens,
                           ["name", "research_focus", "role",
                            "supervisor_professor", "institute"])
        if not m_df.empty:
            parts.append("**Related Researchers / Doctoral Candidates:**\n"
                         + _format_members(m_df, max_items_per_section))

        return "\n\n".join(parts)

    except Exception:
        logger.exception("knowledge.get_context failed")
        return ""
