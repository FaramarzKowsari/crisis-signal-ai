"""Strong, interpretable classical NLP baseline."""

from __future__ import annotations

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


def build_tfidf_logistic_pipeline(
    max_features: int = 40000,
    min_df: int = 2,
    max_df: float = 0.98,
    max_iter: int = 1500,
    random_state: int = 42,
) -> Pipeline:
    return Pipeline(
        steps=[
            (
                "tfidf",
                TfidfVectorizer(
                    lowercase=True,
                    strip_accents="unicode",
                    ngram_range=(1, 2),
                    min_df=min_df,
                    max_df=max_df,
                    max_features=max_features,
                    sublinear_tf=True,
                ),
            ),
            (
                "classifier",
                LogisticRegression(
                    class_weight="balanced",
                    max_iter=max_iter,
                    random_state=random_state,
                    solver="liblinear",
                ),
            ),
        ]
    )
