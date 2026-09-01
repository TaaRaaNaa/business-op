"""
Feedback Synthesis Agent — aggregates client_feedback.csv into recurring
themes per the escalation policy's "3+ similar items in 90 days" auto-flag rule,
and answers natural-language questions against the RAG knowledge base.
"""
import os
import sys
import pandas as pd
from datetime import datetime, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "rag"))
from retriever import retrieve

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw")

def recurring_themes(window_days: int = 90, min_count: int = 3) -> list:
    feedback = pd.read_csv(os.path.join(DATA_DIR, "client_feedback.csv"))
    feedback["feedback_date"] = pd.to_datetime(feedback["feedback_date"])
    cutoff = datetime.now() - timedelta(days=window_days)
    recent = feedback[feedback.feedback_date >= cutoff]
    grouped = recent.groupby(["theme", "category", "severity"]).size().reset_index(name="count")
    flagged = grouped[grouped["count"] >= min_count].sort_values("count", ascending=False)
    return flagged.to_dict(orient="records")

def answer_policy_question(question: str, top_k: int = 3) -> dict:
    """RAG-grounded answer: retrieve relevant policy chunks for a question.
    In the full demo, these chunks are passed to Claude as context; here we
    return the grounding chunks directly so the tool is testable without an API key.
    """
    chunks = retrieve(question, top_k=top_k)
    return {
        "question": question,
        "retrieved_context": chunks,
        "note": "Pass `retrieved_context` to the LLM synthesis step (see prompts/) for a natural-language answer."
    }

if __name__ == "__main__":
    import json
    print(json.dumps(recurring_themes(), indent=2, default=str))
    print(json.dumps(answer_policy_question("what is the SLA for a high severity escalation"), indent=2))
