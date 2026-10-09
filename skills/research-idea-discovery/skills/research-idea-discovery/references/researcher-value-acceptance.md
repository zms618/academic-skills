# Researcher Utility Acceptance: will this actually help someone do research?

## Mandatory adversarial role-play BEFORE final report

Simulate TWO distinct readers while composing the report (role simulation, not independent trained agents):

- **Implementing PhD student**: after reading, can I tell what files/data to inspect, compute which score, which module to code first, exact inputs/outputs, which weights to update, what will happen at the next test batch, and what result will cause a pivot? If NO, fill gap or state verified blocker.
- **Critical area reviewer**: does core hypothesis differ from existing mechanisms at the **operator/prediction** level? Could simple threshold/freeze/entropy/calibration/candidate-label methods match the apparent gain? Are the proposed three contributions merely one idea split across modules? Is missingness identifiable? Are datasets/checkpoints/task/labels aligned? If NO, downgrade verdict.

## Useful vs empty output

BANNED as the only method explanation: 'introduce a novel robust framework', 'attention-based evidence reasoning', 'add a relation graph', 'optimize reliability', 'use CLIP or ImageBind' with no verified compatibility, 'state-of-the-art results expected', or an arbitrary list of general datasets.

The minimal valuable answer contains:
1. **Explain-back**: one normal-language failure, a numerical toy counterexample explicitly marked TOY, the single scientific question.
2. **Feasibility**: ONE primary grounded dataset+task/split, code, matching checkpoint and preprocessing with independent status per item; when not verified, first step resolves mismatch.
3. **Design**: operator-level estimator, new vs original behavior, equations/pseudocode, trainable/frozen parameters, runtime update order, fallback and known impossible cases; no ungrounded shapes.
4. **Competition**: at least Source/no-adapt, cheapest strong rival, and relevant near-neighbor, with compatibility differences explicitly noted.
5. **Science**: E0 to demonstrate adaptation-specific harm (not just lower accuracy from corruption), score-vs-entropy conditional control, compelling distinguishing test, clear success and failure/stop.
6. **Contribution ledger**: 0–3 independent candidate claims; each with specific closest precedent, novelty delta, distinguishing test and essential ablation.
7. **Action cards**: next 3 actions, each `prerequisite → execution → saved artifact → interpretation`; the first action does not depend on inaccessible assets.
8. **Confidence/limitations**: source for facts, explicit UNKNOWN/TODO vs VERIFIED/PLANNED/EXECUTED; no invented observed effect, resource estimate, code path or acceptance rating.

## Zero-fluff self-audit, recommended

Before returning, for every paragraph ask: "Will this change a research decision or enable an implementation/test?" Remove paragraphs with generic AI praise, untestable novelty claims or mere section headings. For each invented method noun demand a definition; for each formula demand what is observed and what is differentiated; for each experimental claim demand actual run evidence. Trim large matrices and status dumps; put optional detail in appendix.

## Simulation cases to rehearse

A. **Incomplete multimodal TTA**: test class-pair evidence claim, whether loss can really protect shared parameters, unseen labels and O(C²). Prefer E0 and a minimal baseline if observable evidence estimator unproven.
B. **Alleged new confidence-gating paper**: challenge already-known sample filtering/candidate-label methods; no 3 fake contributions. Decision PIVOT unless genuine additional operator/prediction established.
C. **Unavailable dataset/checkpoint**: no imaginary 7-day code schedule. Verify links/license/weights/data mapping and propose targeted first-action checks or STOP.
D. **Non-DL or theory**: do not demand a neural loss/GPU; replace with precise materials characterization, mathematical proof obligations or field-specific intervention/controls.

This is a role-play and a local checklist, NOT evidence that the plugin ran as an independent external researcher, not proof of original novelty and not a measured end-to-end model quality score.
