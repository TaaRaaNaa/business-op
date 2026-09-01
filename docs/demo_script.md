# Demo Script (5–7 minutes)

## 1. Open with the "why" (30 sec)
"I built a small end-to-end system that mirrors this role's AI/Copilot pillar —
agent design, RAG grounding, MCP tool exposure — applied to the same Sales Ops
/ Client Services Ops problem space this role owns. Everything runs on
synthetic data, fully offline, no API key required for the core functionality."

## 2. Show the data model (30 sec)
Open `data/raw/` — accounts, opportunities, activities, client_feedback.
"This mirrors a Salesforce-shaped CRM export — accounts with tiers and ARR,
opportunities moving through stages, activity logs, and client feedback tagged
by severity and category."

## 3. KPI Dashboard tab (1 min)
Pick an account, show the 4-dimension composite score and risk flag.
Expand the raw JSON payload — "this is exactly what the MCP tool
`get_account_kpis` returns, so the same logic powers both the dashboard a
human looks at and an agent that could act on it autonomously."

## 4. Lead Leakage tab (1 min)
Show the leakage summary and at-risk table.
"This encodes an actual policy rule — 21+ days inactive on an open deal — read
straight from the sales playbook, not a hardcoded number in the UI."

## 5. Client Feedback tab (1 min)
Show recurring themes, point out the High-severity ones.
"This implements the escalation policy's auto-flag rule: 3+ similar items in
a 90-day window get surfaced for the roadmap review automatically instead of
someone manually re-reading every ticket."

## 6. RAG chat tab — the centerpiece (1.5 min)
Ask: *"What's the SLA for a High severity escalation?"*
Show the retrieved passage with its similarity score.
"This is the RAG loop — it's not calling an LLM to guess the SLA, it's
retrieving the actual policy passage and grounding the answer in it. If an
API key is set it'll also synthesize a natural-language answer from that
exact context — but the grounding step works with zero dependency on an LLM."

## 7. MCP server (1 min)
Open `src/mcp_server/server.py`. "Every one of these capabilities is also
exposed as an MCP tool via FastMCP — so if we wanted to point Claude Desktop
or a Copilot Studio-equivalent agent at this, it's a stdio or HTTP endpoint
away. Same underlying functions, no duplicated logic."

## 8. Close (30 sec)
"I built this in about a day to demonstrate the pattern, not to claim deep
trading-domain expertise — the point is I can go from a JD's technical
requirements to a working, tested system quickly, and I'd bring that same
speed to standing up FlexTrade's actual Copilot/agent initiatives."

## Anticipated questions
- **"Would this scale to real data volumes?"** — TF-IDF and CSV-based agents
  are demo-appropriate; production would move to a real vector DB and a
  proper CRM data warehouse connection (Snowflake, in my experience).
- **"Why not call Copilot Studio directly?"** — No sandbox access to build
  against; the JSON schema is written so the same agent definition could be
  adapted into that tool's format.
- **"What would you productionize first?"** — Swap TF-IDF for real
  embeddings, add auth to the MCP server, and add the guardrails schema's
  human-approval gate as an actual enforcement point, not just a config field.
