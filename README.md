# FlexOps Sales & Client Services Ops Copilot (Demo)

A small, fully working demo built to speak concretely to the AI/Copilot +
Business/Sales/Client-Services Operations sections of the Manager - Sales
Strategy & Business Operations JD. Synthetic data only; runs offline except
for one optional LLM-synthesis step.

**What it demonstrates:** agent design over real operational data, RAG
grounding against actual policy documents (not hallucinated), structured
JSON configuration in the shape of a low-code agent builder, and the same
logic exposed as MCP tools via FastMCP.

## Project Structure

```
flextrade-sales-ops-copilot/
├── README.md
├── requirements.txt
├── .env.example
├── build_plan.md
├── data/
│   ├── raw/                    # synthetic CRM data (generated)
│   │   ├── accounts.csv
│   │   ├── opportunities.csv
│   │   ├── activities.csv
│   │   └── client_feedback.csv
│   └── knowledge_base/         # RAG source documents
│       ├── sales_playbook.md
│       ├── escalation_policy.md
│       └── product_faq.md
├── src/
│   ├── data_gen/
│   │   └── generate_synthetic_data.py
│   ├── rag/
│   │   ├── ingest.py            # markdown → chunks
│   │   ├── vector_store.py      # TF-IDF index (swappable for embeddings)
│   │   └── retriever.py         # retrieve(query, top_k) interface
│   ├── agents/
│   │   ├── kpi_agent.py                 # 4-dimension account health
│   │   ├── lead_leakage_agent.py        # at-risk pipeline per policy
│   │   └── feedback_synthesis_agent.py  # recurring themes + RAG Q&A
│   ├── mcp_server/
│   │   ├── server.py            # FastMCP server, 5 tools
│   │   └── tools.py             # direct-call helper (used by Streamlit)
│   └── schemas/
│       ├── agent_config_schema.json  # Copilot Studio-shaped agent config
│       ├── kpi_schema.json
│       └── tool_call_schema.json
├── app/
│   └── streamlit_app.py         # 4-tab operational dashboard
├── prompts/
│   ├── system_prompt_orchestrator.md
│   ├── system_prompt_kpi_agent.md
│   └── system_prompt_feedback_agent.md
├── docs/
│   ├── architecture.md          # system diagram + design-decision rationale
│   └── demo_script.md           # 5–7 min walkthrough for the interview
└── tests/
    └── test_mcp_tools.py
```

## Setup

```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Generate synthetic data (already generated, but reproducible)

```bash
python src/data_gen/generate_synthetic_data.py
```

## Build the RAG index

```bash
cd src/rag && python vector_store.py
```

## Run the tests

```bash
pytest tests/ -v
```

## Run the MCP server standalone (stdio, e.g. for Claude Desktop config)

```bash
python src/mcp_server/server.py
```

To add this to Claude Desktop's config:
```json
{
  "mcpServers": {
    "flexops-sales-copilot": {
      "command": "python",
      "args": ["/absolute/path/to/src/mcp_server/server.py"]
    }
  }
}
```

## Run the Streamlit dashboard

```bash
streamlit run app/streamlit_app.py
```

Optionally set `ANTHROPIC_API_KEY` (copy `.env.example` to `.env`) to enable
LLM-synthesized natural-language answers in the "Ask the Copilot" tab —
everything else works without it.

## Why this exists

Built as an interview-prep project for a Manager - Sales Strategy & Business
Operations role that asks for hands-on experience with agentic workflows,
RAG, MCP servers, and JSON-configured agents applied to sales/CS operations.
See `docs/architecture.md` for the design rationale and `docs/demo_script.md`
for a walkthrough script.
