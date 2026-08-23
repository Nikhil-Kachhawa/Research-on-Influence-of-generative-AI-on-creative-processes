# import re
# from typing import Sequence

# import numpy as np
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity


# import re
# from typing import Sequence

# import numpy as np
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity


# def generate_local_cluster_name(
#     ideas: Sequence[str],
#     cluster_number: int,
# ) -> str:
#     """
#     Generate one concise cluster topic locally using TF-IDF.

#     Returns one noun-like topic phrase without '/', '&',
#     commas, or multiple combined labels.
#     """

#     cleaned_ideas = [
#         str(idea).strip()
#         for idea in ideas
#         if idea and str(idea).strip()
#     ]

#     if not cleaned_ideas:
#         return f"Cluster {cluster_number}"

#     try:
#         vectorizer = TfidfVectorizer(
#             stop_words="english",
#             # Prefer meaningful two- or three-word phrases.
#             ngram_range=(2, 3),
#             max_features=100,
#         )

#         matrix = vectorizer.fit_transform(cleaned_ideas)
#         feature_names = vectorizer.get_feature_names_out()

#         average_scores = np.asarray(
#             matrix.mean(axis=0)
#         ).ravel()

#         ranked_indexes = average_scores.argsort()[::-1]

#         for index in ranked_indexes:
#             topic = feature_names[index].strip()

#             if not topic:
#                 continue

#             topic = _clean_cluster_name(topic)

#             if topic:
#                 return topic

#     except ValueError:
#         # This can happen when the ideas contain too few usable words.
#         pass

#     # Fallback: derive one short phrase from the first idea.
#     fallback = _fallback_cluster_name(
#         cleaned_ideas[0],
#         cluster_number,
#     )

#     return fallback


# def _clean_cluster_name(topic: str) -> str:
#     """
#     Normalize one selected cluster topic.
#     """

#     # Remove separators and punctuation.
#     topic = re.sub(r"[/&,;:|]+", " ", topic)

#     # Keep letters, numbers, hyphens, and spaces.
#     topic = re.sub(
#         r"[^A-Za-z0-9\s\-]",
#         "",
#         topic,
#     )

#     topic = re.sub(r"\s+", " ", topic).strip()

#     if not topic:
#         return ""

#     # Remove weak leading action words.
#     weak_leading_words = {
#         "using",
#         "use",
#         "comparing",
#         "compare",
#         "testing",
#         "test",
#         "determining",
#         "determine",
#         "analyzing",
#         "analyse",
#         "analyze",
#         "investigating",
#         "investigate",
#         "studying",
#         "study",
#         "evaluating",
#         "evaluate",
#         "developing",
#         "develop",
#     }

#     words = topic.split()

#     while words and words[0].lower() in weak_leading_words:
#         words.pop(0)

#     if not words:
#         return ""

#     # Maximum three words.
#     words = words[:3]

#     return " ".join(words).title()


# def _fallback_cluster_name(
#     idea: str,
#     cluster_number: int,
# ) -> str:
#     """
#     Create one short name when TF-IDF cannot find a phrase.
#     """

#     cleaned = re.sub(r"[/&,;:|]+", " ", idea)
#     cleaned = re.sub(
#         r"[^A-Za-z0-9\s\-]",
#         "",
#         cleaned,
#     )
#     cleaned = re.sub(r"\s+", " ", cleaned).strip()

#     weak_words = {
#         "using",
#         "use",
#         "comparing",
#         "compare",
#         "testing",
#         "test",
#         "determining",
#         "determine",
#         "analyzing",
#         "analyse",
#         "analyze",
#         "investigating",
#         "investigate",
#         "studying",
#         "study",
#         "evaluating",
#         "evaluate",
#         "developing",
#         "develop",
#         "the",
#         "a",
#         "an",
#         "of",
#         "for",
#         "in",
#         "on",
#         "with",
#         "and",
#         "to",
#     }

#     useful_words = [
#         word
#         for word in cleaned.split()
#         if word.lower() not in weak_words
#     ]

#     if not useful_words:
#         return f"Cluster {cluster_number}"

#     return " ".join(
#         useful_words[:3]
#     ).title()


# def calculate_cluster_evidence(
#     cluster_embeddings: np.ndarray,
# ) -> tuple[list[float], float]:
#     """
#     Calculate each idea's similarity to its cluster centroid.

#     Returns:
#         individual similarities and average similarity.
#     """

#     if len(cluster_embeddings) == 0:
#         return [], 0.0

#     centroid = cluster_embeddings.mean(
#         axis=0,
#         keepdims=True,
#     )

#     similarities = cosine_similarity(
#         cluster_embeddings,
#         centroid,
#     ).ravel()

#     scores = [
#         round(float(score), 4)
#         for score in similarities
#     ]

#     average_similarity = round(
#         float(np.mean(similarities)),
#         4,
#     )

#     return scores, average_similarity


# def build_cluster_reason(
#     ideas: Sequence[str],
#     average_similarity: float,
# ) -> str:
#     """
#     Produce an auditable explanation for the grouping.
#     """

#     if len(ideas) == 1:
#         return (
#             "This is a distinct research direction that was not "
#             "combined with another accepted idea."
#         )

#     return (
#         f"These {len(ideas)} accepted ideas were grouped because "
#         f"their Sentence-BERT embeddings are semantically similar. "
#         f"The average cosine similarity to the cluster centroid is "
#         f"{average_similarity:.3f}."
#     )



import re
from typing import Sequence

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


