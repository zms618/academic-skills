---
name: research-paper-anchor-scout
description: Critically read a small adversarial group of anchor papers to discover real, falsifiable research problems from failures, successful-method mechanisms, contradictions and deployment assumptions; reuse verified assets without blindly modifying the previous network.
---

# Research Paper Anchor Scout — paper-grounded problem discovery

Read `../research-idea-discovery/references/paper-lineage-and-critical-reading.md` and `../research-idea-discovery/references/reproduction-asset-policy.md`.

- For fast-start DISCOVER, make an adversarial set of 3–5 papers with different roles: anchor, benchmark/negative result, strongest rival or counterexample, explanation paper, optional cross-field analogue. Don't force quantity when literature unavailable. User-supplied papers count.
- **Read and question simultaneously**: task, train/test domain protocol, exact Table/Figure, non-positive result, assumptions, nearest contradicting paper, follow-up citations, genuine code/data availability. An abstract or Limitations section is a lead, never proof of failure.
- Four core operators: `FAILURE_REPLICATION`, `REVERSE_ENGINEER_SUCCESS`, `CONTRADICTION_TRIAGE`, and `DEPLOYMENT_TO_SCIENCE`. Contradiction requires comparable split/backbone/metric/pretraining/compute; otherwise `APPARENT_CONTRADICTION` and a fair-match probe.
- Maintain source lineage: paper → located evidence → question → null explanations → cheapest falsifier. Deduplicate question families before creating 5–8 motivations; keep adverse evidence next to supporting evidence.
- Method-driven ideas may seed a candidate explanation, but **must re-enter the independent M0 problem gate** before research is invested. A fashionable technique never justifies a research problem.
- Prefer public datasets, usable official code/checkpoints and same-protocol strong simple baselines. No claimed runtime, loaded weights or verified failure without logs.
- Produce a concise paper-lineage table, a problem portfolio and an executable no-new-model probe; not a method first. Use `scripts/paper_anchor_audit.py` for structural checks when available; its PASS does not establish source truth.
- CVPR Best Paper remains an aspirational quality bar, never an award likelihood estimate. If nothing survives, return real negative findings and bounded next reading instead of three made-up innovations.
