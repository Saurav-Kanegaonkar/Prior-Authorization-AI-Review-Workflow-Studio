# Data Dictionary

| Table | Grain | Purpose |
|---|---|---|
| `data/authorization_cases.csv` | Prior authorization case | Synthetic case packet with procedure, specialty, urgency, intake channel, document sufficiency, model confidence, clinical risk, reviewer effort, SLA pressure, and recommendation. |
| `data/pipeline_runs.csv` | Case by pipeline stage | Stage-level confidence, threshold, status, and latency for classification, document extraction, clinical QA, and decision support. |
| `data/reviewer_feedback.csv` | Reviewer feedback item | Synthetic reviewer note used to prioritize prompt, extraction, policy-index, and intake workflow remediation. |
| `analysis/outputs/threshold_scenarios.csv` | Threshold scenario | Conservative, balanced, and aggressive threshold settings with automation, review, escalation, reviewer hours, and guardrail outcomes. |
| `analysis/outputs/clinical_review_queue.csv` | Prioritized case | Reviewer worklist scored by confidence gap, missing evidence, clinical risk, SLA pressure, and reviewer effort. |
| `analysis/outputs/feedback_loop_queue.csv` | Feedback theme | Aggregated reviewer feedback with affected cases, severity mix, owner, action, and priority score. |
| `analysis/outputs/compliance_readiness.csv` | Product control | Product behavior mapped to CMS clock handling, human review guardrails, interoperability readiness, audit trace completeness, and documentation sufficiency. |
| `analysis/outputs/pipeline_summary.json` | App payload | JSON payload used by the static app to render all interactive surfaces. |
