# v3.5 Critical Reading, Paper Lineage and Research Opportunity

## Thesis
Two research decisions: **which problem is important and unsolved?** and **what solution is necessary?** The default fast-start discovery route reuses 3–5 deep-read anchor papers with different roles: core prior method, benchmark/failure record, strongest counterargument, mechanism explanation, optional cross-domain analogue. Open-problem discovery stays available when no appropriate papers exist; single-idea VALIDATE is exempt from paper-portfolio quotas.

A paper is an **evidence source, benchmark, baseline and intellectual stepping stone**, not proof its limitations remain open or that renaming its network is a contribution. Use both backward references and forward-citing papers when accessible.

## Paper evidence card (author claims and actual evidence separate)
Fields: `paper_id, title/year/venue/version/source_url, role, task/modality/train-test/split, headline result and exact Table/Figure locator, null/negative result, key assumption, what authors did NOT establish, source_read_depth, counterevidence, follow-up work, reusable resource/rights status, unanswered_falsifiable_question`. Label `ABSTRACT_LEAD`, `MAIN_PAPER_READ`, `TABLE_LOCATED`, `APPENDIX_READ`, `CODE_INSPECTED`, or `REPLICATION_LOG`. Do not upgrade evidence level by copying a URL.

Critical reading is simultaneous with question discovery. At each figure/table ask `What if another hospital? one modality shifted? matched ERM backbone and train budget? changes in data partition/metric? why should this mechanism be necessary?` Mark such questions HYPOTHESIS, not observed facts.

## Four high-value operators
1. `FAILURE_CASE`: replicate actual cases and cross-check samples, seeds, metric, budget, preprocessing, label leakage and domain split.
2. `SUCCESS_REVERSE_ENGINEERING`: take a strong reported improvement and test *why* it works: matched compute/parameter simple rival, component removal, feature/control intervention, alternative mechanism. Positive SOTA does not confirm the author's causal explanation.
3. `APPARENT_CONTRADICTION`: papers seem to disagree; before declaring a contradiction, compare task, dataset version, split, backbone, pretraining, hyperparameter search, metric, modalities, compute, target domain and variance. If mismatched mark `NOT_COMPARABLE_YET` and propose one harmonizing experiment.
4. `DEPLOYMENT_PRESSURE`: convert a real-world pain into measurable failure, accessible task/protocol, meaningful scientific inference, and plausible alternative explanation; anecdote alone is insufficient.

Also mine *evaluation claim mismatches* and *counterfactual stress tests*; lack of ablation is a possible question, not automatic evidence of a fatal problem.

## Problem-driven and method-driven — not mutually exclusive
Problem-driven is the main path: compare scientific necessity first, then methods. Method-driven is a **hypothesis generator only**: transfer of a proven analogue, necessary combination of complementary principles, or a reframing of task/objective. To become a candidate, it must identify an independently supported failure, pass M0, justify necessity over cheap alternatives, and survive near-neighbor computational equivalence checks. Do not rank research opportunities by method popularity.

## Lineage to communicate
`paper → actual reported observation → what is known → what remains unproved → scientific hypothesis → null explanation → no-new-model experiment → M0 verdict → only then method family`.
Keep links per Motivation Portfolio entry. A weak paper may supply a strong negative benchmark; an influential paper may have no tractable open problem. If forward literature resolves the gap, stop/pivot.

## Impact and velocity are separate axes
`SCIENTIFIC_DEPTH`: consequences for field; genuine unresolved mechanism; ability to generalize; falsifiability.
`RESEARCH_VELOCITY`: source/data/model/checkpoint accessibility; resource budget; first diagnostic latency.
Neither replaces the other. `HIGH_IMPACT_ACCESS_BLOCKED` differs from `FAST_BUT_INCREMENTAL`; explain tradeoffs rather than pretending 8/10 predicts a CVPR award.

## Output checkpoints
1. `PAPER LANDSCAPE`: distinct paper roles, exact evidence locators, open questions, negative/counter evidence and reused assets, with caveats.
2. `MOTIVATION PORTFOLIO`: 5–8 where genuine; compare research necessity; shortlist 2–3; no method design yet.
3. `GAP & REPRODUCTION REALITY`: all shortlist members get strongest follow-up rivals and a cheap matched-condition falsifier; identify one primary and reserve backup.
4. `SOLUTION SEARCH`: only survivors get method transfer / necessary combination / fundamental reframing exploration; then 1–3 independently testable potential contributions and realistic execution blueprint.
For a requested 14-day fast-start plan give GO/STOP checkpoints, not a claim a paper can be finished in 14 days.