MULTILINGUAL_STOP_WORDS = {
    # English
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "using",
    "use",
    "with",

    # German
    "aber",
    "als",
    "am",
    "an",
    "auch",
    "auf",
    "aus",
    "bei",
    "das",
    "dem",
    "den",
    "der",
    "des",
    "die",
    "durch",
    "ein",
    "eine",
    "einer",
    "eines",
    "für",
    "im",
    "in",
    "ist",
    "mit",
    "oder",
    "sich",
    "und",
    "von",
    "vor",
    "wie",
    "zu",
    "zur",
    "zum",
}


WEAK_LEADING_WORDS = {
    # English
    "using",
    "use",
    "comparing",
    "compare",
    "testing",
    "test",
    "determining",
    "determine",
    "analyzing",
    "analyse",
    "analyze",
    "investigating",
    "investigate",
    "studying",
    "study",
    "evaluating",
    "evaluate",
    "developing",
    "develop",

    # German
    "verwenden",
    "verwendung",
    "nutzen",
    "nutzung",
    "vergleichen",
    "vergleich",
    "testen",
    "untersuchen",
    "untersuchung",
    "analysieren",
    "analyse",
    "bewerten",
    "bewertung",
    "entwickeln",
    "entwicklung",
}


FALLBACK_WEAK_WORDS = WEAK_LEADING_WORDS | {
    # English
    "the",
    "a",
    "an",
    "of",
    "for",
    "in",
    "on",
    "with",
    "and",
    "to",

    # German
    "der",
    "die",
    "das",
    "den",
    "dem",
    "des",
    "ein",
    "eine",
    "einer",
    "eines",
    "für",
    "im",
    "in",
    "mit",
    "und",
    "oder",
    "von",
    "zu",
    "zur",
    "zum",
}


def generate_local_cluster_name(
    ideas: Sequence[str],
    cluster_number: int,
) -> str:
    """
    Generate one concise multilingual cluster label using TF-IDF.

    Supports English, German, and mixed-language ideas.
    Returns one topic phrase without '/', '&', commas,
    or multiple combined labels.
    """

    cleaned_ideas = [
        str(idea).strip()
        for idea in ideas
        if idea and str(idea).strip()
    ]

    if not cleaned_ideas:
        return f"Cluster {cluster_number}"

    try:
        vectorizer = TfidfVectorizer(
            stop_words=list(MULTILINGUAL_STOP_WORDS),
            ngram_range=(1, 3),
            max_features=100,
            lowercase=True,
        )

        matrix = vectorizer.fit_transform(cleaned_ideas)
        feature_names = vectorizer.get_feature_names_out()

        average_scores = np.asarray(
            matrix.mean(axis=0)
        ).ravel()

        ranked_indexes = average_scores.argsort()[::-1]

        for index in ranked_indexes:
            topic = feature_names[index].strip()

            if not topic:
                continue

            cleaned_topic = _clean_cluster_name(topic)

            if cleaned_topic:
                return cleaned_topic

    except ValueError:
        # Happens when there are too few usable terms.
        pass

    return _fallback_cluster_name(
        cleaned_ideas[0],
        cluster_number,
    )


def _clean_cluster_name(topic: str) -> str:
    """
    Normalize one multilingual cluster topic.
    """

    topic = re.sub(r"[/&,;:|]+", " ", topic)

    # Keep Unicode letters, digits, hyphens, and spaces.
    # This preserves German characters such as ä, ö, ü and ß.
    topic = re.sub(
        r"[^\w\s\-]",
        "",
        topic,
        flags=re.UNICODE,
    )

    topic = re.sub(r"\s+", " ", topic).strip()

    if not topic:
        return ""

    words = topic.split()

    while (
        words
        and words[0].casefold() in WEAK_LEADING_WORDS
    ):
        words.pop(0)

    if not words:
        return ""

    words = words[:3]

    return " ".join(words).title()


def _fallback_cluster_name(
    idea: str,
    cluster_number: int,
) -> str:
    """
    Create one short multilingual name when TF-IDF cannot find a phrase.
    """

    cleaned = re.sub(r"[/&,;:|]+", " ", idea)

    cleaned = re.sub(
        r"[^\w\s\-]",
        "",
        cleaned,
        flags=re.UNICODE,
    )

    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    useful_words = [
        word
        for word in cleaned.split()
        if word.casefold() not in FALLBACK_WEAK_WORDS
    ]

    if not useful_words:
        return f"Cluster {cluster_number}"

    return " ".join(
        useful_words[:3]
    ).title()


def calculate_cluster_evidence(
    cluster_embeddings: np.ndarray,
) -> tuple[list[float], float]:
    """
    Calculate each idea's similarity to its cluster centroid.
    """

    if len(cluster_embeddings) == 0:
        return [], 0.0

    centroid = cluster_embeddings.mean(
        axis=0,
        keepdims=True,
    )

    similarities = cosine_similarity(
        cluster_embeddings,
        centroid,
    ).ravel()

    scores = [
        round(float(score), 4)
        for score in similarities
    ]

    average_similarity = round(
        float(np.mean(similarities)),
        4,
    )

    return scores, average_similarity


def build_cluster_reason(
    ideas: Sequence[str],
    average_similarity: float,
) -> str:
    """
    Produce an auditable explanation for the grouping.
    """

    if len(ideas) == 1:
        return (
            "This is a distinct research direction that was not "
            "combined with another accepted idea."
        )

    return (
        f"These {len(ideas)} accepted ideas were grouped because "
        f"their multilingual Sentence-BERT embeddings are "
        f"semantically similar. The average cosine similarity "
        f"to the cluster centroid is "
        f"{average_similarity:.3f}."
    )