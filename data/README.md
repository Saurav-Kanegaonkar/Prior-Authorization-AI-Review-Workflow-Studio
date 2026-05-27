# Data README

All datasets are deterministic synthetic data for a public portfolio artifact. They do not represent real patients, providers, payer decisions, Medicare cases, clinical documents, utilization management queues, or production model performance.

The synthetic structure is modeled on a prior authorization workflow with intake, document extraction, clinical policy matching, clinical QA, decision support, reviewer feedback, and compliance controls. Randomness is seeded in `scripts/score_operating_data.py` so the outputs are reproducible.

Generated files:

- `authorization_cases.csv`: PHI-free case packets with procedure category, urgency, intake channel, document sufficiency, model confidence, clinical risk, and reviewer effort.
- `pipeline_runs.csv`: stage-level confidence and latency rows for classification, extraction, clinical QA, and decision support.
- `reviewer_feedback.csv`: synthetic reviewer notes used to close the loop with prompt, extraction, policy-index, and intake workflow fixes.
- `analysis/outputs/model_architecture_decisions.csv`: product and ML engineering contract for each model stage, including model choice, prompt contract, output contract, evaluation metric, and human guardrail.
- `analysis/outputs/interoperability_readiness.csv`: FHIR, X12, HL7-style, reviewer workbench, and audit export readiness controls.
