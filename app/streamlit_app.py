"""
FlexOps Sales & Client Services Operations Copilot
--------------------------------------------------
Executive Streamlit demo for Sales Strategy & Business Operations.

Working capabilities:
1. Account KPI Dashboard
2. Lead Leakage Detection
3. Client Feedback Intelligence
4. RAG-grounded Copilot Q&A

Demo environment:
- Synthetic CRM-style data
- TF-IDF RAG
- AI/agent-oriented workflows
- FastMCP-compatible business tools
"""

import os
import sys

import pandas as pd
import streamlit as st


# -------------------------------------------------------------------
# PATHS
# -------------------------------------------------------------------

BASE_DIR = os.path.dirname(__file__)

sys.path.insert(
    0,
    os.path.join(BASE_DIR, "..", "src", "agents"),
)

sys.path.insert(
    0,
    os.path.join(BASE_DIR, "..", "src", "rag"),
)

sys.path.insert(
    0,
    os.path.join(BASE_DIR, "..", "src", "mcp_server"),
)


# -------------------------------------------------------------------
# PROJECT MODULES
# -------------------------------------------------------------------

import kpi_agent
import lead_leakage_agent
import feedback_synthesis_agent


# -------------------------------------------------------------------
# DATA PATH
# -------------------------------------------------------------------

DATA_DIR = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "raw",
)


# -------------------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------------------

st.set_page_config(
    page_title="FlexOps Sales & Client Services Operations Copilot",
    page_icon="🤖",
    layout="wide",
)


# -------------------------------------------------------------------
# SIMPLE CUSTOM STYLING
# -------------------------------------------------------------------

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    .section-heading {
        font-size: 1.15rem;
        font-weight: 700;
        margin-top: 1.3rem;
        margin-bottom: 0.6rem;
    }

    .footer {
        margin-top: 2.5rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(128,128,128,0.2);
        font-size: 0.78rem;
        opacity: 0.62;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# -------------------------------------------------------------------
# EXECUTIVE SUMMARY
# -------------------------------------------------------------------

summary = lead_leakage_agent.leakage_summary()

open_opps = summary["total_open_opportunities"]
at_risk_count = summary["at_risk_count"]
at_risk_value = summary["at_risk_value_usd"]
leakage_rate = summary["leakage_rate_pct"]


# -------------------------------------------------------------------
# RECRUITER-FACING HEADER
# -------------------------------------------------------------------

st.title(
    "FlexOps Sales & Client Services Operations Copilot"
)

st.subheader(
    "AI-powered operational intelligence for Sales & Client Services teams"
)

st.caption(
    "Interview Portfolio Prototype · "
    "Synthetic CRM data · "
    "RAG · "
    "AI Agents · "
    "MCP"
)


# -------------------------------------------------------------------
# TOP-LEVEL BUSINESS METRICS
# -------------------------------------------------------------------

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric(
        "Open Opportunities",
        f"{open_opps:,}",
    )

with m2:
    st.metric(
        "At Risk",
        f"{at_risk_count:,}",
    )

with m3:
    st.metric(
        "At-Risk Pipeline",
        f"${at_risk_value:,.0f}",
    )

with m4:
    st.metric(
        "Leakage Rate",
        f"{leakage_rate:.1f}%",
    )


# -------------------------------------------------------------------
# WHAT THIS DEMONSTRATES
# -------------------------------------------------------------------

st.markdown(
    '<div class="section-heading">What this demonstrates</div>',
    unsafe_allow_html=True,
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("### 📊 Sales Operations")
    st.caption(
        "Pipeline leakage, account health and operational KPIs."
    )

with c2:
    st.markdown("### 🤖 AI / Copilot")
    st.caption(
        "Agent-oriented workflows for operational decision support."
    )

with c3:
    st.markdown("### 📚 RAG")
    st.caption(
        "Policy-grounded retrieval from the operational knowledge base."
    )

with c4:
    st.markdown("### 🔌 MCP")
    st.caption(
        "Reusable business capabilities exposed as MCP tools."
    )


# -------------------------------------------------------------------
# DEMO DISCLAIMER
# -------------------------------------------------------------------

st.info(
    "Demo environment: synthetic CRM-style data. "
    "No confidential or production customer data is used."
)


# -------------------------------------------------------------------
# NAVIGATION
# -------------------------------------------------------------------

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📊 Account KPIs",
        "⚠️ Lead Leakage",
        "💬 Client Feedback",
        "🤖 Ask the Copilot",
    ]
)


