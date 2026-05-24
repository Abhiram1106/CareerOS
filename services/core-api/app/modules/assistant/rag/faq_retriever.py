from __future__ import annotations

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .faq_corpus import FAQ_CHUNKS


class FaqRetriever:
    def __init__(self) -> None:
        texts = [chunk["text"] for chunk in FAQ_CHUNKS]
        self._ids = [chunk["id"] for chunk in FAQ_CHUNKS]
        self._vectorizer = TfidfVectorizer(stop_words="english")
        self._matrix = self._vectorizer.fit_transform(texts)

    def retrieve(self, query: str, *, top_k: int = 3) -> list[tuple[str, str]]:
        if not query.strip():
            return []
        query_vec = self._vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self._matrix).flatten()
        ranked = sorted(enumerate(scores), key=lambda item: item[1], reverse=True)[:top_k]
        return [(self._ids[i], FAQ_CHUNKS[i]["text"]) for i, score in ranked if score > 0.05]
