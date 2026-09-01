"""
FlexOps Sales Ops Copilot -- Streamlit demo UI.

Four tabs:
1. Account KPI Dashboard  -- 4-dimension health scores per account
2. Lead Leakage           -- at-risk pipeline per the sales playbook policy
3. Client Feedback        -- recurring themes for roadmap prioritization
4. Ask the Copilot        -- RAG-grounded Q&A over the policy knowledge base
                              (optionally synthesized by Claude if an API key is set)

Run: streamlit run app/streamlit_app.py
"""
import os
import sys
import json
import pandas as pd
import streamlit as st

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "agents"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "rag"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "mcp_server"))

import kpi_agent
import lead_leakage_agent
import feedback_synthesis_agent

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")

st.set_page_config(page_title="FlexOps Sales Ops Copilot", layout="wide")
st.title("FlexOps Sales & Client Services Ops Copilot")
st.caption("Demo project · synthetic data · TF-IDF RAG · MCP-exposed agent tools")

tab1, tab2, tab3, tab4 = st.tabs(
    ["📊 Account KPIs", "⚠️ Lead Leakage", "💬 Client Feedback", "🤖 Ask the Copilot"]
)

# ---------- Tab 1: KPIs ----------
with tab1:
    accounts = pd.read_csv(os.path.join(DATA_DIR, "accounts.csv"))
    col1, col2 = st.columns([1, 2])
    with col1:
        account_id = st.selectbox("Account", accounts.account_id.tolist())
    with col2:
        acc_row = accounts[accounts.account_id == account_id].iloc[0]
        st.markdown(f"**{acc_row.account_name}** · {acc_row.industry} · {acc_row.region} · {acc_row.tier} tier")

    kpis = kpi_agent.compute_kpis(account_id)
    risk_color = {"Healthy": "green", "Watch": "orange", "At Risk": "red"}[kpis["risk_flag"]]
    st.markdown(f"### Composite score: {kpis['composite_score']} — :{risk_color}[{kpis['risk_flag']}]")

    dims = kpis["dimensions"]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Engagement", dims["engagement"]["score"])
    c2.metric("Pipeline Health", dims["pipeline_health"]["score"])
    c3.metric("Delivery", dims["delivery"]["score"])
    c4.metric("Satisfaction", dims["satisfaction"]["score"])

    with st.expander("Raw KPI payload (what the MCP tool returns)"):
        st.json(kpis)

# ---------- Tab 2: Lead Leakage ----------
with tab2:
    summary = lead_leakage_agent.leakage_summary()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Open Opportunities", summary["total_open_opportunities"])
    c2.metric("At Risk", summary["at_risk_count"])
    c3.metric("At-Risk Value", f"${summary['at_risk_value_usd']:,.0f}")
    c4.metric("Leakage Rate", f"{summary['leakage_rate_pct']}%")

    min_days = st.slider("Flag threshold (days since last activity)", 7, 60, 21)
    at_risk = lead_leakage_agent.get_at_risk_opportunities(min_days)
    st.dataframe(pd.DataFrame(at_risk), use_container_width=True)

# ---------- Tab 3: Feedback ----------
with tab3:
    window = st.slider("Window (days)", 30, 180, 90)
    min_count = st.slider("Minimum occurrences to flag", 2, 10, 3)
    themes = feedback_synthesis_agent.recurring_themes(window, min_count)
    df = pd.DataFrame(themes)
    if len(df):
        st.dataframe(df, use_container_width=True)
        high_sev = df[df.severity == "High"]
        if len(high_sev):
            st.warning(f"{len(high_sev)} High-severity recurring theme(s) — escalate per policy.")
    else:
        st.info("No themes meet the threshold in this window.")

# ---------- Tab 4: RAG Q&A ----------
with tab4:
    st.markdown("Ask a policy or process question. Answers are grounded in "
                "`sales_playbook.md`, `escalation_policy.md`, and `product_faq.md`.")
    question = st.text_input("Your question", placeholder="What's the SLA for a High severity escalation?")
    if question:
        result = feedback_synthesis_agent.answer_policy_question(question)
        for chunk in result["retrieved_context"]:
            st.markdown(f"**{chunk['source']} — {chunk['heading']}**  (score: {chunk['score']})")
            st.markdown(chunk["text"])
            st.divider()

        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if api_key:
            try:
                import anthropic
                client = anthropic.Anthropic(api_key=api_key)
                context = "\n\n".join(c["text"] for c in result["retrieved_context"])
                with open(os.path.join(os.path.dirname(__file__), "..", "prompts",
                                        "system_prompt_orchestrator.md")) as f:
                    system_prompt = f.read()
                msg = client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=400,
                    system=system_prompt,
                    messages=[{"role": "user", "content":
                        f"Context:\n{context}\n\nQuestion: {question}"}],
                )
                answer = "".join(b.text for b in msg.content if b.type == "text")
                st.success(answer)
            except Exception as e:
                st.error(f"LLM synthesis failed: {e}")
        else:
            st.info("Set ANTHROPIC_API_KEY to have Claude synthesize a natural-language "
                     "answer from the passages above. Retrieval works without a key.")
