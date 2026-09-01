"""
Basic tests for the agent/tool layer. Run with: pytest tests/
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "mcp_server"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "agents"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "rag"))

import tools
import kpi_agent
import lead_leakage_agent
import feedback_synthesis_agent
from retriever import retrieve


def test_leakage_summary_shape():
    result = tools.call_tool("get_leakage_summary")
    assert result["status"] == "success"
    data = result["data"]
    for key in ["total_open_opportunities", "at_risk_count", "at_risk_value_usd", "leakage_rate_pct"]:
        assert key in data


def test_kpi_agent_returns_valid_risk_flag():
    accounts_path = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "accounts.csv")
    import pandas as pd
    accounts = pd.read_csv(accounts_path)
    sample_id = accounts.account_id.iloc[0]
    kpis = kpi_agent.compute_kpis(sample_id)
    assert kpis["risk_flag"] in ("Healthy", "Watch", "At Risk")
    assert 0 <= kpis["composite_score"] <= 100


def test_unknown_tool_returns_error():
    result = tools.call_tool("not_a_real_tool")
    assert result["status"] == "error"


def test_retriever_returns_relevant_chunk_for_escalation_question():
    results = retrieve("what is the SLA for a high severity issue", top_k=3)
    assert len(results) > 0
    assert any("escalation_policy.md" == r["source"] for r in results)


def test_recurring_themes_respects_min_count():
    themes = feedback_synthesis_agent.recurring_themes(window_days=365, min_count=100)
    assert themes == []  # no theme should hit 100 occurrences in this small synthetic dataset
