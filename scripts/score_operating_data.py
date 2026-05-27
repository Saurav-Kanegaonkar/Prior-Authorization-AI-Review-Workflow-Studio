import csv
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "analysis" / "outputs"
ANALYSIS_DIR = ROOT / "analysis"
SRC_DIR = ROOT / "src"

random.seed(57)

PROCEDURES = [
    ("Skin substitute", "wound care", 0.78, 0.84, 34),
    ("Spinal cord stimulator", "pain management", 0.72, 0.79, 48),
    ("Knee arthroscopy", "orthopedics", 0.76, 0.81, 31),
    ("Sleep study", "sleep medicine", 0.88, 0.9, 18),
    ("Home infusion", "pharmacy", 0.84, 0.86, 26),
    ("Advanced imaging", "radiology", 0.9, 0.91, 16),
    ("DME oxygen", "durable medical equipment", 0.82, 0.83, 29),
    ("Genetic test", "laboratory", 0.7, 0.77, 42),
]

DOCUMENT_TYPES = [
    "order",
    "clinical_note",
    "diagnosis_history",
    "conservative_therapy",
    "test_result",
    "payer_policy",
]

FEEDBACK_THEMES = [
    "Missing conservative therapy duration",
    "Extracted diagnosis needs citation",
    "Policy version mismatch",
    "Ambiguous urgency signal",
    "Rationale needs patient-specific language",
    "Duplicate document packet",
]

OWNER_MAP = {
    "Missing conservative therapy duration": "Document AI",
    "Extracted diagnosis needs citation": "Extraction prompt",
    "Policy version mismatch": "Clinical policy ops",
    "Ambiguous urgency signal": "Classifier prompt",
    "Rationale needs patient-specific language": "Clinical QA",
    "Duplicate document packet": "Intake workflow",
}

MODEL_ARCHITECTURE = [
    {
        "stage": "Intake classification",
        "model_choice": "Small supervised classifier plus LLM fallback",
        "prompt_contract": "Classify request type, urgency, channel, and specialty with no clinical determination.",
        "input_signals": "Procedure text, CPT family, diagnosis text, channel metadata, urgency language",
        "output_contract": "Specialty, urgency, request class, confidence, and reason codes",
        "human_guardrail": "Urgency conflicts and low confidence route to clinical QA before clock assignment.",
        "eval_metric": "Macro F1 and urgency false-negative rate",
        "deploy_note": "Runs first so every downstream agent receives the same case envelope.",
    },
    {
        "stage": "Document extraction",
        "model_choice": "OCR plus document AI extractor",
        "prompt_contract": "Extract dated evidence, source page, diagnosis, therapy history, and test results.",
        "input_signals": "PDF pages, fax packets, CCDA sections, portal attachments, duplicate-page score",
        "output_contract": "Structured evidence table with citation anchors and missing-field flags",
        "human_guardrail": "No generated evidence can enter the rationale unless it has a source citation.",
        "eval_metric": "Field-level F1, citation coverage, and duplicate-page precision",
        "deploy_note": "Keeps reviewer trust high by showing where each evidence claim came from.",
    },
    {
        "stage": "Policy retrieval",
        "model_choice": "RAG over active medical necessity policy index",
        "prompt_contract": "Retrieve active criteria only, reject expired policy clauses, and quote criterion text.",
        "input_signals": "Specialty, procedure, payer policy date, diagnosis, requested site of service",
        "output_contract": "Policy criteria, version date, source citation, and retrieval confidence",
        "human_guardrail": "Version mismatch blocks automation and creates a policy-ops work item.",
        "eval_metric": "Top-k policy recall and active-version accuracy",
        "deploy_note": "Separates policy lookup from clinical reasoning so updates are auditable.",
    },
    {
        "stage": "Clinical QA reasoning",
        "model_choice": "Large language model with criteria-by-criteria rubric",
        "prompt_contract": "Compare extracted evidence to each criterion and mark met, unmet, or unknown.",
        "input_signals": "Evidence table, retrieved criteria, contraindication flags, reviewer rubric",
        "output_contract": "Criterion findings, uncertainty notes, rationale draft, and escalation reason",
        "human_guardrail": "Any unmet or unknown criterion routes to licensed clinical review.",
        "eval_metric": "Reviewer agreement, unsupported-claim rate, and rationale completeness",
        "deploy_note": "Designed for decision support only, with no automated adverse determination.",
    },
    {
        "stage": "Decision release",
        "model_choice": "Rules engine plus audit ledger",
        "prompt_contract": "Apply threshold policy and generate release packet only for eligible affirmations.",
        "input_signals": "Stage confidences, evidence sufficiency, clinical risk, SLA clock, reviewer action",
        "output_contract": "Route, reviewer task, denial-reason requirement, audit snapshot, and API response state",
        "human_guardrail": "Auto-affirm only when all gates pass and no non-coverage path is present.",
        "eval_metric": "Unsafe automation blocks, turnaround compliance, and audit completeness",
        "deploy_note": "Makes probabilistic output operational by binding scores to product behavior.",
    },
]

