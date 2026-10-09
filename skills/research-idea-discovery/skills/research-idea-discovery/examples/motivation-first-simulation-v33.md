# Researcher role simulation — M0 motivation gate v3.3

**Simulation, not actual reading of MMDG-Bench Table or running models.** Every example quote/number below is an invented prompt fragment. None constitutes independent literature verification.

## Case A — weak idea-first path: STOP

Proposed title: "Unseen Modality Shift Composition Adaptation". User gives no located table/figure/benchmark experiment or task-level harm, only "shift composition is common and DG needs robustness." This describes an interesting intervention but does not establish that a strong existing baseline genuinely fails under a matched setting. M0: `REJECT_OR_REFRAME` (no observed failure, no falsifier). **Output must not contain** a router, loss, three novelty points, or dataset/backbone full proposal. Redirect to neutral search of genuinely surprising benchmark failures.

## Case B — one potentially important table: PROBE_ONLY

User says: "On one benchmark table, ERM beats multi-modal DG method X in a target domain." Without the original Table, metric, split, backbone/training budget and replication, treat as user-reported `HYPOTHESIZED`; do not present numbers. M0: `RESEARCH_MORE`. If table is actually read with a precise locator and confirms matched values, status can become `PROBE_ONLY`: a single comparison is not evidence for a general mechanism. Proposed minimal check: reconcile implementation/budget and validation strategy, recompute paired ERM and method-X on a small matched sample, log per-domain/per-class accuracy and seeds. Null result -> retire this problem as an innovation anchor, not rename it.

## Case C — multiple independent, matched failure observations: conditional PASS FOR IDEATION

Two distinct sourced/matched results in a **fictional testing fixture** and a measurable failure/stakes/controls/falsifier support M0 *structural* PASS. Then, and only then, examine D0/G0 and the strongest relevant DG papers before hypothesizing a mechanism such as spurious cross-modal shortcuts. **This does not prove the shortcut hypothesis or originality**. A validated implementation could still refute it during M1/M2.

## Adversarial reviewer question

"Why is one surprising leaderboard score scientifically important rather than a hyperparameter artifact?" If the plugin cannot answer with source locator, matched protocol and competing explanations, it must say `PROBE_ONLY/RESEARCH_MORE` and stop downstream spending.

## Researcher utility

A meaningful negative decision is: `Do not implement the new graph. First locate the actual benchmark table, verify equal backbone/split/metric/training budget, then extract a two-column per-domain difference CSV; if the reversal disappears, PIVOT.` This is useful; a five-page optimistic method plan would be wasteful.
