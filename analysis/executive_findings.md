# Executive Findings

## What I analyzed

I generated 48 synthetic Medicare prior authorization case packets and scored them across classification, extraction, clinical QA, decision support, reviewer feedback, and compliance controls.

## Findings

- The balanced threshold policy auto-affirms 7 cases and keeps 1 unsafe automation candidates behind guardrails.
- The highest-priority work item is PA-0010 for Knee arthroscopy, routed to Escalate to licensed clinician because clinical risk or possible adverse determination.
- The most important feedback loop is Missing conservative therapy duration, affecting 8 cases and owned by Document AI.

## Recommendation

Use the balanced threshold policy as the default operating mode. Keep auto-affirm narrow, route missing-document cases before clinical QA, and turn reviewer feedback into weekly prompt, extraction, and policy-index changes.
