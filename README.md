# Prior Authorization AI Review Workflow Studio

I built this because healthcare AI prior authorization, document extraction, and human review workflow design needs more than a dashboard: it needs a decision artifact that connects source data, analysis, and next actions.

![Prior Authorization AI Review Workflow Studio](docs/images/dashboard.png)

## What this project is

This project is a ops for healthcare AI prior authorization, document extraction, and human review workflow design. It uses synthetic but workflow-shaped data to rank authorization case-level risks and convert the output into stakeholder-ready recommendations.

## Data sources

- `entities.csv` - 36 authorization case records
- `daily_metrics.csv` - 5,040 daily operating rows
- `source_events.csv` - 760 event, exception, QA, and stakeholder-request records
- `recommended_actions.csv` - 220 action candidates

## Analysis outputs

- `analysis/executive_findings.md`
- `analysis/analysis_plan.md`
- `analysis/sql_checks.sql`
- `analysis/outputs/priority_queue.csv`

## Recommendation

Use the priority queue to focus stakeholder attention on the authorization case segments where performance upside, measurement risk, and operational readiness overlap.

## Run locally

```bash
python3 -m http.server 4173
```