# ===================================================================
# TAB 1 — ACCOUNT KPIs
# ===================================================================

with tab1:

    st.markdown("### Account Health")

    accounts = pd.read_csv(
        os.path.join(
            DATA_DIR,
            "accounts.csv",
        )
    )

    col1, col2 = st.columns([1, 2])

    with col1:

        account_id = st.selectbox(
            "Select account",
            accounts.account_id.tolist(),
        )

    with col2:

        acc_row = accounts[
            accounts.account_id == account_id
        ].iloc[0]

        st.markdown(
            f"""
            **{acc_row.account_name}**

            {acc_row.industry} ·
            {acc_row.region} ·
            {acc_row.tier} tier
            """
        )

    # ---------------------------------------------------------------
    # KPI CALCULATION
    # ---------------------------------------------------------------

    kpis = kpi_agent.compute_kpis(account_id)

    risk_color = {
        "Healthy": "green",
        "Watch": "orange",
        "At Risk": "red",
    }.get(
        kpis["risk_flag"],
        "gray",
    )

    st.markdown(
        f"""
        ### Composite Score: {kpis["composite_score"]}

        :{risk_color}[**{kpis["risk_flag"]}**]
        """
    )

    # ---------------------------------------------------------------
    # KPI DIMENSIONS
    # ---------------------------------------------------------------

    dims = kpis["dimensions"]

    k1, k2, k3, k4 = st.columns(4)

    k1.metric(
        "Engagement",
        dims["engagement"]["score"],
    )

    k2.metric(
        "Pipeline Health",
        dims["pipeline_health"]["score"],
    )

    k3.metric(
        "Delivery",
        dims["delivery"]["score"],
    )

    k4.metric(
        "Satisfaction",
        dims["satisfaction"]["score"],
    )

    # ---------------------------------------------------------------
    # OPERATIONAL INTERPRETATION
    # ---------------------------------------------------------------

    st.markdown("#### Operational interpretation")

    pipeline = dims["pipeline_health"]

    st.write(
        f"""
        **Pipeline:** ${pipeline["open_opp_value_usd"]:,.0f}
        open opportunity value across
        {pipeline["stalled_opp_count"]}
        stalled opportunity record(s).
        """
    )

    # ---------------------------------------------------------------
    # RAW PAYLOAD
    # ---------------------------------------------------------------

    with st.expander(
        "View raw KPI payload returned by the business logic"
    ):

        st.json(kpis)


# ===================================================================
# TAB 2 — LEAD LEAKAGE
# ===================================================================

with tab2:

    st.markdown(
        "### Pipeline Leakage Detection"
    )

    st.caption(
        "Identify open opportunities with insufficient recent "
        "activity and prioritize intervention."
    )

    # ---------------------------------------------------------------
    # LEAKAGE METRICS
    # ---------------------------------------------------------------

    l1, l2, l3, l4 = st.columns(4)

    l1.metric(
        "Open Opportunities",
        f"{summary['total_open_opportunities']:,}",
    )

    l2.metric(
        "At Risk",
        f"{summary['at_risk_count']:,}",
    )

    l3.metric(
        "At-Risk Value",
        f"${summary['at_risk_value_usd']:,.0f}",
    )

    l4.metric(
        "Leakage Rate",
        f"{summary['leakage_rate_pct']:.1f}%",
    )

    # ---------------------------------------------------------------
    # THRESHOLD
    # ---------------------------------------------------------------

    min_days = st.slider(
        "Inactivity threshold",
        min_value=7,
        max_value=60,
        value=21,
        help=(
            "The sales playbook defines 21+ days of inactivity "
            "as the standard leakage threshold for open opportunities."
        ),
    )

    # ---------------------------------------------------------------
    # AT-RISK OPPORTUNITIES
    # ---------------------------------------------------------------

    at_risk = (
        lead_leakage_agent
        .get_at_risk_opportunities(min_days)
    )

    if at_risk:

        st.markdown(
            f"#### {len(at_risk)} opportunities requiring attention"
        )

        st.dataframe(
            pd.DataFrame(at_risk),
            width="stretch",
            hide_index=True,
        )

    else:

        st.success(
            "No opportunities meet the selected inactivity threshold."
        )


