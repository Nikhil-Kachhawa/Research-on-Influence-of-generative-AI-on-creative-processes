from dataclasses import dataclass

import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class ClusteringResult:
    labels: np.ndarray
    cluster_count: int
    silhouette_score: float | None


def _cluster_two_ideas(
    embeddings: np.ndarray,
    similarity_threshold: float = 0.55,
) -> ClusteringResult:
    """
    Two ideas cannot be evaluated using silhouette score.

    Group them when semantic similarity is sufficiently high;
    otherwise, keep them as separate clusters.
    """

    similarity = float(
        cosine_similarity(
            embeddings[0:1],
            embeddings[1:2],
        )[0][0]
    )

    if similarity >= similarity_threshold:
        labels = np.array([0, 0], dtype=int)
        cluster_count = 1
    else:
        labels = np.array([0, 1], dtype=int)
        cluster_count = 2

    return ClusteringResult(
        labels=labels,
        cluster_count=cluster_count,
        silhouette_score=None,
    )


def cluster_ideas(
    embeddings: np.ndarray,
    max_clusters: int = 6,
) -> ClusteringResult:
    """
    Cluster semantic idea embeddings using Agglomerative
    Hierarchical Clustering.

    For three or more ideas, the cluster count is selected using
    the highest cosine silhouette score.
    """

    number_of_ideas = len(embeddings)

    if number_of_ideas == 0:
        return ClusteringResult(
            labels=np.array([], dtype=int),
            cluster_count=0,
            silhouette_score=None,
        )

    if number_of_ideas == 1:
        return ClusteringResult(
            labels=np.array([0], dtype=int),
            cluster_count=1,
            silhouette_score=None,
        )

    if number_of_ideas == 2:
        return _cluster_two_ideas(embeddings)

    maximum_k = min(
        max_clusters,
        number_of_ideas - 1,
    )

    best_labels = None
    best_score = -1.0
    best_cluster_count = 0

    for cluster_count in range(2, maximum_k + 1):

        model = AgglomerativeClustering(
            n_clusters=cluster_count,
            metric="cosine",
            linkage="average",
        )

        labels = model.fit_predict(embeddings)

        score = float(
            silhouette_score(
                embeddings,
                labels,
                metric="cosine",
            )
        )

        if score > best_score:
            best_score = score
            best_labels = labels
            best_cluster_count = cluster_count

    return ClusteringResult(
        labels=np.asarray(best_labels, dtype=int),
        cluster_count=best_cluster_count,
        silhouette_score=best_score,
    )