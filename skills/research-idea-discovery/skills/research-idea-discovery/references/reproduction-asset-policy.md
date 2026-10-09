# v3.5 Reproduction Asset Gate — source code is not a running experiment

For each shortlisted anchored direction identify one fair executable experimental stack or explicitly mark which facts are still unavailable.

**Asset card**: exact task/modality/label protocol; dataset name/version/official URL and license, data access/actual domain split; official code URL/license/commit, entry/config TO_LOCATE if not inspected, environment compatibility; specific checkpoint and matching preprocessing/class mapping with load status; Source/ERM, simplest rival and strongest comparable method, same data/split/metric; compute/storage estimates only if measured or attributable to a source.

Resource statuses: `DISCOVERED_LINK`, `LICENSE_CHECKED`, `CONFIG_INSPECTED`, `WEIGHTS_LOCATED`, `WEIGHTS_LOADED`, `MINI_INFERENCE_EXECUTED`, `BASELINE_REPRODUCED`, `BLOCKED`. Higher status requires actual evidence/logs and must not be inferred from a lower status or from a filled field. Medical data approval/ethics gates cannot be bypassed; multi-sequence images and image+EHR are not interchangeable setups.

A 14-day **decision** schedule, resource dependent: days 1–2 read anchor evidence and inventory data/weights; 3–5 verify legal access and minimal inference; 6–8 replicate the *problem* under matched condition; 9–11 test simple confounders, null hypotheses and minimal interventions; 12–14 GO/REFINE/PIVOT/STOP, choose one method if problem survives. Stop at access blockers; do not spend a week pretending a model is runnable.

Final actionable handoff must answer: which Table/Figure next; which exact repo/config to inspect (or honestly TO_LOCATE); what smallest experiment; what CSV/JSON/log it creates; what result would abandon this motive. Label all planned commands as plans, not executed runs.
