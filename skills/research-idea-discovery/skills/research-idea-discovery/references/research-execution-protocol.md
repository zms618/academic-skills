# Concrete Research Execution Protocol v3.1

## Principle

An idea is not actionable if it has no specific evidence-backed starter dataset, model/checkpoint, baseline implementation, fair evaluation setting, and first falsifying action—or a clearly named gap and research handoff. Plugin finds them itself; never require the user to provide an already-vetted dataset.

## Feasibility stack card (one primary + at most one backup)

| Key | What to supply | Evidence status |
|---|---|---|
| Dataset | exact title/version, official dataset URL, input modalities, fields, task labels, split, license/access and expected sample subset | VERIFIED_LINK / OFFICIAL_PAGE_ONLY / METADATA_ONLY / LOCAL_SAMPLE_CHECKED / BLOCKED |
| Derived data | original parent, reproducible transformation, unchanged labels justification, leakage checks and cost | VERIFIED_RECIPE / PLANNED / UNKNOWN |
| Implementation | official project repo URL/commit, pretrained checkpoint, backbone, expected preprocessing | CODE_INSPECTED / README_ONLY / UNKNOWN |
| Baselines | Source/no-update; cheapest rival; 1–2 strongest related research implementations. Explain matching/mismatching dataset + metric | COMPATIBLE_VERIFIED / CONDITIONAL / INCOMPATIBLE |
| Adaptation | frozen weights, trainable head/adapter, online/test labels availability, optimizer/loss only if grounded | PAPER_CONFIRMED / PROPOSED / UNKNOWN |
| Cost | GPU/VRAM, sample count, storage, runtime from measured or attributable source; otherwise UNKNOWN | MEASURED / SOURCE_REPORTED / UNKNOWN |

**Hard rule**: A paper's public code is not evidence that its referenced dataset is downloadable. A named pretrained architecture is not evidence of a compatible end-to-end checkpoint. When no verified runnable stack is available, choose an inspection/availability E0 first; never say "48h复现可完成" without concrete grounds. No zero-to-one mass data collection or expensive labeling.

## E0 before Method

1. Task: a single falsifiable failure phenomenon. What is the dependent metric? What are the identical samples and conditions across controls?
2. Controls: Source frozen predictions, strongest reproducible related TTA, simple no/skip-update strategy; compare **adaptation-caused harm** (same corrupted inputs, before vs after update), not just corruption-caused accuracy drop.
3. Failure generator: reproducible severity levels; if hypothesizing evidence loss, state how information retention is measured offline (labels allowed only in offline diagnostics, not as test-time adaptation signal).
4. Record a small CSV/JSON artifact of sample ID, corruption config, baseline, seeds, clean/shift accuracy, confidence, prediction flip and update time; timestamps, code/config/hash where accessible.
5. Pre-register clear GO / REFINE / STOP rules **before** observing results. Unknown effect size thresholds should be set from resources or pilot precision, not invented as proof.

## Timeboxed actionable handoff

- **0–48 h**: day-one data/license/checkpoint reality check; tiny reproducible inference and corruption generation; E0 contrasted with Source/freeze/one simple rival; if data unavailable, return dataset audit and targeted Deep Research prompt.
- **Days 3–7** (conditional on E0 and hardware): characterize failure sources, more seeds/conditions, simplest alternative, one mechanism probe (no need train new large encoder), controlled pilot, revise claims and reviewer case.
- Each day: action → prerequisite → artifact → success/stop signal. No unverified precise GPU hours.

## Honest status & negative outcome

Statuses: READY_TO_INSPECT / ACCESS_PENDING / RUNNABLE_VERIFIED / PILOT_PLANNED / EXECUTED_WITH_LOGS / NO_DATA_PATH / STOP. They have distinct meanings. No fictitious completed runs. If E0 negative, question may need pivot; do not silently re-label it "positive" because a new graph is proposed.