INTEROPERABILITY_CONTROLS = [
    {
        "interface": "FHIR Prior Authorization API",
        "status": "Design ready",
        "required_behavior": "Receive request, expose documentation requirements, return approval, denial reason, or more information.",
        "product_decision": "Map every case packet to a normalized request state and response status.",
        "risk": "Missing source-channel lineage makes API responses hard to audit.",
    },
    {
        "interface": "X12 278 and 275",
        "status": "Design ready",
        "required_behavior": "Support EDI prior authorization request and attachment workflows where trading partners require them.",
        "product_decision": "Preserve EDI transaction IDs beside normalized FHIR-style case identifiers.",
        "risk": "Attachment gaps can create false missing-document tasks.",
    },
    {
        "interface": "HL7 v2, C-CDA, and PDF intake",
        "status": "Needs validation",
        "required_behavior": "Turn clinical notes, observations, orders, and scanned packets into reviewer-ready evidence.",
        "product_decision": "Run duplicate-page detection and citation extraction before clinical QA.",
        "risk": "OCR quality and document order can distort evidence sufficiency.",
    },
    {
        "interface": "Reviewer workbench",
        "status": "Design ready",
        "required_behavior": "Show model confidence, cited evidence, policy version, SLA clock, route, and reviewer action.",
        "product_decision": "Keep model uncertainty visible instead of hiding it behind a single recommendation.",
        "risk": "Reviewers may override without structured feedback unless the action form is constrained.",
    },
    {
        "interface": "Audit and metrics export",
        "status": "Needs validation",
        "required_behavior": "Publish turnaround, approval, denial, more-information, and decision reason metrics.",
        "product_decision": "Log every route change with threshold policy, user, timestamp, and rationale snapshot.",
        "risk": "Incomplete audit fields weaken compliance reporting and root-cause analysis.",
    },
]


def clamp(value, low, high):
    return max(low, min(high, value))


def pct(value):
    return round(value * 100, 1)


