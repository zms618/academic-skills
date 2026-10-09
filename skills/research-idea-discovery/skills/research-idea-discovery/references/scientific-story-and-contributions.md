# Scientific Story and Potential Contributions — Evidence First v3.1

## Scientific story as a causal chain (NOT marketing)

Show in simple words first, then 5–7 linked steps:
**Observation** (measured or HYPOTHESIS), **Existing baseline's actual decision**, **Failure** (observed or pending), **Possible root cause** (competing explanations + confounders), **Insight** (the decision we should change), **Proposed mechanism** (operational input / output / estimate), **Evidence** (E0, rival and decisive experiment). Each arrow needs justification and at least one attempted counterexample.

A story is PROVISIONAL until run results actually support it. Hypothesis becomes justified conclusion only within tested conditions, never from narrative coherence alone.

## Contribution ledger (usually 1–3, not forcibly 3)

For each candidate contribution output:
- **Type**: new problem/protocol, mechanism, theoretical result, distinctive experiment/benchmark, empirical finding.
- **One sentence**: concretely changed scientific or engineering behavior; no module naming as a contribution by itself.
- **Closest prior work** and mechanism delta (verified, unresolved, collision risk).
- **What new evidence would prove it**: experimental/theoretical and required fairness controls.
- **Status**: PROPOSED, NOVELTY_UNVERIFIED, EVIDENCE_PENDING, SUPPORTED_WITH_SCOPE, REJECTED.
- **Failure condition**: simplest rival equivalent, root cause false, data leakage, no obtainable benchmark, prior paper already does same thing.

If only one defensible contribution exists, output one strong candidate. "做了更多消融" and "代码公开" are not stand-alone scientific innovation. Do not claim "首次" unless appropriate near-neighbor evidence is complete and even then qualify search limitations.

## Reviewer attack

At minimum, ask "Is this merely calibrated uncertainty?", "Does freeze/skip/reset achieve the same?", "Does the dataset have sufficient task evidence at all?" when relevant. Customize to field instead of imposing these examples on non-ML research. Provide one feasible falsifying experiment per rejection argument, with available benchmark paths/UNKNOWN flags.
