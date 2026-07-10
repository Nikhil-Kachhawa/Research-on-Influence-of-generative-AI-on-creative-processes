import os
import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer
from django.core.management.base import BaseCommand

# Bilingual Excel files
EXCEL_PATH_EN = os.path.join("chatbot", "rag_data", "university_data.xlsx")
EXCEL_PATH_DE = os.path.join("chatbot", "rag_data", "university_data_de.xlsx")
STORE_PATH = os.path.join("chatbot", "vector_store")
COLLECTION = "uni_koblenz_research"


def _safe(val) -> str:
    """Return a clean string even if the cell is NaN or None."""
    return str(val).strip() if val is not None and str(val) != "nan" else ""


def build_chunks(profs, projects, topics):
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
        # Read both English and German Excel files
        excel_files = [
            ("English", EXCEL_PATH_EN),
            ("German", EXCEL_PATH_DE),
        ]

        all_chunks, all_metas, all_ids = [], [], []
        idx = 0

        for lang_name, excel_path in excel_files:
            if not os.path.exists(excel_path):
                self.stdout.write(self.style.WARNING(
                    f"{lang_name} Excel file not found at {excel_path}"
                ))
                continue

            self.stdout.write(f"Reading {lang_name} Excel...")
            profs    = pd.read_excel(excel_path, sheet_name="professors")
            projects = pd.read_excel(excel_path, sheet_name="projects")
            topics   = pd.read_excel(excel_path, sheet_name="research_topics")

            chunks, metas, ids = build_chunks(profs, projects, topics)

            # Add language tag to metadata so we know which language each chunk is
            for meta in metas:
                meta["language"] = lang_name.lower()

            # Offset IDs to avoid collision between English and German
            offset_ids = [f"{lang_name[0].lower()}_{id_}" for id_ in ids]

            all_chunks.extend(chunks)
            all_metas.extend(metas)
            all_ids.extend(offset_ids)
            idx += len(chunks)

        if not all_chunks:
            self.stdout.write(self.style.ERROR("No chunks built from Excel files"))
            return

        self.stdout.write(f"Built {len(all_chunks)} total chunks "
                          f"(English + German combined)")

        self.stdout.write("Loading multilingual embedding model (downloads once ~110 MB)...")
        model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

        os.makedirs(STORE_PATH, exist_ok=True)
        db = chromadb.PersistentClient(path=STORE_PATH)

        try:
            db.delete_collection(COLLECTION)
        except Exception:
            pass
        collection = db.create_collection(COLLECTION)

        self.stdout.write(f"Embedding {len(all_chunks)} chunks with multilingual model...")
        vectors = model.encode(all_chunks, show_progress_bar=True).tolist()

        collection.add(ids=all_ids, documents=all_chunks, embeddings=vectors, metadatas=all_metas)

        self.stdout.write(self.style.SUCCESS(
            f"Done. {len(all_chunks)} chunks (EN + DE) stored in ChromaDB collection '{COLLECTION}'."
        ))