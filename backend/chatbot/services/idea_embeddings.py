import logging
from functools import lru_cache
from typing import Sequence

import numpy as np
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

#EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

EMBEDDING_MODEL_NAME = (
    "sentence-transformers/"
    "paraphrase-multilingual-MiniLM-L12-v2"
)


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    """
    Load and cache the SentenceTransformer model.

    The model is loaded only when this function is first called,
    rather than when Django starts.
    """

    logger.info(
        "Loading sentence embedding model: %s",
        EMBEDDING_MODEL_NAME,
    )

    return SentenceTransformer(EMBEDDING_MODEL_NAME)


def create_idea_embeddings(
    ideas: Sequence[str],
) -> np.ndarray:
    """
    Convert accepted research ideas into normalized embeddings.

    Parameters
    ----------
    ideas:
        Ordered collection of accepted research-idea strings.

    Returns
    -------
    numpy.ndarray:
        Matrix shaped (number_of_ideas, 384).
    """

    cleaned_ideas = [
        str(idea).strip()
        for idea in ideas
        if idea and str(idea).strip()
    ]

    if not cleaned_ideas:
        return np.empty((0, 384), dtype=np.float32)

    model = get_embedding_model()

    embeddings = model.encode(
        cleaned_ideas,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )

    return embeddings.astype(np.float32)