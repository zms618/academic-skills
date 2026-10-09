# v3.4 Multiple Motivations → Shortlist → Gap Discovery → CVPR Best Paper Aspiration

## Central scientific discipline

The user's stated north star is **CVPR Best Paper**. Treat it as an **aspirational quality bar, not an official scoring rubric, promise of acceptance, or statistical prediction**. CVPR remains the venue; paper awards are an exceptional outcome beyond acceptance. CVPR 2026 reviewer guidance weighs technical soundness, novelty, significance, impact and encourages bold new concepts even without topping SOTA; use the official current-year reviewer/author guidelines when making time-sensitive claims. Adapt to another requested field/venue if the user later changes scope. The configurable project goal is `CVPR_BEST_PAPER_ASPIRATION`; the plugin is still generally usable in other research domains.

## New mandatory *portfolio-first* pipeline for DISCOVER / OPEN_EXPLORE / user-specified award-aspiring discovery

`SCOPE → NEUTRAL BROAD PROBLEM SCOUT → MOTIVATION PORTFOLIO (default 5–8 distinct genuine problems; no invention for quotas) → SHORTLIST 2–3 / with reasons → M0 EVIDENCE VALIDATION for each → TARGETED GAP INVESTIGATION for all shortlist members → CONTINUE / PROBE / PIVOT / STOP PER MOTIVATION → only then IDEA SEED / D0/G0 / M1 / N / L / M2 / method design / E0...`

**Budget is intentionally staged:** broad search before selection is light, source-grounded and neutral; after selection targeted investigation is deeper and includes negative/contradictory sources; heavy systematic mechanism audit and full compute feasibility belong downstream. Do not spend a full Deep Research budget on a weak candidate nor assume M0 establishes a novel gap. Keep at least one alternative motivation alive until gap review reveals why the top candidate is preferable. Do not select the easiest-to-implement topic over a more important, defensible scientific question without giving the trade-off.

### Step A: Motive generation without method-first bias

1. Search real failure cases, boundary conditions, surprising negative results, contradictions between theoretical expectation and outcome, and deployment harms. For CVPR prefer concrete vision/multimodal tasks, not arbitrary ML topics with weak visual grounding.
2. Draft 5–8 distinct **scientific questions**. Group near-duplicates into families. If honest source discovery yields only 2–4, show that reduced number and a coverage limitation; do not invent 8 variants of one claim. Each card includes task/protocol, observable result + source locator, why a strong simple baseline ought to work, why failure matters, an alternative explanation, what would disprove the problem, and missing evidence. Prior work can motivate a question but does not automatically establish a robust failure. No architecture, acronym, loss or ready-made 3 contributions at this point.
3. Diverse search axes for CVPR: generalization/brittleness; cross-modal causality/complementarity; failure of strong simple baselines; evaluation protocol and shortcut; information availability and observability; scaling/compute/explainability only when scientifically relevant. Do not confuse these axes with contributions.
4. Source statuses: `DIRECT_LOCATED` (actual source passage/table read), `PRIMARY_LEAD` (URL/abstract only), `HYPOTHESIS_ONLY`, `COUNTEREVIDENCE`. Tool-record existence is not independent scientific review.

### Step B: Motivation comparison and *reasoned* shortlist

Compare with **non-compensatory checks**, not a fabricated 9.4/10 or award probability:
- `R`: source-grounded reproducible reality of failure (cannot be replaced by popularity)
- `I`: significant stakes, why solving it changes what the community does/understands
- `G`: likely scope / generalization (one benchmark edge case vs a wider question; a decisive counterexample can still be important)
- `F`: falsifiable and a cheap decisive probe
- `C`: credible CVPR computer vision fit (what visual perception/reasoning tasks are implicated)
- `N?`: novelty/gap *opportunity* only, marked unresolved until targeted audit
- `T`: actual resource tractability; this is a trade-off, not a substitute for scientific importance
- `X`: strongest explanation other than the advertised research hypothesis

Each shortlisted motivation must show WHY it beat its **strongest rejected alternative** and what still could invalidate it; keep counterevidence visible. Rank **provisionally** by argument, not composite score. `PASS_FOR_IDEATION` remains an M0 result, and does NOT assert a CVPR-ready paper. No M0 pass → no Idea Seed, even if a motive looks prestigious. A promising single study may move to `PROBE_ONLY` without premature dismissal of a bold idea.

### Step C: Targeted gap research per shortlisted motivation

**Different research jobs**:
- `M0`: is there a real important phenomenon? Requires source and fair-comparison reasoning.
- `GAP INVESTIGATION`: what exactly have nearest works already explained/solved; what is the smallest unresolved important question after crediting their strongest case?
- `N`: after designing a specific mechanism, does it collide with existing methods computationally?
- `M2`: after N/L, does the revised motivation remain interesting and not already resolved?

