const data = window.STUDIO_DATA;

const tabs = [
  { id: "command", label: "Pipeline" },
  { id: "thresholds", label: "Thresholds" },
  { id: "review", label: "Clinical QA" },
  { id: "feedback", label: "Feedback" },
];

let activeTab = "command";

const app = document.querySelector("#app");

function routeClass(route) {
  if (route.includes("Auto")) return "good";
  if (route.includes("missing")) return "warn";
  if (route.includes("clinician")) return "risk";
  if (route.includes("Expedite")) return "blue";
  return "neutral";
}

function bar(value, max, className = "") {
  const width = Math.min(100, Math.round((Number(value) / max) * 100));
  return `<span class="bar ${className}"><span style="width:${width}%"></span></span>`;
}

function percent(value) {
  return `${Math.round(Number(value) * 100)}%`;
}

function renderShell(content) {
  app.innerHTML = `
    <main class="shell">
      <section class="hero">
        <div>
          <p class="eyebrow">Healthcare AI product artifact</p>
          <h1>Prior Authorization AI Review Workflow Studio</h1>
          <p class="hero-copy">A product experience layer for routing Medicare prior authorization packets through classification, document extraction, clinical QA, decision support, and reviewer feedback.</p>
        </div>
        <aside class="hero-panel">
          <span>Default operating mode</span>
          <strong>Balanced thresholds</strong>
          <p>Auto-affirm stays narrow. Missing evidence, high clinical risk, possible non-coverage, and clock pressure move into human review.</p>
        </aside>
      </section>

      <nav class="tabs" aria-label="Artifact surfaces">
        ${tabs
          .map(
            (tab) => `
              <button class="${activeTab === tab.id ? "active" : ""}" data-tab="${tab.id}" type="button">
                ${tab.label}
              </button>
            `
          )
          .join("")}
      </nav>

      ${content}
    </main>
  `;

  document.querySelectorAll("[data-tab]").forEach((button) => {
    button.addEventListener("click", () => {
      activeTab = button.dataset.tab;
      render();
    });
  });
}

function renderCommandCenter() {
  const routeRows = Object.entries(data.routeCounts)
    .sort((a, b) => b[1] - a[1])
    .map(
      ([route, count]) => `
        <div class="route-row">
          <span class="pill ${routeClass(route)}">${route}</span>
          <strong>${count}</strong>
          ${bar(count, 48, routeClass(route))}
        </div>
      `
    )
    .join("");

  const topCase = data.topCases[0];
  return `
    <section class="metrics-grid">
      ${data.stageCards
        .map(
          (card) => `
            <article class="metric-card">
              <span>${card.label}</span>
              <strong>${card.value}</strong>
              <p>${card.detail}</p>
            </article>
          `
        )
        .join("")}
    </section>

    <section class="surface-grid two">
      <article class="panel">
        <div class="panel-head">
          <span class="eyebrow">Routing distribution</span>
          <h2>Where the pipeline sends work</h2>
        </div>
        <div class="route-list">${routeRows}</div>
      </article>

      <article class="panel priority-panel">
        <div class="panel-head">
          <span class="eyebrow">Highest priority packet</span>
          <h2>${topCase.case_id} ${topCase.procedure}</h2>
        </div>
        <dl class="case-facts">
          <div><dt>Route</dt><dd>${topCase.route}</dd></div>
          <div><dt>Reason</dt><dd>${topCase.escalation_reason}</dd></div>
          <div><dt>SLA remaining</dt><dd>${topCase.sla_remaining_hours} hours</dd></div>
          <div><dt>Recommendation</dt><dd>${topCase.model_recommendation}</dd></div>
        </dl>
      </article>
    </section>
  `;
}

