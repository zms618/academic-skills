---
name: research-advisor-report
description: Mandatory final mentor-style, plain-language, experiment-ready Idea report after Research Idea Discovery screening, including scientific motivation, defensible contributions, story, linked datasets/models/baselines and E0/weekly plan, reviewer attacks and kill criteria.
---

## v3.4 multi-motivation / CVPR research discovery deliverables

If the request is new research discovery aiming for a very high-impact CVPR paper, **first** produce a separate Motivation Landscape report comparing 5–8 source-grounded problem candidates with scientific necessity and counterevidence, then a Gap/Survivors report for the selected 2–3. These precede the individual Idea/method execution report. Do not show 1–3 contributions before a problem survives both M0 and the targeted prior-art gap investigation. See `../research-idea-discovery/references/motivation-portfolio-and-cvpr.md`. Differentiate research ambition, verified evidence, gap opportunity, actual novelty and achievable compute. Never promise Best Paper or imply that a structural gate proves venue-level scientific merit.

# Research Advisor Report v3.2

## v3.3 Motivation-first stop rule

The main report first states the **M0 problem and motivation verdict** with exact observed failures, evidence locators, baseline fairness, important stakes, two alternative causes and a no-new-model probe. When M0 is not PASS_FOR_IDEATION, deliver a concise **problem-discovery report** and stop; no 1–3 contributions, network, method design or 7-day training fantasy. Add M0 status and evidence to a full downstream report and revise it if N/M2 refute the original premise. `references/motivation-first-gate.md` controls this behavior.

The researcher needs an explanation they understand and a specific next experiment they can execute. Avoid abstract audit jargon in the main answer; move M1/N/L/M2/S gate details to optional appendix.

Read `../research-idea-discovery/references/research-advisor-output-protocol.md`, `../research-idea-discovery/references/plain-language-idea-protocol.md`, `../research-idea-discovery/references/research-execution-protocol.md`, and `../research-idea-discovery/references/scientific-story-and-contributions.md`.

## v3.2 method viability and usefulness addendum

- Read `../research-idea-discovery/references/method-design-and-necessity.md` and `../research-idea-discovery/references/researcher-value-acceptance.md` and run the **implementer + critical reviewer role simulation** before returning the answer.
- **Mandatory method design** (for a full research proposal): concise task I/O, operational estimate (computed from what, with/without labels), minimal architecture/module wiring, technical algorithm or equations, gradients/Loss with frozen/updatable parameters, test-time t0/t1 trace, resource/complexity and known failure cases. If not yet operational, say `METHOD_NOT_READY` and name the exact missing observation/code/data; do not pretend the idea is implementable.
- Give M0 easiest competitor, M1 smallest core mechanism, M2 complexity only if independently necessary. The 1–3 contributions are **claims** with separate tests, not the modules M0/M1/M2. Merge redundant claims.
- Every proposed component must earn its place with a necessary ablation and a source-grounded integration action; flag collisions at operator level.
- The report must include researcher artifacts (CSV/JSON/config/patch) and a bounded first action. Explain when a source model cannot possibly recover missing task information.
- No fabricated measured success or code inspection, and no claim a run took place based on role-play.

## Non-negotiable

- Lead with status, one-sentence **human** research problem, and first real action.
- Explain example input/output, previous solution and why it *may* fail before naming new architecture.
- Explicit Motivation: actual significance, evidence of gap, original vs revised after near-neighbor analysis.
- Show closest prior works with factual boundaries; do not claim UniModalShift/DASP/etc lack things you have not checked.
- Distinguish Hypothesis from Potential Contribution and validated result. Offer 1–3 contributions only if distinguishable, **never manufacture the third**.
- Make the story legible: Observation → Failure → possible Root cause → Insight → Method → Evidence; unknown links marked UNKNOWN.
- **Execution card mandatory**: concrete dataset/parent/split/fields/official URL/access state, compatible model/checkpoint + code, same-task Source/simple rival/strong baseline, frozen/updated weights, metrics, resource unknowns. If any cannot be verified, state that and propose a real check or Deep Research handoff. Do not choose arbitrary pretrained models just because names are familiar.
- State the 0–48h E0 test and conditional 7-day plan, artifacts and GO/STOP triggers, with no invented runtime or unobserved test outcomes.
- Explain strongest rejection risk, minimal test to distinguish mechanism from uncertainty/threshold/freezing, and a final one-line teach-back.

If no defensible idea exists: clear negative verdict, specific blockers and copy-paste targeted Deep Research prompt. For follow-up explanation requests, use a small toy example instead of repeating the whole report. All important statuses VERIFIED / CONDITIONAL / HYPOTHESIS / UNKNOWN and no fake execution results.

## v3.5 research lineage section (paper-first projects)
Before giving potential contributions, identify 3–5 anchor papers by role with exact evidence status, what each established, which stronger newer paper may have solved the problem, and which experiment or implementation asset the student can reuse. Lead with the motivating failure in normal language. Report `SCIENTIFIC_UPSIDE` and `RESEARCH_VELOCITY` separately; include a 14-day conditional decision sequence and an explicit strongest null explanation. Do not treat author limitation text as proof, do not mix incompatible published benchmark results, and do not promise replication where access is not verified.
