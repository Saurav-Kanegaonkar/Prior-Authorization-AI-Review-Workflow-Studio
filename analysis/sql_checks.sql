-- SQL checks mirror the synthetic CSV outputs in this public portfolio artifact.

select urgency, count(*) as cases
from authorization_cases
group by urgency;

select route, count(*) as cases, avg(priority_score) as avg_priority
from clinical_review_queue
group by route
order by avg_priority desc;

select scenario, auto_affirm_cases, clinician_escalations, unsafe_auto_decisions_blocked
from threshold_scenarios
order by reviewer_hours;

select stage, model_choice, eval_metric
from model_architecture_decisions
order by stage;

select interface, status, risk
from interoperability_readiness
where status <> 'Design ready';
