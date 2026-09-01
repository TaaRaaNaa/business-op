"""
Synthetic data generator for the Sales Ops Copilot demo.
Generates realistic-looking (but fully fake) CRM data: accounts, opportunities,
sales activities, and client feedback -- mirroring the shape of data you'd
find in Salesforce for a B2B trading-technology sales org.

No external dependencies (no Faker) so it runs anywhere with just stdlib + pandas.
"""
import random
import csv
import os
from datetime import datetime, timedelta

random.seed(42)

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw")
os.makedirs(OUT_DIR, exist_ok=True)

FIRST_NAMES = ["Alex","Jordan","Priya","Wei","Sofia","Liam","Noor","Carlos","Emma","Raj",
               "Yuki","Mateo","Fatima","Lucas","Anya","Sam","Nina","Omar","Grace","Theo"]
LAST_NAMES = ["Chen","Patel","Novak","Silva","Kim","Rossi","Haddad","Muller","Nguyen","Okafor",
              "Ivanov","Costa","Sato","Reyes","Larsen","Bianchi","Abbas","Duarte","Weiss","Osei"]

INDUSTRIES = ["Hedge Fund","Asset Manager","Broker-Dealer","Prop Trading Firm",
              "Investment Bank","Regional Bank","Pension Fund","Family Office"]

REGIONS = ["Americas","EMEA","APAC"]

PRODUCTS = ["FlexOMS","FlexEMS","FlexAlgo Suite","FlexAnalytics","FlexConnect API"]

STAGES = ["Prospecting","Qualification","Needs Analysis","Proposal Sent",
          "Negotiation","Closed Won","Closed Lost"]

LOSS_REASONS = ["Budget constraints","Chose competitor","Project deprioritized",
                "No decision maker engagement","Timeline mismatch", None, None, None]

ACTIVITY_TYPES = ["Discovery Call","Demo","Follow-up Email","Contract Review",
                   "Technical Deep Dive","Renewal Check-in","Escalation Call"]

FEEDBACK_THEMES = [
    ("Onboarding was slower than expected", "Client Services", "Medium"),
    ("API documentation unclear for FlexConnect", "Product", "High"),
    ("Excellent support response time", "Client Services", "Low"),
    ("Pricing model confusing for multi-asset bundles", "Sales", "Medium"),
    ("Feature request: real-time risk dashboard", "Product", "Low"),
    ("Integration with internal OMS took 3 extra weeks", "Client Services", "High"),
    ("Sales rep was very responsive during eval", "Sales", "Low"),
    ("Renewal negotiation felt rushed", "Sales", "Medium"),
    ("Outage during market open caused client escalation", "Client Services", "High"),
    ("Training materials outdated for latest release", "Product", "Medium"),
]

def rand_date(start_days_ago=730, end_days_ago=0):
    days = random.randint(end_days_ago, start_days_ago)
    return (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

def gen_accounts(n=60):
    rows = []
    for i in range(1, n + 1):
        acc_id = f"ACC-{1000+i}"
        name = f"{random.choice(LAST_NAMES)} {random.choice(INDUSTRIES)}"
        rows.append({
            "account_id": acc_id,
            "account_name": name,
            "industry": random.choice(INDUSTRIES),
            "region": random.choice(REGIONS),
            "tier": random.choices(["Strategic","Enterprise","Mid-Market"], weights=[15,45,40])[0],
            "arr_usd": random.choice([25000,50000,75000,120000,180000,250000,400000,600000]),
            "csm_owner": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
            "created_date": rand_date(1500, 200),
        })
    return rows

def gen_opportunities(accounts, n=140):
    rows = []
    for i in range(1, n + 1):
        acc = random.choice(accounts)
        stage = random.choices(STAGES, weights=[15,15,15,15,10,20,10])[0]
        created = rand_date(400, 30)
        rows.append({
            "opp_id": f"OPP-{2000+i}",
            "account_id": acc["account_id"],
            "product": random.choice(PRODUCTS),
            "stage": stage,
            "amount_usd": random.choice([15000,30000,60000,90000,150000,250000]),
            "owner": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
            "created_date": created,
            "close_date": rand_date(200, -60) if stage in ("Closed Won","Closed Lost") else "",
            "loss_reason": random.choice(LOSS_REASONS) if stage == "Closed Lost" else "",
            "days_since_last_activity": random.randint(0, 45),
        })
    return rows

def gen_activities(opportunities, n=400):
    rows = []
    for i in range(1, n + 1):
        opp = random.choice(opportunities)
        rows.append({
            "activity_id": f"ACT-{5000+i}",
            "opp_id": opp["opp_id"],
            "account_id": opp["account_id"],
            "activity_type": random.choice(ACTIVITY_TYPES),
            "rep": opp["owner"],
            "activity_date": rand_date(180, 0),
            "outcome": random.choice(["Positive","Neutral","No response","Needs follow-up"]),
        })
    return rows

def gen_feedback(accounts, n=90):
    rows = []
    for i in range(1, n + 1):
        acc = random.choice(accounts)
        theme, category, severity = random.choice(FEEDBACK_THEMES)
        rows.append({
            "feedback_id": f"FB-{7000+i}",
            "account_id": acc["account_id"],
            "channel": random.choice(["Support Ticket","QBR Notes","Survey (CSAT)","Renewal Call","Email"]),
            "category": category,
            "severity": severity,
            "theme": theme,
            "feedback_date": rand_date(300, 0),
        })
    return rows

def write_csv(path, rows, fieldnames):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def main():
    accounts = gen_accounts()
    opportunities = gen_opportunities(accounts)
    activities = gen_activities(opportunities)
    feedback = gen_feedback(accounts)

    write_csv(os.path.join(OUT_DIR, "accounts.csv"), accounts, list(accounts[0].keys()))
    write_csv(os.path.join(OUT_DIR, "opportunities.csv"), opportunities, list(opportunities[0].keys()))
    write_csv(os.path.join(OUT_DIR, "activities.csv"), activities, list(activities[0].keys()))
    write_csv(os.path.join(OUT_DIR, "client_feedback.csv"), feedback, list(feedback[0].keys()))

    print(f"Generated {len(accounts)} accounts, {len(opportunities)} opportunities, "
          f"{len(activities)} activities, {len(feedback)} feedback records -> {OUT_DIR}")

if __name__ == "__main__":
    main()
