"""
Lightweight local vector store using TF-IDF (scikit-learn).

Why TF-IDF instead of embeddings for this demo:
- Zero external API dependency -> runs fully offline, no API key needed for the
  retrieval step itself (only the final answer synthesis needs an LLM call).
- Knowledge base is small (a few policy docs) where TF-IDF performs well and is
  instant to build/rebuild.
- Swappable: `embed()` and `EmbeddingIndex` are written as a single interface so
  this can be replaced with a real embedding model (e.g. voyage/OpenAI/local
  sentence-transformers) without touching the retriever or agents.
"""
import os
import json
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

CHUNKS_PATH = os.path.join(os.path.dirname(__file__), "chunks.json")
INDEX_PATH = os.path.join(os.path.dirname(__file__), "tfidf_index.pkl")


class VectorStore:
    def __init__(self):
        self.chunks = []
        self.vectorizer = None
        self.matrix = None

    def build(self):
        with open(CHUNKS_PATH) as f:
            self.chunks = json.load(f)
        texts = [c["text"] for c in self.chunks]
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.matrix = self.vectorizer.fit_transform(texts)
        with open(INDEX_PATH, "wb") as f:
            pickle.dump({"chunks": self.chunks, "vectorizer": self.vectorizer, "matrix": self.matrix}, f)
        return self

    def load(self):
        with open(INDEX_PATH, "rb") as f:
            data = pickle.load(f)
        self.chunks = data["chunks"]
        self.vectorizer = data["vectorizer"]
        self.matrix = data["matrix"]
        return self

    def search(self, query, top_k=3):
        query_vec = self.vectorizer.transform([query])
        sims = cosine_similarity(query_vec, self.matrix).flatten()
        top_idx = sims.argsort()[::-1][:top_k]
        results = []
        for i in top_idx:
            if sims[i] <= 0:
                continue
            results.append({**self.chunks[i], "score": round(float(sims[i]), 4)})
        return results


def build_index():
    from ingest import build_chunks
    build_chunks()
    return VectorStore().build()


if __name__ == "__main__":
    store = build_index()
    print(f"Indexed {len(store.chunks)} chunks.")
    demo = store.search("what happens if a deal has no activity for 3 weeks")
    for r in demo:
        print(f"[{r['score']}] {r['source']} :: {r['heading']}")
