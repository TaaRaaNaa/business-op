# 1-Day Build Plan

Realistic solo-build schedule if you were building this from scratch in a day
(this version was pre-built for you, but this is the plan to be able to
speak to *how* you'd build it under time pressure — likely to come up).

| Time | Block | Output |
|---|---|---|
| 9:00–9:30 | Scope & schema first | Decide the 3–4 tools/agents up front; write JSON schemas before code so everything downstream has a contract |
| 9:30–10:30 | Synthetic data generator | accounts/opportunities/activities/feedback CSVs — deterministic seed so demo numbers are stable |
| 10:30–11:00 | Knowledge base docs | 3 short markdown policy docs the RAG layer will index |
| 11:00–12:30 | RAG layer | chunking → TF-IDF index → retriever, tested standalone before wiring into agents |
| 12:30–13:00 | Lunch / buffer | — |
| 13:00–14:30 | Agents | kpi_agent, lead_leakage_agent, feedback_synthesis_agent — pure functions, testable in isolation |
| 14:30–15:30 | MCP server | FastMCP wrapping the same agent functions as tools; smoke test each tool call |
| 15:30–17:00 | Streamlit UI | 4 tabs wired to the agent functions directly |
| 17:00–17:30 | Tests | pytest covering each tool + retriever relevance |
| 17:30–18:00 | README + demo script | So the project is self-explanatory without you narrating every file |

## What to cut first if time runs short
1. Streamlit polish (metrics/tables are enough — skip styling)
2. The Anthropic API synthesis step in the RAG tab (retrieval-only still demos the concept)
3. Guardrails fields in the JSON schema (nice-to-have, not core to the demo)

## What NOT to cut
- The MCP server (it's the most directly JD-relevant artifact)
- At least one passing test suite (shows engineering discipline, not just a script)
- The architecture.md "why" section (interviewers will ask *why*, not just *what*)
