## v3.5.0 — Paper-grounded research discovery
- Add critical paper reading as part of scientific problem creation, with source-to-question evidence lineage and forward/backward related-work checking.
- Add four evidence-first generators: failure replication, reverse-engineering successful mechanisms, fair reconciliation of contradictory findings, deployment-to-science abstraction.
- Keep method-driven techniques as search heuristics only; any suggested problem still requires M0 and downstream novelty/necessity checks.
- Introduce scoped, optional PAPER_ANCHORED workflow gate with source-record replay; retain OPEN_PROBLEM and one-question paths.
- Add separate scientific-upside vs reproducible-speed assessments, concrete asset-check policy, conditional two-week GO/STOP decision plan, anti-fabrication tests and researcher desk simulation.

## 3.4.0 — Motivation portfolio, shortlisted gaps and CVPR aspiration
- Add high-impact portfolio-first discovery: 5–8 distinct motivations when evidence permits; evidence-/impact-/falsifiability-aware comparison and 2–3 justified shortlist entries.
- Add targeted gap investigation for all shortlisted motivations before selecting a final one; maintain backup motives and record negative results.
- Add optional CVPR Best Paper aspirational quality profile without treating awards as an official scoring rubric or changing other research domain settings.
- Add reproducibility-conscious structural portfolio/gap audit tool and regression cases; preserve existing M0/M1/M2/idea/method/experiment gates.

## v3.3.0 — Motivation-First Gate (2026-10-09)

- Enforce M0 problem-first evidence review before idea seeds/data search/method synthesis; retain M1 and M2 later.
- Add `research-problem-scout`, motivation-first protocol and structural CLI gate with guarded progression.
- Fail-fast weak/problem-unverified motivation; provide neutral evidence probe or reframing, not a proposed algorithm.
- Add multimodal DG evidence-first researcher fixtures, legacy-state protection and regression tests.
- Preserve existing v3.2 method synthesis and all later evidence gates.

# Changelog

## 3.2.0 — 2026-10-09

- Add research-method-designer with concrete operator/loss, TTA stepwise state updates and implementer-facing artifact requirements.
- Add two-role researcher/reviewer desktop simulation; force adversarial corrections to method and independent potential contributions rather than simply three named modules.
- Expose identifiability, oracle-label leakage, source-data constraints, missingness-vs-corruption, checkpoint mapping, source teacher failure and O(C^2) risks.
- Add realistic multimodal TTA worked example with unverified data access labeled, repository risks and E0/no-go conditions.
- Strengthen advisor-report checks and add researcher-utility self-audit with synthetic adversarial cases. Structural tests never prove novelty or reproducibility.
- Retain prior plugins' identity, integration defaults and original evidence/workflow features.

# Changelog

## 3.1.0 — 2026-10-09

- Introduce plain-language Idea Explanation and Research Execution Planner as actual user-facing requirements.
- Force concrete dataset/backbone/checkpoint/baseline, falsifying E0, first-week actions, kill conditions or explicit verification blockers.
- Align research story, hypothesis and potential contributions with evidence status; no forced third contribution.
- Integrate supervisor report into MAIN skill (not only optional advisor skill).
- Add structure checks and regression tests; retain all v2.7 evidence gates and restore original three default prompts in the extension manifest.

# Research Idea Discovery release history

## v2.7.0 — Execution-evidence gates and regression checks

- P0: Separate dataset catalog/field declarations from evidence of actually reading a bounded local sample. Record SHA256 and parsed fields. Reject missing sample, HTML landing pages, placeholder URLs, and missing labels. Do not claim source/license/whole-dataset reproducibility from a sample check.
- P0: Guard REVIEW → PILOT with a recorded review decision tied to idea_id/revision. Guard PILOT → UPDATE with replayed run-log checks and measurements or documented failure. Reject dry runs, no-metric successes, and forged readiness flags.
- P1: Structured four-axis prior-art query coverage and source-locator records; no claim of exhaustive novelty. Coverage record needed before mechanism-logic phase when running local workflow.
- P1: Compare proposed and simple-baseline outcomes when evidence exists. Equal/worse results mark `requires_reaudit` and force renewed mechanism/motivation/story scrutiny.
- P2: Local append-only idea ledger with duplicate signatures; revising source evidence invalidates dependent assessments. Adds reproducible adversarial fixtures.
- 66 tests pass locally. These check control logic, not academic originality or real-world availability without network/tool permissions.

## v2.6.0

- Research Idea Discovery plus targeted manual ChatGPT Deep Research handoff and report return.