function renderThresholds() {
  return `
    <section class="surface-grid threshold-grid">
      ${data.thresholds
        .map(
          (scenario) => `
            <article class="panel threshold-card">
              <div class="panel-head">
                <span class="eyebrow">${scenario.scenario} scenario</span>
                <h2>${scenario.reviewer_hours} reviewer hours</h2>
              </div>
              <div class="scenario-metrics">
                <div><span>Auto-affirm</span><strong>${scenario.auto_affirm_cases}</strong></div>
                <div><span>Clinical QA</span><strong>${scenario.clinical_review_cases}</strong></div>
                <div><span>Clinician escalation</span><strong>${scenario.clinician_escalations}</strong></div>
                <div><span>Missing docs</span><strong>${scenario.missing_doc_requests}</strong></div>
              </div>
              <div class="threshold-bars">
                <label>Classifier ${percent(scenario.classifier_threshold)} ${bar(scenario.classifier_threshold, 1, "blue")}</label>
                <label>Extraction ${percent(scenario.extraction_threshold)} ${bar(scenario.extraction_threshold, 1, "good")}</label>
                <label>Policy ${percent(scenario.policy_threshold)} ${bar(scenario.policy_threshold, 1, "warn")}</label>
                <label>Evidence ${percent(scenario.evidence_threshold)} ${bar(scenario.evidence_threshold, 1, "risk")}</label>
              </div>
              <p class="guardrail">${scenario.unsafe_auto_decisions_blocked} unsafe automation candidates blocked by guardrails.</p>
            </article>
          `
        )
        .join("")}
    </section>
  `;
}

function renderReview() {
  return `
    <section class="panel">
      <div class="panel-head split">
        <div>
          <span class="eyebrow">Clinical QA workbench</span>
          <h2>Case packets needing reviewer action</h2>
        </div>
        <p>Sorted by confidence gap, missing evidence, clinical risk, SLA pressure, and reviewer effort.</p>
      </div>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Case</th>
              <th>Route</th>
              <th>Priority</th>
              <th>Confidence</th>
              <th>Evidence</th>
              <th>Reason</th>
            </tr>
          </thead>
          <tbody>
            ${data.topCases
              .map(
                (caseRow) => `
                  <tr>
                    <td><strong>${caseRow.case_id}</strong><span>${caseRow.procedure}</span></td>
                    <td><span class="pill ${routeClass(caseRow.route)}">${caseRow.route}</span></td>
                    <td>${caseRow.priority_score}</td>
                    <td>
                      <span>Class ${percent(caseRow.classifier_confidence)}</span>
                      <span>Extract ${percent(caseRow.extraction_f1)}</span>
                    </td>
                    <td>
                      <span>Policy ${percent(caseRow.policy_match_confidence)}</span>
                      <span>Evidence ${percent(caseRow.evidence_sufficiency)}</span>
                    </td>
                    <td>${caseRow.escalation_reason}</td>
                  </tr>
                `
              )
              .join("")}
          </tbody>
        </table>
      </div>
    </section>
  `;
}

function renderFeedback() {
  return `
    <section class="surface-grid two">
      <article class="panel">
        <div class="panel-head">
          <span class="eyebrow">Reviewer feedback loop</span>
          <h2>What should change in the AI pipeline</h2>
        </div>
        <div class="feedback-list">
          ${data.feedback
            .map(
              (item) => `
                <div class="feedback-item">
                  <div>
                    <strong>${item.theme}</strong>
                    <span>${item.owner}</span>
                  </div>
                  <p>${item.closed_loop_action}</p>
                  <b>${item.feedback_priority_score}</b>
                </div>
              `
            )
            .join("")}
        </div>
      </article>

      <article class="panel">
        <div class="panel-head">
          <span class="eyebrow">Compliance behavior</span>
          <h2>How rules become product controls</h2>
        </div>
        <div class="control-list">
          ${data.compliance
            .map(
              (item) => `
                <div class="control-item">
                  <span class="pill ${item.status === "Ready" ? "good" : "warn"}">${item.status}</span>
                  <strong>${item.control}</strong>
                  <p>${item.product_behavior}</p>
                  <small>${item.evidence}</small>
                </div>
              `
            )
            .join("")}
        </div>
      </article>
    </section>
  `;
}

function render() {
  if (activeTab === "thresholds") renderShell(renderThresholds());
  else if (activeTab === "review") renderShell(renderReview());
  else if (activeTab === "feedback") renderShell(renderFeedback());
  else renderShell(renderCommandCenter());
}

render();
