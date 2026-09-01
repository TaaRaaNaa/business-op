"""
Standalone tool-call helper for testing the MCP tools without spinning up a
full MCP client -- calls the same underlying functions server.py registers.
Useful for the Streamlit app, which talks to these functions directly rather
than round-tripping through the MCP transport (simpler for a single-process demo).
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "agents"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "rag"))

import kpi_agent
import lead_leakage_agent
import feedback_synthesis_agent

TOOL_REGISTRY = {
    "get_account_kpis": kpi_agent.compute_kpis,
    "list_at_risk_opportunities": lead_leakage_agent.get_at_risk_opportunities,
    "get_leakage_summary": lead_leakage_agent.leakage_summary,
    "get_recurring_feedback_themes": feedback_synthesis_agent.recurring_themes,
    "search_knowledge_base": feedback_synthesis_agent.answer_policy_question,
}

def call_tool(tool_name: str, **kwargs):
    """Mimics the {request, response} envelope defined in tool_call_schema.json."""
    if tool_name not in TOOL_REGISTRY:
        return {"status": "error", "data": None, "error_message": f"Unknown tool: {tool_name}"}
    try:
        result = TOOL_REGISTRY[tool_name](**kwargs)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "data": None, "error_message": str(e)}
