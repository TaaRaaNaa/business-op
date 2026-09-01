# Client Services Escalation Policy (Demo)

## Severity Definitions
- **High**: Production outage, data integrity issue, or client threatening churn. Response SLA: 2 business hours.
- **Medium**: Feature gap, workflow friction, delayed onboarding milestone. Response SLA: 1 business day.
- **Low**: Cosmetic issue, documentation gap, minor feature request. Response SLA: 3 business days.

## Escalation Path
1. Support ticket or QBR note logged in CRM with severity tag.
2. If High severity, CSM notifies Client Services Ops lead immediately.
3. Client Services Ops lead triages: assign to Product (if feature/bug), Engineering (if technical), or Sales (if commercial/pricing).
4. All High-severity items are reviewed in the weekly Client Services Ops sync and tracked to resolution.

## Root Cause Categories
- Product: bugs, missing features, documentation gaps
- Client Services: onboarding delays, support responsiveness, training gaps
- Sales: pricing confusion, expectation mismatch during sales cycle, contract terms

## Automation Note
Recurring themes (3+ similar feedback items in a rolling 90-day window, same category) should be auto-flagged for the roadmap prioritization review.