For each shortlisted problem, identify nearest 3–7 papers **when available**, including same question / different mechanism, same mechanism / different task, high-performing simple rivals, and counterexamples. Record primary URLs/sections and reading depth; explicit limitation when not found. Write `original question → known explanations → unresolved *testable* gap → dangerous rival → fastest falsifier`. Search actively for the explanation that would make us STOP. If gap fully addressed, mark `ALREADY_SOLVED` and return to another shortlist entry; if evidence missing, `RESEARCH_MORE`, not a fake novelty delta.

### Step D: Only survivors receive method innovation

Produce one scientific hypothesis and 1–3 **potential** independent contributions only for surviving motives; distinguish problem discovery / conceptual insight / necessity-driven core mechanism / evaluation. No manufactured third module. Follow full method/feasibility/novelty protocols and strong simple rivals. Use 1–2 projects in parallel only if actual resources allow; explicitly choose one primary plus alternative rather than building three full systems at once.

### User-facing delivery (two checkpoints, not one giant report)

**Checkpoint 1: MOTIVATION LANDSCAPE — before committing to research**
- 30-second framing: the overall research tension, in human terms.
- Table of 5–8 **distinct** motivations with source/locator and exact failure, why needed, contrary evidence / null rival, scope and evidence confidence. Never invent exact metrics.
- Detailed comparison of 2–3 selected motivations: each with one concrete example, actual vs hypothesized failure, CVPR field-level stakes, literature / fairness holes, one no-new-method E0 probe, kill signal, why not the strongest rejected alternative.
- Provisional verdicts `INVESTIGATE_GAP / PROBE_FIRST / REJECT / SOURCE_UNKNOWN`; do not claim an innovation point or a best-paper score.
- Ask whether to proceed **only if the user has not already authorized continuing research**. Default continue on user's existing instruction.

**Checkpoint 2: GAP → RESEARCH DIRECTIONS**
- Per shortlisted motivation: closest existing explanations (factual with sources), truly remaining question, how much confidence in its existence, strongest threat and decision `SURVIVES_GAP / PROBE_ONLY / ALREADY_SOLVED / RESEARCH_MORE`.
- Choose at most two survivors for heavy method investigation, with a plain-language reason; if none, output negative findings and a targeted neutral next search rather than force a project.
- Only then attach scoped potential idea seeds, tangible dataset/model/baseline prospects, and the first falsifier. Final report keeps source evidence and unverified items distinct.

### Anti-game checks

- Writing three aliases for one motivation fails the portfolio's substantive diversity requirement.
- A single benchmark anomaly without matched conditions is a probe, not a proven fundamental flaw.
- The strongest published rival may already address the failure; revisit/refute, do not omit it.
- Source links that have not been read are leads, not VERIFIED evidence.
- Do not use arbitrary fixed numerical rankings to declare award potential. If a candidate has high potential impact but weak initial evidence, state `HIGH_UPSIDE_UNVERIFIED` and order a cheap experiment rather than throwing it out only due to low publication count.
- If the user supplied a single already-chosen question for VALIDATE/REFINE, apply M0 directly without inventing other motivations, unless they request multi-direction discovery.

## Final high-impact research audit after innovation assessment

For full CVPR Best Paper aspirations, do an explicit **scientific-impact adversarial review** *after* the mechanism and experiments are defined. It must confront: (1) whether the work reveals a non-obvious general lesson or only optimizes one benchmark, (2) whether the essential proof is technically sound/falsifiable, (3) the nearest functionally equivalent explanation, (4) matched fair controls and reproducibility, (5) how the finding matters to broader vision research, (6) a devastating counterexperiment, (7) limitations and compute. Explicitly separate `CVPR-quality scientific aspiration` from `award selection`, which cannot be promised or estimated by a made-up rating. The final JSON report should carry `goal: CVPR_BEST_PAPER_ASPIRATION` and `cvpr_aspiration_review` with corresponding fields; report structural completeness is not evidence of impact.

**CLI:** `python scripts/workflow.py init --project PATH --goal CVPR_BEST_PAPER_ASPIRATION` automatically activates the optional portfolio-first gate. `--motivation-mode PORTFOLIO` activates the gate for non-CVPR discovery; `--motivation-mode SINGLE` deliberately disables it for a one-question VALIDATE/REFINE audit. While at MOTIVATION_GATE, submit `motivation-portfolio --card`, validate focus M0 with `motivation-gate --card`, and submit `gap-investigation --card` before advancing to DIVERGE. The gap report MUST cover every shortlisted problem, even those that are now negative. Source contents remain independently unverified by these scripts.


## v3.5 source-paper grounding extension
For researchers favoring rapid progress, build a 3–5-paper adversarial anchor portfolio before collecting 5–8 *distinct* motivations. Read paper figures/tables and questions together, including a strong contrary paper. Source-to-observation-to-motivation lineage must stay auditable. Include failure replication, reverse-engineering of successful methods, matched-setting contradiction triage and real deployment-to-science problem abstraction. When paper evidence is sparse, return OPEN_PROBLEM rather than forcing fake anchors. Scientific impact and speed-to-first-valid-experiment should be reported separately, never numerically collapsed into a Best Paper prediction.
