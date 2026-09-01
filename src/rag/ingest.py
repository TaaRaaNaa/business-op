"""
Chunking + ingestion for the knowledge base.
Splits markdown docs into passage-level chunks (by ## heading) so retrieval
returns focused, citeable context instead of whole-document dumps.
"""
import os
import re
import json

KB_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "knowledge_base")
INDEX_PATH = os.path.join(os.path.dirname(__file__), "chunks.json")

def chunk_markdown(text, source):
    """Split on '## ' headings; keep the heading with its body as one chunk."""
    parts = re.split(r"\n(?=## )", text)
    chunks = []
    for part in parts:
        part = part.strip()
        if not part or part.startswith("# "):  # skip the H1 title-only fragment
            if part.startswith("# ") and "\n" not in part:
                continue
        heading_match = re.match(r"##\s*(.+)", part)
        heading = heading_match.group(1) if heading_match else source
        if part:
            chunks.append({"source": source, "heading": heading, "text": part})
    return chunks

def build_chunks():
    all_chunks = []
    for fname in sorted(os.listdir(KB_DIR)):
        if not fname.endswith(".md"):
            continue
        path = os.path.join(KB_DIR, fname)
        with open(path) as f:
            text = f.read()
        all_chunks.extend(chunk_markdown(text, fname))
    with open(INDEX_PATH, "w") as f:
        json.dump(all_chunks, f, indent=2)
    return all_chunks

if __name__ == "__main__":
    chunks = build_chunks()
    print(f"Built {len(chunks)} chunks -> {INDEX_PATH}")
