"""
Thin retrieval interface used by agents and the MCP server.
Keeps the RAG contract simple: retrieve(query, top_k) -> list[{source, heading, text, score}]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from vector_store import VectorStore, build_index, INDEX_PATH

_store = None

def get_store():
    global _store
    if _store is None:
        _store = VectorStore()
        if os.path.exists(INDEX_PATH):
            _store.load()
        else:
            _store = build_index()
    return _store

def retrieve(query: str, top_k: int = 3):
    store = get_store()
    return store.search(query, top_k=top_k)
