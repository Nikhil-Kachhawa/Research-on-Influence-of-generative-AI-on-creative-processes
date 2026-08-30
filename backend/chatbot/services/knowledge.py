"""
Excel-based knowledge retrieval for WeST / FB4 university data.

Supports bilingual setup: separate Excel files for English and German.
- university_data.xlsx (English)
- university_data_de.xlsx (German)

Usage:
    from chatbot.services.knowledge import get_context
    snippet = get_context("What projects are about knowledge graphs?", language="en")
    snippet_de = get_context("Welche Projekte behandeln Wissensgraphen?", language="de")

Retrieval strategy: keyword overlap between query tokens and indexed text rows.
No ML model needed — fast, transparent, and fully offline.
"""
import os
import logging
import re
from functools import lru_cache

import pandas as pd

logger = logging.getLogger(__name__)

# Bilingual Excel files
EXCEL_PATH_EN = os.path.join(
    os.path.dirname(__file__), "..", "rag_data", "university_data.xlsx"
)
EXCEL_PATH_DE = os.path.join(
    os.path.dirname(__file__), "..", "rag_data", "university_data_de.xlsx"
)

# ── Data loading (cached per language) ────────────────────────────────────

@lru_cache(maxsize=2)
def _load_data(language: str = "en"):
    """Load Excel file for the specified language (en or de)."""
    try:
        excel_path = EXCEL_PATH_DE if language == "de" else EXCEL_PATH_EN
        path = os.path.abspath(excel_path)

        if not os.path.exists(path):
            logger.warning(f"Knowledge base not found for language {language}: {path}")
            return None, None, None

        profs    = pd.read_excel(path, sheet_name="professors")
        projects = pd.read_excel(path, sheet_name="projects")
        topics   = pd.read_excel(path, sheet_name="research_topics")
        return profs, projects, topics
    except Exception:
        logger.exception(f"Failed to load university_data for language {language}")
        return None, None, None


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

def get_context(query: str, max_items_per_section: int = 3, language: str = "en") -> str:
    """
    Retrieve university context for RAG grounding.

    Args:
        query: User question/message
        max_items_per_section: How many results per category
        language: "de" for German, "en" for English (default)

    Returns:
        Formatted markdown snippet for prompt injection, or empty string if no match.

    Loads the appropriate language-specific Excel file (university_data.xlsx or
    university_data_de.xlsx) and searches it with the same column names.
    """
    try:
        profs, projects, topics = _load_data(language=language)
        if profs is None:
            return ""

        query_tokens = _tokenize(query)
        if not query_tokens:
            return ""

        # Standard columns (same in both EN and DE files)
        topic_cols = ["topic_title", "description", "keywords",
                      "professor_name", "institute"]
        project_cols = ["project_name", "description", "keywords",
                        "professor_name", "institute"]
        prof_cols = ["name", "research_area", "position_chair",
                     "institute", "notes"]

        # Filter to only columns that exist
        topic_cols = [c for c in topic_cols if c in topics.columns]
        project_cols = [c for c in project_cols if c in projects.columns]
        prof_cols = [c for c in prof_cols if c in profs.columns]

        parts = []

        # Research topics — highest priority for thesis ideas
        t_df = _score_rows(topics, query_tokens, topic_cols)
        if not t_df.empty:
            header = ("**Relevante Forschungsthemen der Universität:**"
                      if language == "de"
                      else "**Relevant Research Topics at the University:**")
            parts.append(header + "\n" + _format_topics(t_df, max_items_per_section))

        # Projects
        p_df = _score_rows(projects, query_tokens, project_cols)
        if not p_df.empty:
            header = ("**Aktuelle Forschungsprojekte:**"
                      if language == "de"
                      else "**Relevant Research Projects:**")
            parts.append(header + "\n" + _format_projects(p_df, max_items_per_section))

        # Professors
        pr_df = _score_rows(profs, query_tokens, prof_cols)
        if not pr_df.empty:
            header = ("**Verwandte Fakultätsmitglieder:**"
                      if language == "de"
                      else "**Related Faculty Members:**")
            parts.append(header + "\n" + _format_professors(pr_df, max_items_per_section))

        return "\n\n".join(parts)

    except Exception:
        logger.exception("knowledge.get_context failed")
        return ""