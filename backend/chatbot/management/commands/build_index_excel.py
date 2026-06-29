import os
import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer
from django.core.management.base import BaseCommand

EXCEL_PATH = os.path.join("chatbot", "rag_data", "university_data.xlsx")
STORE_PATH = os.path.join("chatbot", "vector_store")
COLLECTION = "uni_koblenz_research"


def _safe(val) -> str:
    """Return a clean string even if the cell is NaN or None."""
    return str(val).strip() if val is not None and str(val) != "nan" else ""


def build_chunks(profs, members, projects, topics):
    """
    Convert every Excel row into a plain-text chunk plus metadata dict.
    Each chunk is self-contained so the LLM can read it without context.
    """
    chunks, metas, ids = [], [], []
    idx = 0

    # ── Professors ───────────────────────────────────────────────
    for _, row in profs.iterrows():
        text = (
            f"[PROFESSOR] {_safe(row.get('name'))} | "
            f"Institute: {_safe(row.get('institute'))} | "
            f"Role: {_safe(row.get('role'))} | "
            f"Chair: {_safe(row.get('position_chair'))}\n"
            f"Research Areas: {_safe(row.get('research_area'))}"
        )
        notes = _safe(row.get("notes"))
        if notes:
            text += f"\nNotes: {notes}"

        chunks.append(text)
        metas.append({
            "source":    "professors",
            "institute": _safe(row.get("institute")),
            "name":      _safe(row.get("name")),
        })
        ids.append(f"prof_{idx}")
        idx += 1

    # ── Team members (postdocs / PhD students) ───────────────────
    for _, row in members.iterrows():
        text = (
            f"[RESEARCHER] {_safe(row.get('name'))} | "
            f"Role: {_safe(row.get('role'))} | "
            f"Institute: {_safe(row.get('institute'))} | "
            f"Supervisor: {_safe(row.get('supervisor_professor'))}\n"
            f"Research Focus: {_safe(row.get('research_focus'))}"
        )
        chunks.append(text)
        metas.append({
            "source":    "team_members",
            "institute": _safe(row.get("institute")),
            "name":      _safe(row.get("name")),
        })
        ids.append(f"mem_{idx}")
        idx += 1

    # ── Projects ─────────────────────────────────────────────────
    for _, row in projects.iterrows():
        text = (
            f"[PROJECT] {_safe(row.get('project_name'))} | "
            f"Professor: {_safe(row.get('professor_name'))} | "
            f"Institute: {_safe(row.get('institute'))} | "
            f"Funding: {_safe(row.get('funding'))} | "
            f"Status: {_safe(row.get('status'))}\n"
            f"Description: {_safe(row.get('description'))}\n"
            f"Keywords: {_safe(row.get('keywords'))}"
        )
        chunks.append(text)
        metas.append({
            "source":    "projects",
            "institute": _safe(row.get("institute")),
            "name":      _safe(row.get("project_name")),
        })
        ids.append(f"proj_{idx}")
        idx += 1

    # ── Research topics ──────────────────────────────────────────
    for _, row in topics.iterrows():
        text = (
            f"[RESEARCH TOPIC] {_safe(row.get('topic_title'))} | "
            f"Professor: {_safe(row.get('professor_name'))} | "
            f"Institute: {_safe(row.get('institute'))}\n"
            f"Description: {_safe(row.get('description'))}\n"
            f"Keywords: {_safe(row.get('keywords'))}"
        )
        chunks.append(text)
        metas.append({
            "source":    "research_topics",
            "institute": _safe(row.get("institute")),
            "name":      _safe(row.get("topic_title")),
        })
        ids.append(f"topic_{idx}")
        idx += 1

    return chunks, metas, ids


class Command(BaseCommand):
    help = "Build ChromaDB vector index from university_data.xlsx"

    def handle(self, *args, **options):
        if not os.path.exists(EXCEL_PATH):
            self.stdout.write(self.style.ERROR(
                f"Excel file not found at {EXCEL_PATH}"
            ))
            return

        self.stdout.write("Reading Excel...")
        profs   = pd.read_excel(EXCEL_PATH, sheet_name="professors")
        members = pd.read_excel(EXCEL_PATH, sheet_name="team_members")
        projects  = pd.read_excel(EXCEL_PATH, sheet_name="projects")
        topics    = pd.read_excel(EXCEL_PATH, sheet_name="research_topics")

        chunks, metas, ids = build_chunks(profs, members, projects, topics)
        self.stdout.write(f"Built {len(chunks)} chunks from Excel "
                          f"({len(profs)} professors, {len(members)} researchers, "
                          f"{len(projects)} projects, {len(topics)} topics)")

        self.stdout.write("Loading embedding model (downloads once ~22 MB)...")
        model = SentenceTransformer("all-MiniLM-L6-v2")

        os.makedirs(STORE_PATH, exist_ok=True)
        db = chromadb.PersistentClient(path=STORE_PATH)

        try:
            db.delete_collection(COLLECTION)
        except Exception:
            pass
        collection = db.create_collection(COLLECTION)

        self.stdout.write(f"Embedding {len(chunks)} chunks...")
        vectors = model.encode(chunks, show_progress_bar=True).tolist()

        collection.add(ids=ids, documents=chunks, embeddings=vectors, metadatas=metas)

        self.stdout.write(self.style.SUCCESS(
            f"Done. {len(chunks)} chunks stored in ChromaDB collection '{COLLECTION}'."
        ))
