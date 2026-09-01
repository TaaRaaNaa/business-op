"""
FlexOps Sales Ops MCP Server (FastMCP)

Exposes the sales/CS operations agents as MCP tools so any MCP-compatible
client (Claude Desktop, Claude Cowork, a custom orchestrator, etc.) can call
them directly. This mirrors what the JD calls for: "practical experience in
building MCP servers using frameworks like FastMCP."

Run:
    python server.py                # stdio transport (for Claude Desktop config)
    python server.py --http          # streamable-http transport (for local testing)
"""
import sys
import os
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "agents"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "rag"))

from mcp.server.fastmcp import FastMCP
import kpi_agent
import lead_leakage_agent
import feedback_synthesis_agent

mcp = FastMCP("flexops-sales-copilot")


@mcp.tool()
def get_account_kpis(account_id: str) -> dict:
    """Compute the 4-dimension KPI framework (engagement, pipeline health,
    delivery, satisfaction) for a given account_id, returning a composite
    score and risk flag (Healthy / Watch / At Risk)."""
    return kpi_agent.compute_kpis(account_id)


@mcp.tool()
def list_at_risk_opportunities(min_days_inactive: int = 21) -> list:
    """List open opportunities with no logged activity in `min_days_inactive`
    days or more, per the lead leakage policy in the sales playbook. Sorted
    by deal size descending."""
    return lead_leakage_agent.get_at_risk_opportunities(min_days_inactive)


@mcp.tool()
def get_leakage_summary() -> dict:
    """Return a summary of pipeline leakage: total open opportunities,
    at-risk count, at-risk dollar value, and leakage rate percentage."""
    return lead_leakage_agent.leakage_summary()


@mcp.tool()
def get_recurring_feedback_themes(window_days: int = 90, min_count: int = 3) -> list:
    """Surface client feedback themes that recur 3+ times within a rolling
    window (default 90 days), per the escalation policy's auto-flag rule for
    roadmap prioritization review."""
    return feedback_synthesis_agent.recurring_themes(window_days, min_count)


@mcp.tool()
def search_knowledge_base(question: str, top_k: int = 3) -> dict:
    """RAG-search the sales playbook, escalation policy, and product FAQ for
    context relevant to a natural-language question. Returns the top-k
    grounding passages with source and similarity score."""
    return feedback_synthesis_agent.answer_policy_question(question, top_k)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--http", action="store_true", help="Run with streamable-http transport instead of stdio")
    args = parser.parse_args()
    if args.http:
        mcp.run(transport="streamable-http")
    else:
        mcp.run()
