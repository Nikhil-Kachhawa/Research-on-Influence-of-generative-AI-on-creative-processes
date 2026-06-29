import os
import logging
import chromadb
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

STORE_PATH = os.path.join("chatbot", "vector_store")
COLLECTION = "uni_koblenz_research"

_model = None
_collection = None


def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def _get_collection():
    global _collection
    if _collection is None:
        db = chromadb.PersistentClient(path=STORE_PATH)
        _collection = db.get_collection(COLLECTION)
    return _collection


def retrieve_context(query: str, n_results: int = 5) -> str:
    """
    Embed the query, search ChromaDB built from university_data.xlsx,
    and return the top-n chunks as a formatted string for prompt injection.
    Falls back to empty string on any error so the LLM still responds.
    """
    try:
        query_vec = _get_model().encode([query])[0].tolist()

        results = _get_collection().query(
            query_embeddings=[query_vec],
            n_results=n_results,
            include=["documents", "metadatas"],
        )

        parts = []
        for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
            source = meta.get("source", "")
            parts.append(f"[{source.upper().replace('_', ' ')}]\n{doc}")

        return "\n\n---\n\n".join(parts)

    except Exception:
        logger.exception("RAG retrieval failed — continuing without context")
        return ""