def write_csv(path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def confidence(base, spread=0.08):
    return round(clamp(random.gauss(base, spread), 0.45, 0.99), 3)


def create_cases():
    cases = []
    for idx in range(1, 49):
        procedure, specialty, classifier_base, policy_base, reviewer_base = random.choice(PROCEDURES)
        urgency = random.choices(["Standard", "Expedited"], weights=[72, 28])[0]
        channel = random.choices(["FHIR API", "Portal upload", "Fax conversion", "X12 278"], weights=[32, 38, 17, 13])[0]
        packet_quality = random.choices(["Complete", "Partial", "Sparse", "Conflicting"], weights=[58, 25, 10, 7])[0]
        missing_count = {
            "Complete": 0,
            "Partial": random.choice([1, 1, 2]),
            "Sparse": random.choice([2, 3]),
            "Conflicting": random.choice([1, 2]),
        }[packet_quality]
        missing_docs = random.sample(DOCUMENT_TYPES, missing_count)
        hours_allowed = 72 if urgency == "Expedited" else 168
        elapsed_hours = random.randint(6, hours_allowed + 18)
        sla_remaining_hours = hours_allowed - elapsed_hours
        classifier_confidence = confidence(classifier_base, 0.09)
        extraction_f1 = confidence(0.86 - missing_count * 0.055, 0.07)
        policy_match_confidence = confidence(policy_base - (0.04 if packet_quality == "Conflicting" else 0), 0.08)
        evidence_sufficiency = confidence(0.9 - missing_count * 0.08 - (0.06 if packet_quality == "Conflicting" else 0), 0.07)
        rationale_completeness = confidence(0.84 - missing_count * 0.045, 0.08)
        clinical_risk = random.choices(["Low", "Medium", "High"], weights=[43, 39, 18])[0]
        if clinical_risk == "High":
            reviewer_base += 14
            evidence_sufficiency = round(max(0.5, evidence_sufficiency - 0.07), 3)
        if sla_remaining_hours < 12:
            reviewer_base += 8
        reviewer_minutes = max(8, int(random.gauss(reviewer_base, 7)))
        recommendation = choose_recommendation(
            evidence_sufficiency,
            policy_match_confidence,
            missing_count,
            clinical_risk,
        )
        cases.append(
            {
                "case_id": f"PA-{idx:04d}",
                "procedure": procedure,
                "specialty": specialty,
                "urgency": urgency,
                "intake_channel": channel,
                "packet_quality": packet_quality,
                "missing_documents": "; ".join(missing_docs) if missing_docs else "none",
                "classifier_confidence": classifier_confidence,
                "extraction_f1": extraction_f1,
                "policy_match_confidence": policy_match_confidence,
                "evidence_sufficiency": evidence_sufficiency,
                "rationale_completeness": rationale_completeness,
                "clinical_risk": clinical_risk,
                "reviewer_minutes": reviewer_minutes,
                "sla_remaining_hours": sla_remaining_hours,
                "model_recommendation": recommendation,
            }
        )
    return cases


def choose_recommendation(evidence, policy, missing_count, clinical_risk):
    if missing_count >= 2:
        return "Request more information"
    if clinical_risk == "High" and policy < 0.82:
        return "Escalate to clinician"
    if evidence >= 0.84 and policy >= 0.84:
        return "Affirm coverage criteria met"
    if evidence < 0.72 or policy < 0.72:
        return "Potential non-coverage, clinician required"
    return "Clinical review required"


def route_case(case, thresholds):
    min_model_conf = min(
        float(case["classifier_confidence"]),
        float(case["extraction_f1"]),
        float(case["policy_match_confidence"]),
        float(case["evidence_sufficiency"]),
    )
    missing_docs = case["missing_documents"] != "none"
    sla_risk = int(case["sla_remaining_hours"]) < (10 if case["urgency"] == "Expedited" else 24)
    high_risk = case["clinical_risk"] == "High"
    recommendation = case["model_recommendation"]

    threshold_pass = (
        float(case["classifier_confidence"]) >= thresholds["classifier"]
        and float(case["extraction_f1"]) >= thresholds["extraction"]
        and float(case["policy_match_confidence"]) >= thresholds["policy"]
        and float(case["evidence_sufficiency"]) >= thresholds["evidence"]
    )
    auto_affirm_candidate = (
        recommendation == "Affirm coverage criteria met"
        and threshold_pass
        and not missing_docs
        and not high_risk
    )

    if auto_affirm_candidate:
        route = "Auto-affirm with audit trace"
        escalation_reason = "Meets all confidence and evidence gates"
    elif missing_docs:
        route = "Request missing documentation"
        escalation_reason = f"Missing {case['missing_documents']}"
    elif high_risk or "Potential non-coverage" in recommendation:
        route = "Escalate to licensed clinician"
        escalation_reason = "Clinical risk or possible adverse determination"
    elif sla_risk:
        route = "Expedite reviewer queue"
        escalation_reason = "CMS clock risk"
    elif min_model_conf < thresholds["evidence"]:
        route = "Clinical QA review"
        escalation_reason = "Low confidence in one or more pipeline stages"
    else:
        route = "Clinical QA review"
        escalation_reason = "Reviewer validation before decision release"

    unsafe_auto_blocked = (
        threshold_pass
        and recommendation != "Affirm coverage criteria met"
        and (high_risk or "Potential non-coverage" in recommendation)
    )
    return route, escalation_reason, unsafe_auto_blocked


def create_threshold_scenarios(cases):
    scenarios = {
        "Conservative": {"classifier": 0.9, "extraction": 0.88, "policy": 0.9, "evidence": 0.88},
        "Balanced": {"classifier": 0.8, "extraction": 0.78, "policy": 0.8, "evidence": 0.78},
        "Aggressive": {"classifier": 0.77, "extraction": 0.76, "policy": 0.78, "evidence": 0.76},
    }
    rows = []
    for name, thresholds in scenarios.items():
        route_counts = Counter()
        reviewer_minutes = 0
        unsafe_blocked = 0
        for case in cases:
            route, _, blocked = route_case(case, thresholds)
            route_counts[route] += 1
            if route != "Auto-affirm with audit trace":
                reviewer_minutes += int(case["reviewer_minutes"])
            unsafe_blocked += int(blocked)
        rows.append(
            {
                "scenario": name,
                "classifier_threshold": thresholds["classifier"],
                "extraction_threshold": thresholds["extraction"],
                "policy_threshold": thresholds["policy"],
                "evidence_threshold": thresholds["evidence"],
                "auto_affirm_cases": route_counts["Auto-affirm with audit trace"],
                "clinical_review_cases": route_counts["Clinical QA review"],
                "clinician_escalations": route_counts["Escalate to licensed clinician"],
                "missing_doc_requests": route_counts["Request missing documentation"],
                "expedited_queue_cases": route_counts["Expedite reviewer queue"],
                "reviewer_hours": round(reviewer_minutes / 60, 1),
                "unsafe_auto_decisions_blocked": unsafe_blocked,
            }
        )
    return rows


def create_review_queue(cases):
    thresholds = {"classifier": 0.84, "extraction": 0.82, "policy": 0.84, "evidence": 0.82}
    queue = []
    for case in cases:
        route, escalation_reason, blocked = route_case(case, thresholds)
        sla_pressure = max(0, 36 - int(case["sla_remaining_hours"]))
        confidence_gap = max(
            0,
            thresholds["classifier"] - float(case["classifier_confidence"]),
            thresholds["extraction"] - float(case["extraction_f1"]),
            thresholds["policy"] - float(case["policy_match_confidence"]),
            thresholds["evidence"] - float(case["evidence_sufficiency"]),
        )
        missing_penalty = 20 if case["missing_documents"] != "none" else 0
        risk_penalty = {"Low": 4, "Medium": 12, "High": 24}[case["clinical_risk"]]
        priority_score = round(
            32 * confidence_gap
            + missing_penalty
            + risk_penalty
            + sla_pressure * 0.65
            + int(case["reviewer_minutes"]) * 0.18,
            1,
        )
        queue.append(
            {
                "case_id": case["case_id"],
                "procedure": case["procedure"],
                "urgency": case["urgency"],
                "route": route,
                "priority_score": priority_score,
                "sla_remaining_hours": case["sla_remaining_hours"],
                "reviewer_minutes": case["reviewer_minutes"],
                "classifier_confidence": case["classifier_confidence"],
                "extraction_f1": case["extraction_f1"],
                "policy_match_confidence": case["policy_match_confidence"],
                "evidence_sufficiency": case["evidence_sufficiency"],
                "model_recommendation": case["model_recommendation"],
                "escalation_reason": escalation_reason,
                "unsafe_auto_decision_blocked": "yes" if blocked else "no",
            }
        )
    return sorted(queue, key=lambda row: row["priority_score"], reverse=True)


def create_feedback(cases):
    feedback = []
    for idx, case in enumerate(cases, start=1):
        if random.random() < 0.62 or case["missing_documents"] != "none":
            theme = random.choice(FEEDBACK_THEMES)
            severity = random.choices(["Low", "Medium", "High"], weights=[26, 48, 26])[0]
            feedback.append(
                {
                    "feedback_id": f"FB-{idx:04d}",
                    "case_id": case["case_id"],
                    "theme": theme,
                    "severity": severity,
                    "owner": OWNER_MAP[theme],
                    "reviewer_note": reviewer_note(theme),
                    "closed_loop_action": closed_loop_action(theme),
                }
            )
    return feedback


def reviewer_note(theme):
    notes = {
        "Missing conservative therapy duration": "Reviewer could not verify duration from the submitted notes.",
        "Extracted diagnosis needs citation": "Diagnosis code is plausible but needs a source sentence pointer.",
        "Policy version mismatch": "The rationale references an older policy clause.",
        "Ambiguous urgency signal": "The model treated a standard request as expedited based on weak language.",
        "Rationale needs patient-specific language": "Summary is clinically coherent but too generic for the packet.",
        "Duplicate document packet": "Intake included repeated pages that inflated evidence counts.",
    }
    return notes[theme]


def closed_loop_action(theme):
    actions = {
        "Missing conservative therapy duration": "Add duration extractor and reviewer checklist item.",
        "Extracted diagnosis needs citation": "Require quote-level citation before rationale generation.",
        "Policy version mismatch": "Refresh policy index and lock rationale to active policy date.",
        "Ambiguous urgency signal": "Tune classifier prompt with urgency counterexamples.",
        "Rationale needs patient-specific language": "Add rationale rubric and QA prompt examples.",
        "Duplicate document packet": "Add duplicate-page detector before extraction.",
    }
    return actions[theme]


def summarize_feedback(feedback):
    grouped = defaultdict(lambda: {"cases": 0, "high": 0, "medium": 0, "owner": "", "action": ""})
    for item in feedback:
        bucket = grouped[item["theme"]]
        bucket["cases"] += 1
        bucket["high"] += int(item["severity"] == "High")
        bucket["medium"] += int(item["severity"] == "Medium")
        bucket["owner"] = item["owner"]
        bucket["action"] = item["closed_loop_action"]
    rows = []
    for theme, values in grouped.items():
        priority = values["high"] * 3 + values["medium"] * 1.4 + values["cases"] * 0.8
        rows.append(
            {
                "theme": theme,
                "affected_cases": values["cases"],
                "high_severity_count": values["high"],
                "medium_severity_count": values["medium"],
                "owner": values["owner"],
                "closed_loop_action": values["action"],
                "feedback_priority_score": round(priority, 1),
            }
        )
    return sorted(rows, key=lambda row: row["feedback_priority_score"], reverse=True)


def compliance_controls(cases, review_queue):
    total = len(cases)
    trace_ready = sum(
        1
        for case in cases
        if min(
            float(case["classifier_confidence"]),
            float(case["extraction_f1"]),
            float(case["policy_match_confidence"]),
            float(case["rationale_completeness"]),
        )
        >= 0.78
    )
    within_clock = sum(1 for case in cases if int(case["sla_remaining_hours"]) >= 0)
    human_denial = sum(
        1
        for row in review_queue
        if row["model_recommendation"] == "Potential non-coverage, clinician required"
        and row["route"] == "Escalate to licensed clinician"
    )
    missing_doc_clear = sum(1 for row in review_queue if row["route"] != "Request missing documentation")
    return [
        {
            "control": "CMS turnaround clock",
            "status": "Watch",
            "evidence": f"{within_clock} of {total} cases remain inside the active clock.",
            "product_behavior": "Surface SLA pressure and move near-breach cases into expedited reviewer worklists.",
        },
        {
            "control": "No automated adverse determination",
            "status": "Ready",
            "evidence": f"{human_denial} potential non-coverage cases are routed to licensed clinicians.",
            "product_behavior": "Allow auto-affirm only. Require human clinical review for adverse or high-risk outcomes.",
        },
        {
            "control": "FHIR prior authorization readiness",
            "status": "In progress",
            "evidence": "FHIR API, X12 278, portal, and fax conversion channels are tracked separately.",
            "product_behavior": "Normalize intake events into a single case packet with source-channel lineage.",
        },
        {
            "control": "Audit trace completeness",
            "status": "Watch",
            "evidence": f"{trace_ready} of {total} cases have sufficient confidence and rationale trace fields.",
            "product_behavior": "Require source citation, policy version, confidence score, reviewer action, and rationale snapshot.",
        },
        {
            "control": "Documentation sufficiency",
            "status": "Watch",
            "evidence": f"{missing_doc_clear} of {total} cases avoid missing-document routing.",
            "product_behavior": "Ask for missing evidence before clinical QA when required packet elements are absent.",
        },
    ]


def create_pipeline_runs(cases):
    rows = []
    stages = [
        ("Classification", "classifier_confidence", 0.84),
        ("Document extraction", "extraction_f1", 0.82),
        ("Clinical QA", "evidence_sufficiency", 0.82),
        ("Decision support", "policy_match_confidence", 0.84),
    ]
    for case in cases:
        for stage, field, threshold in stages:
            value = float(case[field])
            rows.append(
                {
                    "case_id": case["case_id"],
                    "stage": stage,
                    "score": value,
                    "threshold": threshold,
                    "stage_status": "Pass" if value >= threshold else "Review",
                    "latency_seconds": int(random.gauss(70 + threshold * 60, 18)),
                }
            )
    return rows


def create_summary(cases, review_queue, threshold_rows, feedback_rows, compliance_rows):
    balanced = next(row for row in threshold_rows if row["scenario"] == "Balanced")
    near_breach = sum(1 for case in cases if int(case["sla_remaining_hours"]) < 12)
    missing_docs = sum(1 for case in cases if case["missing_documents"] != "none")
    route_counts = Counter(row["route"] for row in review_queue)
    stage_cards = [
        {
            "label": "Cases in pipeline",
            "value": str(len(cases)),
            "detail": f"{near_breach} near CMS clock breach",
        },
        {
            "label": "Auto-affirm eligible",
            "value": str(balanced["auto_affirm_cases"]),
            "detail": "Only coverage-met cases with complete evidence",
        },
        {
            "label": "Reviewer hours",
            "value": str(balanced["reviewer_hours"]),
            "detail": "Balanced threshold scenario",
        },
        {
            "label": "Missing-doc packets",
            "value": str(missing_docs),
            "detail": "Routed before clinical QA",
        },
    ]
    return {
        "stageCards": stage_cards,
        "routeCounts": dict(route_counts),
        "topCases": review_queue[:8],
        "thresholds": threshold_rows,
        "architecture": MODEL_ARCHITECTURE,
        "interoperability": INTEROPERABILITY_CONTROLS,
        "feedback": feedback_rows,
        "compliance": compliance_rows,
    }


def write_analysis_docs(cases, review_queue, threshold_rows, feedback_rows):
    top_case = review_queue[0]
    balanced = next(row for row in threshold_rows if row["scenario"] == "Balanced")
    high_priority_feedback = feedback_rows[0]
    (ANALYSIS_DIR / "executive_findings.md").write_text(
        "\n".join(
            [
                "# Executive Findings",
                "",
                "## What I analyzed",
                "",
                f"I generated {len(cases)} synthetic Medicare prior authorization case packets and scored them across classification, extraction, clinical QA, decision support, reviewer feedback, and compliance controls.",
                "",
                "## Findings",
                "",
                f"- The balanced threshold policy auto-affirms {balanced['auto_affirm_cases']} cases and keeps {balanced['unsafe_auto_decisions_blocked']} unsafe automation candidates behind guardrails.",
                f"- The highest-priority work item is {top_case['case_id']} for {top_case['procedure']}, routed to {top_case['route']} because {top_case['escalation_reason'].lower()}.",
                f"- The most important feedback loop is {high_priority_feedback['theme']}, affecting {high_priority_feedback['affected_cases']} cases and owned by {high_priority_feedback['owner']}.",
                "",
                "## Recommendation",
                "",
                "Use the balanced threshold policy as the default operating mode. Keep auto-affirm narrow, route missing-document cases before clinical QA, and turn reviewer feedback into weekly prompt, extraction, and policy-index changes.",
                "",
            ]
        )
    )
    (ANALYSIS_DIR / "analysis_plan.md").write_text(
        "\n".join(
            [
                "# Analysis Plan",
                "",
                "1. Generate PHI-free synthetic prior authorization packets with urgency, intake channel, document sufficiency, model confidence, clinical risk, and reviewer effort.",
                "2. Score each packet through classification, extraction, clinical QA, and decision support gates.",
                "3. Compare conservative, balanced, and aggressive confidence threshold policies.",
                "4. Build a clinical review queue that prioritizes SLA pressure, missing evidence, clinical risk, and confidence gaps.",
                "5. Aggregate reviewer feedback into model, prompt, policy, and intake remediation actions.",
                "6. Define model selection, prompt contracts, evaluation metrics, and human guardrails by pipeline stage.",
                "7. Map product behavior to CMS turnaround clocks, human review guardrails, interoperability readiness, and audit trace needs.",
                "",
            ]
        )
    )
    (ANALYSIS_DIR / "sql_checks.sql").write_text(
        "\n".join(
            [
                "-- SQL checks mirror the synthetic CSV outputs in this public portfolio artifact.",
                "",
                "select urgency, count(*) as cases",
                "from authorization_cases",
                "group by urgency;",
                "",
                "select route, count(*) as cases, avg(priority_score) as avg_priority",
                "from clinical_review_queue",
                "group by route",
                "order by avg_priority desc;",
                "",
                "select scenario, auto_affirm_cases, clinician_escalations, unsafe_auto_decisions_blocked",
                "from threshold_scenarios",
                "order by reviewer_hours;",
                "",
                "select stage, model_choice, eval_metric",
                "from model_architecture_decisions",
                "order by stage;",
                "",
                "select interface, status, risk",
                "from interoperability_readiness",
                "where status <> 'Design ready';",
                "",
            ]
        )
    )


def main():
    DATA_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    SRC_DIR.mkdir(exist_ok=True)

    cases = create_cases()
    pipeline_runs = create_pipeline_runs(cases)
    threshold_rows = create_threshold_scenarios(cases)
    review_queue = create_review_queue(cases)
    feedback = create_feedback(cases)
    feedback_rows = summarize_feedback(feedback)
    compliance_rows = compliance_controls(cases, review_queue)
    summary = create_summary(cases, review_queue, threshold_rows, feedback_rows, compliance_rows)

    write_csv(DATA_DIR / "authorization_cases.csv", cases, list(cases[0].keys()))
    write_csv(DATA_DIR / "pipeline_runs.csv", pipeline_runs, list(pipeline_runs[0].keys()))
    write_csv(DATA_DIR / "reviewer_feedback.csv", feedback, list(feedback[0].keys()))
    write_csv(OUTPUT_DIR / "threshold_scenarios.csv", threshold_rows, list(threshold_rows[0].keys()))
    write_csv(OUTPUT_DIR / "clinical_review_queue.csv", review_queue, list(review_queue[0].keys()))
    write_csv(OUTPUT_DIR / "feedback_loop_queue.csv", feedback_rows, list(feedback_rows[0].keys()))
    write_csv(OUTPUT_DIR / "compliance_readiness.csv", compliance_rows, list(compliance_rows[0].keys()))
    write_csv(
        OUTPUT_DIR / "model_architecture_decisions.csv",
        MODEL_ARCHITECTURE,
        list(MODEL_ARCHITECTURE[0].keys()),
    )
    write_csv(
        OUTPUT_DIR / "interoperability_readiness.csv",
        INTEROPERABILITY_CONTROLS,
        list(INTEROPERABILITY_CONTROLS[0].keys()),
    )
    (OUTPUT_DIR / "pipeline_summary.json").write_text(json.dumps(summary, indent=2))
    (SRC_DIR / "data.js").write_text("window.STUDIO_DATA = " + json.dumps(summary, indent=2) + ";\n")

    (DATA_DIR / "README.md").write_text(
        "\n".join(
            [
                "# Data README",
                "",
                "All datasets are deterministic synthetic data for a public portfolio artifact. They do not represent real patients, providers, payer decisions, Medicare cases, clinical documents, utilization management queues, or production model performance.",
                "",
                "The synthetic structure is modeled on a prior authorization workflow with intake, document extraction, clinical policy matching, clinical QA, decision support, reviewer feedback, and compliance controls. Randomness is seeded in `scripts/score_operating_data.py` so the outputs are reproducible.",
                "",
                "Generated files:",
                "",
                "- `authorization_cases.csv`: PHI-free case packets with procedure category, urgency, intake channel, document sufficiency, model confidence, clinical risk, and reviewer effort.",
                "- `pipeline_runs.csv`: stage-level confidence and latency rows for classification, extraction, clinical QA, and decision support.",
                "- `reviewer_feedback.csv`: synthetic reviewer notes used to close the loop with prompt, extraction, policy-index, and intake workflow fixes.",
                "- `analysis/outputs/model_architecture_decisions.csv`: product and ML engineering contract for each model stage, including model choice, prompt contract, output contract, evaluation metric, and human guardrail.",
                "- `analysis/outputs/interoperability_readiness.csv`: FHIR, X12, HL7-style, reviewer workbench, and audit export readiness controls.",
                "",
            ]
        )
    )
    write_analysis_docs(cases, review_queue, threshold_rows, feedback_rows)

    print("Generated prior authorization AI review workflow artifact data.")
    print(f"Cases: {len(cases)}")
    print(f"Balanced auto-affirm cases: {next(row for row in threshold_rows if row['scenario'] == 'Balanced')['auto_affirm_cases']}")
    print(f"Top review case: {review_queue[0]['case_id']} with priority {review_queue[0]['priority_score']}")


if __name__ == "__main__":
    main()
