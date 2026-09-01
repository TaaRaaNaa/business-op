"""
Lead Leakage Agent — flags opportunities at risk per the sales playbook policy:
open stage + no activity in 21+ days.
"""
import os
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw")
OPEN_STAGES = {"Prospecting", "Qualification", "Needs Analysis", "Proposal Sent", "Negotiation"}

def get_at_risk_opportunities(min_days_inactive: int = 21) -> list:
    opps = pd.read_csv(os.path.join(DATA_DIR, "opportunities.csv"))
    accounts = pd.read_csv(os.path.join(DATA_DIR, "accounts.csv"))
    at_risk = opps[
        opps.stage.isin(OPEN_STAGES) & (opps.days_since_last_activity >= min_days_inactive)
    ].merge(accounts[["account_id", "account_name", "tier"]], on="account_id", how="left")
    at_risk = at_risk.sort_values("amount_usd", ascending=False)
    return at_risk[[
        "opp_id", "account_name", "tier", "product", "stage",
        "amount_usd", "days_since_last_activity", "owner"
    ]].to_dict(orient="records")

def leakage_summary() -> dict:
    opps = pd.read_csv(os.path.join(DATA_DIR, "opportunities.csv"))
    open_opps = opps[opps.stage.isin(OPEN_STAGES)]
    at_risk = open_opps[open_opps.days_since_last_activity >= 21]
    return {
        "total_open_opportunities": int(len(open_opps)),
        "at_risk_count": int(len(at_risk)),
        "at_risk_value_usd": float(at_risk.amount_usd.sum()),
        "leakage_rate_pct": round(100 * len(at_risk) / max(1, len(open_opps)), 1),
    }

if __name__ == "__main__":
    import json
    print(json.dumps(leakage_summary(), indent=2))
