"""
Explore document vectors.

@author: Yuanjing Zhu

"""
from functools import lru_cache
from typing import List

import nltk
import numpy as np

categories = [
    "hobbies",
    "romance",
]


@lru_cache
def load(document_name: str) -> List[str]:
    """Load document by name."""
    return nltk.corpus.brown.words(fileids=[document_name])


class KNN:
    """K-nearest neighbors classifier."""

    def __init__(self, *args, **kwargs):
        """Initialize."""
        pass

    def train(self, X, Y):
        """Train."""
        self.X = X
        self.Y = Y

    def compute_distances(self, X):
        """Compute distances between test and train points."""
        return (
            np.add.reduce(
                [(X[:, [idx]] - self.X[:, [idx]].T) ** 2 for idx in range(X.shape[1])]
            )
            ** 0.5
        )

    def nearby(self, X):
        """Compute ordered list of nearby labels."""
        distances = self.compute_distances(X)
        idx = np.argsort(distances, axis=1)
        distances = np.sort(distances, axis=1)
        return self.Y[idx], distances

    def decide(self, X, k):
        """Find the most-common label in the top k."""
        modes = []
        labels, _ = self.nearby(X)
        for ys in labels:
            p = 1 / k
            modes.append(round(np.sum(ys[:k] * p)))
        return modes


def main():
    """Classify documents."""
    terms = [
        "to",
        "could",
    ]
    documents = [
        load(document_name)
        for category in categories
        for document_name in nltk.corpus.brown.fileids(categories=[category])
    ]

    Y = np.array(
        [
            idx
            for idx, category in enumerate(categories)
            for _ in nltk.corpus.brown.fileids(categories=[category])
        ]
    )

    X = np.array([[document.count(term) for term in terms] for document in documents])

    knn = KNN()

    # leave-one-out cross-validation
    Y_hat = np.empty(Y.shape)
    for idx in range(X.shape[0]):
        X_train = np.concatenate(
            (
                X.copy()[:idx, :],
                X.copy()[idx + 1 :, :],
            ),
            axis=0,
        )
        Y_train = np.concatenate(
            (
                Y.copy()[:idx],
                Y.copy()[idx + 1 :],
            ),
            axis=0,
        )
        knn.train(X_train, Y_train)
        Y_hat[[idx]] = knn.decide(X[[idx], :], k=5)

    print(np.sum(Y_hat == Y) / Y.shape[0] * 100, "percent correct")


if __name__ == "__main__":
    main()
