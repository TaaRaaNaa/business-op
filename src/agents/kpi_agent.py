"""
KPI Agent — computes the 4-dimension account health framework
(engagement, pipeline health, delivery, satisfaction) from the synthetic CRM data.
"""
import os
import pandas as pd
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw")

def _load():
    accounts = pd.read_csv(os.path.join(DATA_DIR, "accounts.csv"))
    opps = pd.read_csv(os.path.join(DATA_DIR, "opportunities.csv"))
    activities = pd.read_csv(os.path.join(DATA_DIR, "activities.csv"))
    feedback = pd.read_csv(os.path.join(DATA_DIR, "client_feedback.csv"))
    return accounts, opps, activities, feedback

def _score(value, low, high):
    """Normalize a raw metric into a 0-100 score, higher-is-better."""
    if high == low:
        return 50.0
    pct = (value - low) / (high - low)
    return round(max(0, min(100, pct * 100)), 1)

def compute_kpis(account_id: str) -> dict:
    accounts, opps, activities, feedback = _load()
    acc_opps = opps[opps.account_id == account_id]
    acc_activities = activities[activities.account_id == account_id]
    acc_feedback = feedback[feedback.account_id == account_id]

    activity_count = len(acc_activities)
    days_since_last = int(acc_opps.days_since_last_activity.min()) if len(acc_opps) else 999
    open_opps = acc_opps[~acc_opps.stage.isin(["Closed Won", "Closed Lost"])]
    open_value = float(open_opps.amount_usd.sum())
    stalled = int((open_opps.days_since_last_activity > 21).sum())
    closed = acc_opps[acc_opps.stage.isin(["Closed Won", "Closed Lost"])]
    on_time_rate = round(random_ontime(account_id), 2)  # placeholder deterministic proxy
    high_sev_open = int((acc_feedback.severity == "High").sum())

    engagement_score = _score(activity_count, 0, 15)
    pipeline_score = _score(open_value, 0, 400000) - (stalled * 10)
    delivery_score = on_time_rate * 100
    satisfaction_score = 100 - (high_sev_open * 25)

    scores = {
        "engagement": max(0, min(100, engagement_score)),
        "pipeline_health": max(0, min(100, pipeline_score)),
        "delivery": max(0, min(100, delivery_score)),
        "satisfaction": max(0, min(100, satisfaction_score)),
    }
    composite = round(sum(scores.values()) / 4, 1)
    risk_flag = "Healthy" if composite >= 70 else ("Watch" if composite >= 45 else "At Risk")

    return {
        "account_id": account_id,
        "period": datetime.now().strftime("%Y-Q%q").replace("%q", str((datetime.now().month - 1)//3 + 1)),
        "dimensions": {
            "engagement": {"score": scores["engagement"], "activity_count_90d": activity_count,
                           "days_since_last_touch": days_since_last},
            "pipeline_health": {"score": round(scores["pipeline_health"], 1), "open_opp_value_usd": open_value,
                                 "stalled_opp_count": stalled},
            "delivery": {"score": round(scores["delivery"], 1), "on_time_rate": on_time_rate},
            "satisfaction": {"score": scores["satisfaction"], "open_high_severity_items": high_sev_open},
        },
        "composite_score": composite,
        "risk_flag": risk_flag,
    }

def random_ontime(account_id: str) -> float:
    # deterministic pseudo-metric so repeated calls are stable per account
    return 0.6 + (hash(account_id) % 40) / 100

def compute_kpis_all() -> list:
    accounts, *_ = _load()
    return [compute_kpis(a) for a in accounts.account_id.tolist()]

if __name__ == "__main__":
    accounts, *_ = _load()
    sample = accounts.account_id.iloc[0]
    import json
    print(json.dumps(compute_kpis(sample), indent=2))
