# Research Method Design & Validation Gate v3.2

## From WHY to HOW (mandatory for complete ML research Idea reports)

After M1/N/L/M2 and **before** announcing potential contributions or method viability, design the smallest intervention tied to the single causal failure. Design is PROPOSED until experiments run; `CAN_BE_IMPLEMENTED` requires sufficient interfaces/resources evidence, not merely written pseudocode.

### 0. Solve the decision, not the naming

Write in ordinary language: old method observes x, computes y, makes decision d, and may fail under condition c. State the specific changed decision and how it would avoid the failure *if the hypothesis holds*. Identify an impossibility boundary: e.g. removed information cannot be recreated from a remaining modality without added prior/information; a confidence score is not a sufficient statistic for task evidence.

### 1. Method alternatives: cannot skip the simplest rival

Design and compare: `M0 = source/freeze/skip/reset/ordinary calibrated threshold` as applicable; `M1 = minimal new mechanism` with ONE distinguishing mathematical operation; `M2 = additional mechanism only if M1 demonstrably inadequate`. State reason for rejecting simpler alternative. Do not report these as "three innovations"; final potential contributions are **scientific claims** only when independently testable.

### 2. Required implementer-facing Method Spec (for DL)

- **I/O and base**: actual task, modalities x_m, output task y, known input tensors/dtypes/shapes (UNKNOWN unless grounded), checkpoint/backbone architecture and code lineage, source-free/source-available constraint.
- **Estimator definition**: measured quantity (sample-level, class-pair, region, time), EXACT computational formula or algorithm; normalization and calibration; what stored source stats/target samples it needs; are there labels at test? Is score independent of raw confidence? If only a learned latent quantity with no observable supervision/proxy, mark UNIDENTIFIABLE/OPEN.
- **Mechanism**: choices, thresholds or continuous weights, update/no-update action, fallback when no usable evidence, O(C²) / token / sample / memory compute scaling as applicable.
- **Loss/algorithm**: each term's input and target, coefficient source, gradient path, stop-gradient, frozen and trainable parameters, adaptation timing, teacher refresh/reset, multiple test rounds, batch-vs-stream policy and state isolation.
- **Integration sketch**: concrete repo/config/checkpoint/version/split; name actual file/function ONLY if inspected. Otherwise `TO_LOCATE`; a reproducible checklist, not fabricated copy-paste commands. Describe new functions to implement, required data contract, intermediate output contract, and first unit tests.
- **Data and identifiability**: can available modalities distinguish specified class pairs in principle? Offline labels permissible *only* in diagnostic/evaluation and held-out threshold/model selection splits. List competing explanations and ways to separate covariate shift from information destruction. Source-data availability and prototype storage need explicit protocol check.
- **Evidence plan**: E0 observe effect on same samples (before vs after TTA); E1 score predicts harm conditional on confidence/entropy; E2 simplest alternative; E3 minimal new method; E4 ablate each necessary component plus multi-seed/multi-severity/generalization/cost. Distinct predictions (including conditions where mechanism MUST fail).
- **GO/STOP**: predeclare continuation and falsification criteria, with pilot effect sizes as PLANNED (not fake observations). If method cannot be implemented within resource bound, return a smaller diagnostic or pivot.

### 3. Explicit checks for pairwise/partial-modality TTA

If this application is relevant, ask:
1. Is the dataset's action/event label distinguishable from the surviving modality at all? Source-side class-pair AUC is a *population prior*, not proof that the current sample has evidence.
2. What non-oracle signal estimates sample-specific pairwise evidence without ground-truth test labels? If no usable signal, cannot claim this method works.
3. Does score explain additional harm beyond calibrated entropy, corruption severity, per-modality confidence and skip-update? Compare within matched strata; split selection and evaluation sets.
4. Are missingness and corrupted-but-present input conflated? Missing modality may require model masking rather than corruption generator; explicitly mark different protocols and feasible baselines.
5. If optimizing one class pair changes shared weights for others, how are *unselected* boundaries protected? Check gradients/teacher anchor; don't claim a masked loss freezes independent decision boundaries.
6. If the source teacher is wrong on degraded input, does protecting its margin merely preserve a wrong decision? Compare a no-update baseline and use transparent limits.
7. `O(C²)` pairwise edges at C classes: show actual computational scaling, how sparsification works and whether it changes claims. Avoid invented C, throughput or VRAM numbers.
8. Class imbalance, label prior drift, cross-domain calibration and confidence collapse may mimic boundary-specific failures: include appropriate controls.

### 4. Contribution necessity test

Each proposed claim must have: `type, claimed_delta, closest_work, unique_prediction, proposed_mechanism, needed_proof_or_experiment, cheapest_rival, kill_signal, evidence_status`. If two candidate claims need the same novelty delta and same decisive ablation, merge them. 0–3 genuinely separate claims are acceptable.

### 5. Deliverable

A selected minimal architecture, pseudocode, loss/mechanism, 2-step test-time trace, explicit updated parameters, testable edge cases, data/code/weights caveats, and **a grounded first implementation task**. No claim "can publish" from architecture plausibility alone.
