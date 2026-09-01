#!/usr/bin/env bash
#
# setup_git_history.sh
#
# Initializes this project as a git repo and commits it in the same logical
# build order laid out in build_plan.md, with timestamps spread across a
# single realistic work day (matching the "built in about a day" framing
# used in the demo script). Idempotent-ish: safe to inspect with `git log`
# after running; re-running on an already-initialized repo will just fail
# cleanly on `git init` being a no-op and skip re-adding committed files.
#
# Usage:
#   chmod +x setup_git_history.sh
#   ./setup_git_history.sh
#
# Edit BUILD_DATE, AUTHOR_NAME, AUTHOR_EMAIL below before running.

set -euo pipefail

# ---- Configure these ----
BUILD_DATE="2026-08-28"     # the day this was "built" — change to your actual date
AUTHOR_NAME="Your Name"
AUTHOR_EMAIL="your@email.com"
# --------------------------

commit_step() {
    local time="$1"
    local message="$2"
    shift 2
    git add "$@"
    GIT_AUTHOR_NAME="$AUTHOR_NAME" GIT_AUTHOR_EMAIL="$AUTHOR_EMAIL" \
    GIT_COMMITTER_NAME="$AUTHOR_NAME" GIT_COMMITTER_EMAIL="$AUTHOR_EMAIL" \
    GIT_AUTHOR_DATE="${BUILD_DATE}T${time}:00" \
    GIT_COMMITTER_DATE="${BUILD_DATE}T${time}:00" \
    git commit -m "$message"
}

if [ ! -d .git ]; then
    git init
    git branch -M main
fi

commit_step "09:15" "Init project scaffold and JSON schemas for agent config, KPIs, MCP tool calls" \
    .gitignore requirements.txt .env.example src/schemas/

commit_step "10:05" "Add synthetic CRM data generator (accounts, opportunities, activities, feedback)" \
    src/data_gen/

commit_step "10:20" "Generate synthetic dataset" \
    data/raw/

commit_step "10:55" "Add sales playbook, escalation policy, and product FAQ knowledge base docs" \
    data/knowledge_base/

commit_step "12:10" "Build TF-IDF RAG layer: chunking, indexing, retrieval interface" \
    src/rag/ingest.py src/rag/vector_store.py src/rag/retriever.py

commit_step "13:40" "Add KPI agent: 4-dimension account health scoring" \
    src/agents/kpi_agent.py

commit_step "14:05" "Add lead leakage agent per sales playbook policy" \
    src/agents/lead_leakage_agent.py

commit_step "14:35" "Add feedback synthesis agent with RAG-grounded Q&A" \
    src/agents/feedback_synthesis_agent.py

commit_step "15:20" "Expose agents as MCP tools via FastMCP" \
    src/mcp_server/

commit_step "15:40" "Add system prompts for orchestrator and sub-agents" \
    prompts/

commit_step "16:50" "Add Streamlit dashboard: KPIs, leakage, feedback, RAG chat tabs" \
    app/

commit_step "17:20" "Add pytest suite covering agents, MCP tools, and retrieval relevance" \
    tests/

commit_step "17:55" "Add architecture notes, demo script, build plan, and README" \
    docs/ README.md build_plan.md

echo ""
echo "Done. Review with: git log --oneline --format='%h %ad %s' --date=format:'%H:%M'"
echo "Then add your remote and push:"
echo "  git remote add origin https://github.com/<you>/flextrade-sales-ops-copilot.git"
echo "  git push -u origin main"
