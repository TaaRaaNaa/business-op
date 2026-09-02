# FlexOps — Sales & Client Operations Copilot

### AI-powered operational intelligence for Sales Strategy, Client Services & GTM teams

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?logo=streamlit\&logoColor=white)](https://flexops-sales-client-ops-copilot.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python\&logoColor=white)](https://www.python.org/)
[![MCP](https://img.shields.io/badge/MCP-FastMCP-purple)](https://modelcontextprotocol.io/)
[![Status](https://img.shields.io/badge/Status-Working%20Prototype-success)](#)

**Live Demo:** https://flexops-sales-client-ops-copilot.streamlit.app/

**Source Code:** https://github.com/TaaRaaNaa/business-op

> **Interview portfolio project** demonstrating how operational data, AI agents, RAG, structured tool interfaces and MCP can be combined to improve Sales Strategy & Business Operations.

---

## 🚀 What Is FlexOps?

FlexOps is a working AI-powered Business Operations prototype designed to sit **on top of existing operational systems** and turn data + organizational knowledge into actionable insights.

It combines:

* CRM-style operational data
* Account health scoring
* Pipeline leakage detection
* Client feedback intelligence
* Policy-grounded RAG
* Agent-oriented workflows
* Structured JSON schemas
* FastMCP tools
* Streamlit executive dashboard

The objective is **not** to replace CRM or BI systems.

The objective is to create an:

> **Intelligence + Context + Action layer on top of operational systems.**

---

# 🚀 Try the Working Demo

## [Launch the Live FlexOps Demo →](https://flexops-sales-client-ops-copilot.streamlit.app/)

The application currently demonstrates four primary business workflows:

| Module                 | Business Question                                   |
| ---------------------- | --------------------------------------------------- |
| 📊 **Account KPIs**    | Which accounts require attention?                   |
| ⚠️ **Lead Leakage**    | Where is pipeline becoming inactive?                |
| 💬 **Client Feedback** | What recurring client issues should be prioritized? |
| 🤖 **Ask the Copilot** | What does the operating policy require?             |

**Demo environment:** Synthetic CRM-style data. No confidential, proprietary or production customer data is used.

---

# 🎯 Executive Value Proposition

Traditional dashboards primarily answer:

> **What happened?**

FlexOps is designed to move toward:

> **What is happening → Why → What does policy say → What should we do next?**

### Example

Instead of:

> "Pipeline is declining."

FlexOps can surface:

> "These opportunities have been inactive for 21+ days, representing $X of exposed pipeline, and the governing sales policy requires notification/escalation."

This connects:

**Operational Data → Business Logic → Knowledge → Evidence → Action**

---

# 1. Business Problem

Sales Strategy & Business Operations teams frequently need to answer questions such as:

* Which opportunities are at risk of leakage?
* How much pipeline value is exposed?
* Which accounts need intervention?
* What client-service issues are recurring?
* Which issues should be escalated?
* What does the governing sales/process policy require?
* Which actions should be prioritized?
* How can these capabilities be made available to AI assistants or agents?

Traditional dashboards provide visibility.

FlexOps is designed to provide **operational intelligence**.

---

# 2. Live Operational Snapshot

The current synthetic dataset demonstrates:

| Metric                 | Current Result |
| ---------------------- | -------------: |
| Open opportunities     |         **93** |
| At-risk opportunities  |         **55** |
| At-risk pipeline value |     **$5.76M** |
| Pipeline leakage rate  |      **59.1%** |

These metrics are calculated dynamically from the underlying operational dataset.

---

# 3. Account Health Intelligence

FlexOps evaluates accounts across multiple operational dimensions:

```text
Engagement
Pipeline Health
Delivery
Satisfaction
```

### Example: Abbas Regional Bank

| Metric                |     Example |
| --------------------- | ----------: |
| ARR                   |   **$400K** |
| Open pipeline         |   **$510K** |
| Active opportunities  |       **5** |
| Stalled opportunities |       **3** |
| Composite KPI         |    **88.2** |
| Risk flag             | **Healthy** |

The operational insight is that an account can remain **Healthy overall** while an individual dimension — such as pipeline health — requires intervention.

This separates:

> **Executive prioritization**

from:

> **Operational diagnosis**

rather than collapsing every issue into a single risk flag.

---

# 4. Pipeline Leakage Detection

The Sales Playbook defines an opportunity as at risk of leakage when:

* No activity has been logged for **21+ days**
* The opportunity remains in an open sales stage

FlexOps identifies affected opportunities and calculates:

* Inactivity duration
* Opportunity value
* Owner
* Product
* Sales stage
* Total exposed pipeline
* Leakage rate

This enables Sales Operations to move from:

**"Pipeline is declining."**

to:

**"These specific opportunities require intervention."**

---

# 5. Client Feedback Intelligence

The feedback workflow identifies recurring themes across client feedback.

Example themes include:

| Theme                              | Function        | Severity | Count |
| ---------------------------------- | --------------- | -------- | ----: |
| Real-time risk dashboard request   | Product         | Low      |     7 |
| OMS integration took 3 extra weeks | Client Services | High     |     6 |
| Onboarding slower than expected    | Client Services | Medium   |     4 |
| Outage during market open          | Client Services | High     |     4 |
| Training materials outdated        | Product         | Medium   |     3 |

This creates a bridge between:

**Client Feedback → Operational Insight → Prioritization**

---

# 6. RAG / Policy Grounding

FlexOps includes a policy-grounded knowledge layer using documents such as:

```text
sales_playbook.md
escalation_policy.md
product_faq.md
```

### Example question

> "What should a sales representative do when an opportunity has had no activity for more than 30 days?"

The user asks about **30 days**, but the governing policy specifies **21+ days**.

Rather than accepting the user's assumption, the system retrieves the relevant policy evidence.

### Example escalation workflow

```text
21+ days inactive
       ↓
Rep notification
       ↓
5 business days without action
       ↓
Regional Sales Ops escalation
```

This demonstrates an important enterprise-AI principle:

> **Ground operational answers in governed organizational knowledge rather than relying solely on an LLM's general knowledge or the user's premise.**

---

# 7. AI / Copilot Layer

The Copilot experience is designed around operational questions rather than generic chatbot interactions.

Example questions include:

```text
Which accounts require attention?

Which opportunities are at risk?

How much pipeline is exposed?

What recurring client issues should we prioritize?

What does the sales policy require?

What should happen when an opportunity becomes inactive?
```

The architecture allows the Copilot to combine:

```text
User Intent
     ↓
Business Logic
     +
Operational Data
     +
Policy / Knowledge
     ↓
Evidence-Based Response
     ↓
Recommended Action
```

---

# 8. MCP / Tool Layer

The operational capabilities are exposed through a **FastMCP server**.

Five tools are currently available:

```text
get_account_kpis
list_at_risk_opportunities
get_leakage_summary
get_recurring_feedback_themes
search_knowledge_base
```

The MCP layer makes the underlying business capabilities reusable by:

* AI agents
* Copilot-style interfaces
* MCP-compatible clients
* Orchestration layers
* Future enterprise workflows
* Other downstream applications

### Live MCP Validation

The implementation has been tested using an MCP client with:

* MCP session initialization
* Streamable HTTP transport
* Tool discovery
* Live tool invocation
* Structured responses

Example validation:

```text
5 tools discovered

✓ get_account_kpis
✓ list_at_risk_opportunities
✓ get_leakage_summary
✓ get_recurring_feedback_themes
✓ search_knowledge_base
```

---

# 9. Architecture

```text
                         USER
                           │
                           ▼
                  ┌─────────────────┐
                  │     COPILOT     │
                  └────────┬────────┘
                           │
                    Intent / Agent
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
      ┌───────────────┐         ┌───────────────┐
      │ Operational   │         │      RAG      │
      │ Data / CRM    │         │ Policy / KB   │
      └───────┬───────┘         └───────┬───────┘
              │                         │
              ▼                         ▼
      ┌───────────────┐         ┌───────────────┐
      │ Business      │         │ Evidence /    │
      │ Analytics     │         │ Retrieval     │
      └───────┬───────┘         └───────┬───────┘
              │                         │
              └────────────┬────────────┘
                           ▼
                  Evidence Synthesis
                           │
                           ▼
                  Recommended Action
                           │
                           ▼
                         MCP
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
        Dashboard       AI Agent    Other Clients
```

### Architectural Principle

The system separates:

```text
Data
  ↓
Business Logic
  ↓
Knowledge
  ↓
Tool Interface
  ↓
User Experience
```

This allows the same underlying business capability to be consumed through different interfaces without duplicating the operational logic.

---

# 10. Technology Stack

## Application

* Python
* Streamlit
* Pandas

## AI / Knowledge

* Retrieval-Augmented Generation (RAG)
* TF-IDF retrieval
* Policy knowledge base
* Agent-oriented workflows
* Optional LLM synthesis

## Integration

* FastMCP
* MCP Streamable HTTP
* JSON schemas
* Structured tool interfaces

## Data

Synthetic Salesforce-shaped operational data:

* Accounts
* Opportunities
* Activities
* Client feedback

## Engineering

* Modular Python architecture
* Automated tests
* Reproducible synthetic data generation
* Structured schemas
* Documentation
* Architecture specification
* Interview demo specification

---

# 11. Project Structure

```text
business-op/
│
├── README.md
├── requirements.txt
├── .env.example
│
├── data/
│   ├── raw/
│   │   ├── accounts.csv
│   │   ├── opportunities.csv
│   │   ├── activities.csv
│   │   └── client_feedback.csv
│   │
│   └── knowledge_base/
│       ├── sales_playbook.md
│       ├── escalation_policy.md
│       └── product_faq.md
│
├── src/
│   ├── agents/
│   │   ├── kpi_agent.py
│   │   ├── lead_leakage_agent.py
│   │   └── feedback_synthesis_agent.py
│   │
│   ├── rag/
│   │   ├── ingest.py
│   │   ├── vector_store.py
│   │   └── retriever.py
│   │
│   ├── mcp_server/
│   │   ├── server.py
│   │   └── tools.py
│   │
│   └── schemas/
│       ├── agent_config_schema.json
│       ├── kpi_schema.json
│       └── tool_call_schema.json
│
├── app/
│   └── streamlit_app.py
│
├── prompts/
│
├── docs/
│   ├── architecture.md
│   └── demo_script.md
│
└── tests/
    └── test_mcp_tools.py
```

---

# 12. Key Design Decisions

## Why synthetic data?

The prototype demonstrates architecture and business reasoning without exposing confidential customer or company information.

## Why RAG?

Policies, escalation rules and product knowledge should be retrieved from governed sources rather than invented by a model.

## Why MCP?

MCP provides a standardized interface through which operational capabilities can be exposed to compatible AI clients and agents.

## Why separate account health from pipeline leakage?

An account can be strategically healthy while containing individual opportunities requiring intervention.

This prevents an executive KPI from masking an operational problem.

## Why expose structured payloads?

Different consumers need different interfaces.

Business users may want:

* dashboards
* summaries
* recommendations

while AI agents and downstream systems may require:

* structured JSON
* schemas
* deterministic tool responses

The same capability should support both.

---

# 13. Governance & Human-in-the-Loop

For a production implementation, AI-generated recommendations should not automatically become irreversible business actions.

A production design could introduce:

```text
AI Recommendation
       ↓
Evidence / Source
       ↓
Confidence
       ↓
Human Approval
       ↓
Action
       ↓
Audit Trail
       ↓
Outcome Measurement
```

This creates a path toward controlled enterprise adoption of AI within business operations.

---

# 14. Production Expansion Opportunities

A production implementation could be extended to:

* Connect directly to Salesforce
* Feed Power BI dashboards
* Monitor pipeline risk continuously
* Trigger human-in-the-loop workflows
* Generate prioritized Sales Ops action lists
* Connect to Microsoft Copilot / Copilot Studio
* Integrate with CRM, CLM, Jira or ServiceNow
* Maintain an audit trail of AI recommendations
* Introduce confidence and evidence scoring
* Measure intervention-to-outcome conversion
* Add role-based access controls
* Add observability and model/tool usage monitoring

The prototype therefore represents an:

> **Operational Intelligence Layer**

rather than a replacement for existing enterprise systems.

---

# 15. Testing & Validation

The project includes automated tests for the core MCP/business-operation tool layer.

The MCP implementation has also been validated through a live MCP client using Streamable HTTP.

Validation included:

1. MCP session initialization
2. Tool discovery
3. Account KPI tool invocation
4. RAG knowledge-base tool invocation
5. Structured response validation

---

# 16. Run Locally

```bash
python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

streamlit run app/streamlit_app.py
```

The application can also be deployed through Streamlit Community Cloud.

---

# 17. Documentation

### Architecture

See:

`docs/architecture.md`

### Interview Demo

See:

`docs/demo_script.md`

### Build Plan

See:

`build_plan.md`

---

# 18. Portfolio Links

## 🚀 Working Demo

**https://flexops-sales-client-ops-copilot.streamlit.app/**

## 💻 GitHub / Technical Implementation

**https://github.com/TaaRaaNaa/business-op**

---

# 19. FlexTrade / Sales Strategy & Business Operations Alignment

This project was intentionally designed around capabilities relevant to a **Sales Strategy & Business Operations** environment.

| Capability            | Project Evidence                                |
| --------------------- | ----------------------------------------------- |
| Sales Operations      | Pipeline leakage analysis                       |
| Business Operations   | Account KPI framework                           |
| Client Services       | Feedback intelligence                           |
| Operational Analytics | Dynamic dashboard                               |
| AI / Copilot          | Copilot interface                               |
| RAG                   | Policy-grounded retrieval                       |
| Agentic Workflows     | KPI, leakage and feedback agents                |
| Context Engineering   | Structured operational + policy context         |
| JSON                  | Structured configuration/tool schemas           |
| MCP                   | Five FastMCP tools                              |
| CRM                   | Salesforce-shaped synthetic dataset             |
| Financial Services    | Trading / financial-services operating scenario |
| Decision Support      | Executive KPIs + drill-down                     |
| Governance            | Evidence grounding + human-in-the-loop design   |

### Why this matters

The project demonstrates the ability to connect:

**Business Problem → Data → Analytics → AI → Governance → Action**

rather than treating AI as a standalone chatbot.

---

# 20. Skills Demonstrated

### Business

* Sales Strategy
* Sales Operations
* Client Services Operations
* GTM Operations
* Business Analysis
* Executive Decision Support
* Operational Problem Solving
* Process Design

### Data & Analytics

* KPI Design
* Pipeline Analytics
* Risk Identification
* Data Modeling
* Operational Dashboards
* Feedback Analysis
* Synthetic Data Design

### AI

* RAG
* AI Agents
* Copilot Workflows
* Context Engineering
* Policy Grounding
* Evidence-Based Responses
* Human-in-the-Loop AI

### Technical

* Python
* Streamlit
* Pandas
* FastMCP
* MCP
* JSON Schemas
* Modular Architecture
* API / Tool Interfaces
* Automated Testing

---

# 21. Interview Talking Points

This project can be used to demonstrate several senior-level discussion areas.

### Business Question

> How can Sales Operations move from dashboard visibility to proactive intervention?

### Architecture Question

> How would you separate business logic, retrieval, agent orchestration and user experience?

### AI Question

> How do you prevent an AI system from inventing organizational policy?

### MCP Question

> Why expose business capabilities through MCP instead of embedding everything inside the UI?

### Governance Question

> How should AI recommendations be controlled before becoming business actions?

### Scaling Question

> How would you move this prototype from synthetic data to Salesforce and enterprise systems?

### Product Question

> What metrics would you use to prove that FlexOps actually improves Sales Operations?

---

# 22. Future Product Metrics

A production implementation could measure:

| Metric                         | Purpose                         |
| ------------------------------ | ------------------------------- |
| Pipeline recovered             | Financial impact                |
| At-risk opportunities actioned | Operational adoption            |
| Time-to-intervention           | Responsiveness                  |
| False-positive rate            | Recommendation quality          |
| Recommendation acceptance rate | User trust                      |
| Escalation resolution time     | Process effectiveness           |
| Client issue recurrence        | Service improvement             |
| AI-assisted resolution rate    | Automation impact               |
| Evidence coverage              | Governance                      |
| Human override rate            | Human-in-the-loop effectiveness |

---

# 23. Disclaimer

This is an independent interview / portfolio prototype.

It uses synthetic data and is **not affiliated with, endorsed by, or representative of FlexTrade Systems or its internal systems, data, policies or architecture**.

The purpose is to demonstrate practical thinking across:

* Business Operations
* Sales Strategy
* Analytics
* AI
* RAG
* Agentic Workflows
* MCP
* Context Engineering
* Governance
* Executive Decision Support

---

# 👤 Author

## Tarana Chawla

**Business & Technology | GTM | Operations | AI-enabled Transformation**

9+ years across technology, consulting, business analysis, cloud / technology operations, program management and go-to-market strategy.

**Portfolio:** https://taaraanaa.github.io/

**GitHub:** https://github.com/TaaRaaNaa

---

## ⭐ If you're reviewing this project

Start here:

**1. Launch the live demo**

https://flexops-sales-client-ops-copilot.streamlit.app/

**2. Review the architecture**

`docs/architecture.md`

**3. Review the MCP implementation**

`src/mcp_server/`

**4. Review the RAG implementation**

`src/rag/`

**5. Review the business agents**

`src/agents/`

**6. Review the automated tests**

`tests/`

---

### Project Status

**🟢 Working Portfolio Prototype**

The current implementation demonstrates the core operational intelligence, RAG, agent-oriented workflows, structured tool interfaces, MCP integration and executive dashboard experience described above.