# ===================================================================
# TAB 3 — CLIENT FEEDBACK
# ===================================================================

with tab3:

    st.markdown(
        "### Client Feedback Intelligence"
    )

    st.caption(
        "Surface recurring client-service and product themes "
        "for prioritization and escalation."
    )

    # ---------------------------------------------------------------
    # FILTERS
    # ---------------------------------------------------------------

    f1, f2 = st.columns(2)

    with f1:

        window = st.slider(
            "Analysis window (days)",
            min_value=30,
            max_value=180,
            value=90,
        )

    with f2:

        min_count = st.slider(
            "Minimum occurrences",
            min_value=2,
            max_value=10,
            value=3,
        )

    # ---------------------------------------------------------------
    # THEME ANALYSIS
    # ---------------------------------------------------------------

    themes = (
        feedback_synthesis_agent
        .recurring_themes(
            window,
            min_count,
        )
    )

    df = pd.DataFrame(themes)

    if len(df):

        st.dataframe(
            df,
            width="stretch",
            hide_index=True,
        )

        high_sev = df[
            df.severity == "High"
        ]

        if len(high_sev):

            st.warning(
                f"{len(high_sev)} high-severity recurring "
                "theme(s) may require escalation or "
                "cross-functional review."
            )

    else:

        st.info(
            "No themes meet the selected threshold in this window."
        )


# ===================================================================
# TAB 4 — RAG COPILOT
# ===================================================================

with tab4:

    st.markdown(
        "### Ask the Copilot"
    )

    st.caption(
        "Ask a sales, client-service or process question. "
        "The retrieval layer grounds the response in the "
        "operational knowledge base."
    )

    # ---------------------------------------------------------------
    # QUESTION
    # ---------------------------------------------------------------

    question = st.text_input(
        "Your question",
        placeholder=(
            "What should a sales representative do when an "
            "opportunity has had no activity for more than 30 days?"
        ),
    )

    if question:

        result = (
            feedback_synthesis_agent
            .answer_policy_question(question)
        )

        # -----------------------------------------------------------
        # RETRIEVED EVIDENCE
        # -----------------------------------------------------------

        st.markdown(
            "#### Retrieved evidence"
        )

        for chunk in result["retrieved_context"]:

            st.markdown(
                f"**{chunk['source']} — "
                f"{chunk['heading']}**"
            )

            st.caption(
                f"Retrieval similarity score: "
                f"{chunk['score']}"
            )

            st.markdown(
                chunk["text"]
            )

            st.divider()

        # -----------------------------------------------------------
        # OPTIONAL CLAUDE SYNTHESIS
        # -----------------------------------------------------------

        api_key = os.environ.get(
            "ANTHROPIC_API_KEY"
        )

        if api_key:

            try:

                import anthropic

                client = anthropic.Anthropic(
                    api_key=api_key
                )

                context = "\n\n".join(
                    c["text"]
                    for c in result["retrieved_context"]
                )

                prompt_path = os.path.join(
                    BASE_DIR,
                    "..",
                    "prompts",
                    "system_prompt_orchestrator.md",
                )

                with open(
                    prompt_path,
                    encoding="utf-8",
                ) as f:

                    system_prompt = f.read()

                msg = client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=400,
                    system=system_prompt,
                    messages=[
                        {
                            "role": "user",
                            "content": (
                                f"Context:\n{context}\n\n"
                                f"Question: {question}"
                            ),
                        }
                    ],
                )

                answer = "".join(
                    block.text
                    for block in msg.content
                    if block.type == "text"
                )

                st.markdown(
                    "#### Copilot response"
                )

                st.success(
                    answer
                )

            except Exception as e:

                st.error(
                    f"LLM synthesis failed: {e}"
                )

        else:

            st.info(
                "RAG retrieval is active. "
                "Add ANTHROPIC_API_KEY to enable "
                "Claude-generated natural-language synthesis."
            )


# ===================================================================
# FOOTER
# ===================================================================

st.markdown(
    """
    <div class="footer">

        <strong>FlexOps</strong>
        · Interview portfolio prototype
        · Synthetic CRM-style data
        · RAG
        · AI Agents
        · MCP

        <br><br>

        Independent demonstration project.
        Not affiliated with or representative of
        FlexTrade Systems' internal systems,
        data, policies or architecture.

    </div>
    """,
    unsafe_allow_html=True,
)
