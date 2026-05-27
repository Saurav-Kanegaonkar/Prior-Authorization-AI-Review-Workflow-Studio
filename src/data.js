window.STUDIO_DATA = {
  "stageCards": [
    {
      "label": "Cases in pipeline",
      "value": "48",
      "detail": "8 near CMS clock breach"
    },
    {
      "label": "Auto-affirm eligible",
      "value": "7",
      "detail": "Only coverage-met cases with complete evidence"
    },
    {
      "label": "Reviewer hours",
      "value": "23.4",
      "detail": "Balanced threshold scenario"
    },
    {
      "label": "Missing-doc packets",
      "value": "15",
      "detail": "Routed before clinical QA"
    }
  ],
  "routeCounts": {
    "Escalate to licensed clinician": 7,
    "Request missing documentation": 15,
    "Auto-affirm with audit trace": 5,
    "Expedite reviewer queue": 6,
    "Clinical QA review": 15
  },
  "topCases": [
    {
      "case_id": "PA-0010",
      "procedure": "Knee arthroscopy",
      "urgency": "Expedited",
      "route": "Escalate to licensed clinician",
      "priority_score": 71.2,
      "sla_remaining_hours": -18,
      "reviewer_minutes": 44,
      "classifier_confidence": 0.767,
      "extraction_f1": 0.918,
      "policy_match_confidence": 0.71,
      "evidence_sufficiency": 0.777,
      "model_recommendation": "Escalate to clinician",
      "escalation_reason": "Clinical risk or possible adverse determination",
      "unsafe_auto_decision_blocked": "no"
    },
    {
      "case_id": "PA-0029",
      "procedure": "Home infusion",
      "urgency": "Standard",
      "route": "Request missing documentation",
      "priority_score": 60.4,
      "sla_remaining_hours": 26,
      "reviewer_minutes": 36,
      "classifier_confidence": 0.937,
      "extraction_f1": 0.737,
      "policy_match_confidence": 0.935,
      "evidence_sufficiency": 0.714,
      "model_recommendation": "Request more information",
      "escalation_reason": "Missing diagnosis_history; test_result",
      "unsafe_auto_decision_blocked": "no"
    },
    {
      "case_id": "PA-0009",
      "procedure": "DME oxygen",
      "urgency": "Standard",
      "route": "Auto-affirm with audit trace",
      "priority_score": 52.9,
      "sla_remaining_hours": -17,
      "reviewer_minutes": 36,
      "classifier_confidence": 0.863,
      "extraction_f1": 0.929,
      "policy_match_confidence": 0.845,
      "evidence_sufficiency": 0.943,
      "model_recommendation": "Affirm coverage criteria met",
      "escalation_reason": "Meets all confidence and evidence gates",
      "unsafe_auto_decision_blocked": "no"
    },
    {
      "case_id": "PA-0025",
      "procedure": "Genetic test",
      "urgency": "Expedited",
      "route": "Expedite reviewer queue",
      "priority_score": 52.7,
      "sla_remaining_hours": 0,
      "reviewer_minutes": 53,
      "classifier_confidence": 0.599,
      "extraction_f1": 0.947,
      "policy_match_confidence": 0.841,
      "evidence_sufficiency": 0.876,
      "model_recommendation": "Affirm coverage criteria met",
      "escalation_reason": "CMS clock risk",
      "unsafe_auto_decision_blocked": "no"
    },
    {
      "case_id": "PA-0016",
      "procedure": "DME oxygen",
      "urgency": "Standard",
      "route": "Expedite reviewer queue",
      "priority_score": 52.5,
      "sla_remaining_hours": -7,
      "reviewer_minutes": 47,
      "classifier_confidence": 0.804,
      "extraction_f1": 0.691,
      "policy_match_confidence": 0.934,
      "evidence_sufficiency": 0.923,
      "model_recommendation": "Affirm coverage criteria met",
      "escalation_reason": "CMS clock risk",
      "unsafe_auto_decision_blocked": "no"
    },
    {
      "case_id": "PA-0002",
      "procedure": "Spinal cord stimulator",
      "urgency": "Standard",
      "route": "Request missing documentation",
      "priority_score": 51.0,
      "sla_remaining_hours": 127,
      "reviewer_minutes": 47,
      "classifier_confidence": 0.512,
      "extraction_f1": 0.901,
      "policy_match_confidence": 0.862,
      "evidence_sufficiency": 0.589,
      "model_recommendation": "Request more information",
      "escalation_reason": "Missing test_result; clinical_note",
      "unsafe_auto_decision_blocked": "no"
    },
    {
      "case_id": "PA-0047",
      "procedure": "Home infusion",
      "urgency": "Expedited",
      "route": "Request missing documentation",
      "priority_score": 49.6,
      "sla_remaining_hours": 20,
      "reviewer_minutes": 17,
      "classifier_confidence": 0.76,
      "extraction_f1": 0.691,
      "policy_match_confidence": 0.868,
      "evidence_sufficiency": 0.786,
      "model_recommendation": "Request more information",
      "escalation_reason": "Missing order; conservative_therapy",
      "unsafe_auto_decision_blocked": "no"
    },
    {
      "case_id": "PA-0039",
      "procedure": "Advanced imaging",
      "urgency": "Standard",
      "route": "Escalate to licensed clinician",
      "priority_score": 46.7,
      "sla_remaining_hours": 12,
      "reviewer_minutes": 29,
      "classifier_confidence": 0.864,
      "extraction_f1": 0.924,
      "policy_match_confidence": 0.885,
      "evidence_sufficiency": 0.76,
      "model_recommendation": "Clinical review required",
      "escalation_reason": "Clinical risk or possible adverse determination",
      "unsafe_auto_decision_blocked": "no"
    }
  ],
  "thresholds": [
    {
      "scenario": "Conservative",
      "classifier_threshold": 0.9,
      "extraction_threshold": 0.88,
      "policy_threshold": 0.9,
      "evidence_threshold": 0.88,
      "auto_affirm_cases": 1,
      "clinical_review_cases": 18,
      "clinician_escalations": 7,
      "missing_doc_requests": 15,
      "expedited_queue_cases": 7,
      "reviewer_hours": 25.9,
      "unsafe_auto_decisions_blocked": 0
    },
    {
      "scenario": "Balanced",
      "classifier_threshold": 0.8,
      "extraction_threshold": 0.78,
      "policy_threshold": 0.8,
      "evidence_threshold": 0.78,
      "auto_affirm_cases": 7,
      "clinical_review_cases": 13,
      "clinician_escalations": 7,
      "missing_doc_requests": 15,
      "expedited_queue_cases": 6,
      "reviewer_hours": 23.4,
      "unsafe_auto_decisions_blocked": 1
    },
    {
      "scenario": "Aggressive",
      "classifier_threshold": 0.77,
      "extraction_threshold": 0.76,
      "policy_threshold": 0.78,
      "evidence_threshold": 0.76,
      "auto_affirm_cases": 9,
      "clinical_review_cases": 11,
      "clinician_escalations": 7,
      "missing_doc_requests": 15,
      "expedited_queue_cases": 6,
      "reviewer_hours": 22.4,
      "unsafe_auto_decisions_blocked": 2
    }
  ],
  "architecture": [
    {
      "stage": "Intake classification",
      "model_choice": "Small supervised classifier plus LLM fallback",
      "prompt_contract": "Classify request type, urgency, channel, and specialty with no clinical determination.",
      "input_signals": "Procedure text, CPT family, diagnosis text, channel metadata, urgency language",
      "output_contract": "Specialty, urgency, request class, confidence, and reason codes",
      "human_guardrail": "Urgency conflicts and low confidence route to clinical QA before clock assignment.",
      "eval_metric": "Macro F1 and urgency false-negative rate",
      "deploy_note": "Runs first so every downstream agent receives the same case envelope."
    },
    {
      "stage": "Document extraction",
      "model_choice": "OCR plus document AI extractor",
      "prompt_contract": "Extract dated evidence, source page, diagnosis, therapy history, and test results.",
      "input_signals": "PDF pages, fax packets, CCDA sections, portal attachments, duplicate-page score",
      "output_contract": "Structured evidence table with citation anchors and missing-field flags",
      "human_guardrail": "No generated evidence can enter the rationale unless it has a source citation.",
      "eval_metric": "Field-level F1, citation coverage, and duplicate-page precision",
      "deploy_note": "Keeps reviewer trust high by showing where each evidence claim came from."
    },
    {
      "stage": "Policy retrieval",
      "model_choice": "RAG over active medical necessity policy index",
      "prompt_contract": "Retrieve active criteria only, reject expired policy clauses, and quote criterion text.",
      "input_signals": "Specialty, procedure, payer policy date, diagnosis, requested site of service",
      "output_contract": "Policy criteria, version date, source citation, and retrieval confidence",
      "human_guardrail": "Version mismatch blocks automation and creates a policy-ops work item.",
      "eval_metric": "Top-k policy recall and active-version accuracy",
      "deploy_note": "Separates policy lookup from clinical reasoning so updates are auditable."
    },
    {
      "stage": "Clinical QA reasoning",
      "model_choice": "Large language model with criteria-by-criteria rubric",
      "prompt_contract": "Compare extracted evidence to each criterion and mark met, unmet, or unknown.",
      "input_signals": "Evidence table, retrieved criteria, contraindication flags, reviewer rubric",
      "output_contract": "Criterion findings, uncertainty notes, rationale draft, and escalation reason",
      "human_guardrail": "Any unmet or unknown criterion routes to licensed clinical review.",
      "eval_metric": "Reviewer agreement, unsupported-claim rate, and rationale completeness",
      "deploy_note": "Designed for decision support only, with no automated adverse determination."
    },
    {
      "stage": "Decision release",
      "model_choice": "Rules engine plus audit ledger",
      "prompt_contract": "Apply threshold policy and generate release packet only for eligible affirmations.",
      "input_signals": "Stage confidences, evidence sufficiency, clinical risk, SLA clock, reviewer action",
      "output_contract": "Route, reviewer task, denial-reason requirement, audit snapshot, and API response state",
      "human_guardrail": "Auto-affirm only when all gates pass and no non-coverage path is present.",
      "eval_metric": "Unsafe automation blocks, turnaround compliance, and audit completeness",
      "deploy_note": "Makes probabilistic output operational by binding scores to product behavior."
    }
  ],
  "interoperability": [
    {
      "interface": "FHIR Prior Authorization API",
      "status": "Design ready",
      "required_behavior": "Receive request, expose documentation requirements, return approval, denial reason, or more information.",
      "product_decision": "Map every case packet to a normalized request state and response status.",
      "risk": "Missing source-channel lineage makes API responses hard to audit."
    },
    {
      "interface": "X12 278 and 275",
      "status": "Design ready",
      "required_behavior": "Support EDI prior authorization request and attachment workflows where trading partners require them.",
      "product_decision": "Preserve EDI transaction IDs beside normalized FHIR-style case identifiers.",
      "risk": "Attachment gaps can create false missing-document tasks."
    },
    {
      "interface": "HL7 v2, C-CDA, and PDF intake",
      "status": "Needs validation",
      "required_behavior": "Turn clinical notes, observations, orders, and scanned packets into reviewer-ready evidence.",
      "product_decision": "Run duplicate-page detection and citation extraction before clinical QA.",
      "risk": "OCR quality and document order can distort evidence sufficiency."
    },
    {
      "interface": "Reviewer workbench",
      "status": "Design ready",
      "required_behavior": "Show model confidence, cited evidence, policy version, SLA clock, route, and reviewer action.",
      "product_decision": "Keep model uncertainty visible instead of hiding it behind a single recommendation.",
      "risk": "Reviewers may override without structured feedback unless the action form is constrained."
    },
    {
      "interface": "Audit and metrics export",
      "status": "Needs validation",
      "required_behavior": "Publish turnaround, approval, denial, more-information, and decision reason metrics.",
      "product_decision": "Log every route change with threshold policy, user, timestamp, and rationale snapshot.",
      "risk": "Incomplete audit fields weaken compliance reporting and root-cause analysis."
    }
  ],
  "feedback": [
    {
      "theme": "Missing conservative therapy duration",
      "affected_cases": 8,
      "high_severity_count": 4,
      "medium_severity_count": 3,
      "owner": "Document AI",
      "closed_loop_action": "Add duration extractor and reviewer checklist item.",
      "feedback_priority_score": 22.6
    },
    {
      "theme": "Ambiguous urgency signal",
      "affected_cases": 6,
      "high_severity_count": 3,
      "medium_severity_count": 2,
      "owner": "Classifier prompt",
      "closed_loop_action": "Tune classifier prompt with urgency counterexamples.",
      "feedback_priority_score": 16.6
    },
    {
      "theme": "Extracted diagnosis needs citation",
      "affected_cases": 5,
      "high_severity_count": 2,
      "medium_severity_count": 3,
      "owner": "Extraction prompt",
      "closed_loop_action": "Require quote-level citation before rationale generation.",
      "feedback_priority_score": 14.2
    },
    {
      "theme": "Policy version mismatch",
      "affected_cases": 5,
      "high_severity_count": 0,
      "medium_severity_count": 5,
      "owner": "Clinical policy ops",
      "closed_loop_action": "Refresh policy index and lock rationale to active policy date.",
      "feedback_priority_score": 11.0
    },
    {
      "theme": "Rationale needs patient-specific language",
      "affected_cases": 4,
      "high_severity_count": 2,
      "medium_severity_count": 1,
      "owner": "Clinical QA",
      "closed_loop_action": "Add rationale rubric and QA prompt examples.",
      "feedback_priority_score": 10.6
    },
    {
      "theme": "Duplicate document packet",
      "affected_cases": 3,
      "high_severity_count": 2,
      "medium_severity_count": 0,
      "owner": "Intake workflow",
      "closed_loop_action": "Add duplicate-page detector before extraction.",
      "feedback_priority_score": 8.4
    }
  ],
  "compliance": [
    {
      "control": "CMS turnaround clock",
      "status": "Watch",
      "evidence": "44 of 48 cases remain inside the active clock.",
      "product_behavior": "Surface SLA pressure and move near-breach cases into expedited reviewer worklists."
    },
    {
      "control": "No automated adverse determination",
      "status": "Ready",
      "evidence": "2 potential non-coverage cases are routed to licensed clinicians.",
      "product_behavior": "Allow auto-affirm only. Require human clinical review for adverse or high-risk outcomes."
    },
    {
      "control": "FHIR prior authorization readiness",
      "status": "In progress",
      "evidence": "FHIR API, X12 278, portal, and fax conversion channels are tracked separately.",
      "product_behavior": "Normalize intake events into a single case packet with source-channel lineage."
    },
    {
      "control": "Audit trace completeness",
      "status": "Watch",
      "evidence": "10 of 48 cases have sufficient confidence and rationale trace fields.",
      "product_behavior": "Require source citation, policy version, confidence score, reviewer action, and rationale snapshot."
    },
    {
      "control": "Documentation sufficiency",
      "status": "Watch",
      "evidence": "33 of 48 cases avoid missing-document routing.",
      "product_behavior": "Ask for missing evidence before clinical QA when required packet elements are absent."
    }
  ]
};
