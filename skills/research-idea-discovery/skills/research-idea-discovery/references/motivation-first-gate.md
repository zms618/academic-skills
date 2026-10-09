# v3.3 M0: Motivation-first scientific problem discovery and fail-fast review

## Foundational rule

**A promising method does not justify a problem. Start with a scientific failure/contradiction; do not begin with an architecture, a slogan, or a fashionable shift combination.**

The discovery pipeline starts `SCOPE → PROBLEM_SCOUT (small, neutral source search) → EXPLAIN_PROBLEM → M0 MOTIVATION_GATE → (only when passed) DIVERGE/IDEA_SEED → DATA_SEARCH/D0 → G0 → M1 → N → L → M2 → S → PILOT`. M0 is an inexpensive **problem-worth-investigating filter**, not a novelty proof or a claim of proven causality. Keep G0/M1/N/L/M2 and all downstream hard gates unchanged.

Distinguish two research budgets:
- **Before M0:** search a bounded sample of benchmark tables, negative results, ablations, related strong baselines and replication notes to identify genuine problems. Prioritize surprising observations; compare fair tasks, backbone, splits and training budgets. Do not decide a cause yet. One tiny source/replication check is permitted to resolve an M0 ambiguity; this is a **problem-evidence probe**, not an E3 method implementation.
- **After M0 PASS_FOR_IDEATION:** only now invest in candidate mechanism synthesis, full dataset feasibility D0/G0, prior-art collision audit and experiments. Distinguish initial motive confidence (M0) from downstream necessity/newness (N/L/M2).

## Problem Card — required fields before proposing ideas

1. `problem_id`, `task_context`, `scientific_question`: who does what in which domain, under what train/test protocol; state one specific measurable contradiction or failure.
2. `concrete_observation` + `observable_measure` + `baseline_reference`: e.g. exact result metric, comparison target and what counts as same-setting fairness. A paper author's generic claim is NOT observed failure.
3. `evidence[]`: cite primary source/URL, Table/Figure/Section/page or reproducible log, observed comparison and strength; distinguish `DIRECT_TABLE`, `DIRECT_REPLICATION`, `DIRECT_THEOREM`, `BENCHMARK_ANALYSIS` from `ABSTRACT_ONLY` / `CLAIM_ONLY` / `HYPOTHESIZED`. Never fabricate metrics, dates or negative results.
4. `problem_importance`: why resolving this failure changes fundamental understanding, existing deployment performance, reliability, or a hard scientific limit. “Hot topic” and “novel combination” do not count.
5. `alternative_explanations`: at least two credible mundane explanations (unfair tuning, capacity, missing modalities, sample imbalance, implementation/metric mismatch etc.). `confounder_checks` explicitly say how to rule them out. Root cause remains `HYPOTHESIS` unless separately established.
6. `falsification_probe` + `bounded_probe`: minimal empirical measurement or proof and what result would refute the *problem premise*, preferably without a new model. Specify accessible resource lead/status, unit of comparison, artifact, label visibility, and expected stop signal. Do not require full D0/G0 here; M0's tiny probe is to verify a problem, not to design a solution.
7. `independence_scope`: record whether the evidence is from independent papers/teams or multiple datasets in one benchmark; do not describe them as equivalent. Independent sources are preferred; one high-quality result can justify a small PROBE_ONLY, not broad generalization.

## M0 outcomes — make the stop action real

- `PASS_FOR_IDEATION`: adequate, traceable observation(s), task importance, measurable benchmark, plausible fair comparison, competing causes and falsification plan. Require at least two truly distinct corroborating evidence units OR one unusually strong direct proof/reproducible demonstration with transparent applicability. The software gate checks only field/coherence presence; a real researcher must still judge evidential strength and prior work.
- `PROBE_ONLY`: one intriguing result but fairness/replication/significance unconfirmed. **No architecture, no three contributions, no deep search advocating the candidate.** Output a sharply targeted M0 problem-evidence probe and only investigate until the premise becomes supported/contradicted. This is not a PASS.
- `REJECT_OR_REFRAME`: only hot-topic story, “unseen shift combinations might fail,” abstract claims, known confounds, fully explained benchmark differences or lack of a measurable problem. Stop current idea and scout a different genuine scientific failure.
- `RESEARCH_MORE`: essential sources unavailable; output a neutral, *problem discovery* Deep Research prompt (not “prove our favorite idea”), with a finite evidence target and stop condition.

The problem Card must be **problem-first**: no `proposed_method`/`method_name`, no router/loss/three contributions in M0 report. New mechanism ideas may be privately parked but must NOT influence ranking of problem strength.

## Plain-language user report required BEFORE downstream Idea

- One sentence: **what unexpected thing fails** and in which setting.
- Two to four concrete observations with exact Table/Fig/setting, including adverse/contradicting ones. If unverifiable, say precisely what cannot be claimed.
- Why a strong baseline should have helped, and what actually differs; why that matters scientifically.
- Two alternate explanations and which **first no-new-model check** separates them.
- Verdict (`PASS_FOR_IDEATION/PROBE_ONLY/REJECT_OR_REFRAME/RESEARCH_MORE`) + permission boundary: `CAN_GENERATE_IDEA_SEEDS` yes/no.
- If no motive passed: return a neutral targeted reading/search plan, NOT 3 inventions, NOT dataset/backbone/method architecture tables. Mark the problem as pending or stopped rather than repeatedly polishing it.

## Case-study anti-bias: multimodal DG

User observes that a benchmark sometimes reports ERM above specialised multi-modal DG variants. Without verified table numbers, it is `RESEARCH_MORE` or `PROBE_ONLY`, not established general failure. Investigate **same task/split/backbone/optimization/compute** and multiple seeds and domains; test whether advantage is robust or an implementation/tuning artifact. Competing hypotheses: model-selection fairness; modality shortcut/overfitting; evaluation severity; capacity mismatch. Do NOT immediately conclude “unseen modality shift combinations” or “modality contributions inconsistent.” Only after observing a robust, important, unresolved failure may those become hypotheses/possible methods.

## Scope

Research domains other than deep learning may substitute falsifiable proofs, material measurements or system failures for model accuracy tables. A rare but decisive counterexample or theorem can motivate a strong problem without multiple empirical datasets. Source unavailable is uncertainty, not proof of a weak problem. Later N and M2 must re-evaluate significance against strongest recent neighbors; M0 PASS is never a journal/conference accept prediction.
