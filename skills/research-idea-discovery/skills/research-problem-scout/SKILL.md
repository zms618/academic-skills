---
name: research-problem-scout
description: Use at the beginning of scientific idea discovery to find real, important, falsifiable research failures from actual sources; reject weak motivations before architectures and novelty-hunting. Includes low-cost problem-evidence scouting and a hard Motivation-First Gate.
---

## v3.4 portfolio discovery extension

For `CVPR_BEST_PAPER_ASPIRATION` or multi-motivation discovery, call `research-motivation-portfolio` first. Build a broad, source-grounded **portfolio of different questions** (default 5–8 honest motives) then explain why 2–3 have more important, defensible shortcomings, and research nearest prior work for every shortlist member. Only after this can you turn a surviving motivation into a technical Idea. See `../research-idea-discovery/references/motivation-portfolio-and-cvpr.md`. A strong single-problem analysis alone is not a completed portfolio-first discovery.

# Research Problem Scout — 先找真问题，再考虑 Idea

Read `../research-idea-discovery/references/motivation-first-gate.md`, `../research-idea-discovery/references/motivation-and-story-protocol.md`, and `../research-idea-discovery/references/search-connectors.md`.

Perform bounded, neutral reading of actual benchmarks, strongest simple baselines, counterexamples, negative results and matched-condition comparisons. Produce up to three **problem cards**, not method proposals. Seek adverse data as actively as supportive data. Cite each Table/Figure/setting or prove evidence is unavailable. Never claim the root cause was discovered from one comparison.

Rank by **problem evidence quality and scientific importance**, NOT how easily three innovations can be invented. Explicitly test the null explanation: “Would fair tuning, a different metric or a matched backbone make this disappear?” Check dataset and regime scope to avoid overgeneralizing from one condition. This cheap scan may precede resource-intensive dataset feasibility; do not impose downstream G0 before deciding which problem merits further work.

For each problem call the structural `scripts/motivation_gate.py` when local commands are available, but also critically read its sources. The script cannot independently verify citations or scientific importance. Output PASS_FOR_IDEATION / PROBE_ONLY / REJECT_OR_REFRAME / RESEARCH_MORE; only PASS may trigger the Hypothesis Lab to generate IDEA_SEED and the costly D0/G0/N/L/M2/method design workflow. For PROBE_ONLY, offer one bounded fairness/replication check and a stop condition, with no method architecture. If all fail, report why and one targeted neutral Deep Research prompt. Label any role-playing review `ROLE_SIMULATED`.

## v3.5 paper-anchored probe
Use `research-paper-anchor-scout` for quick-start research: ask counterfactual questions at each real Figure/Table, replicate failures, investigate why successful methods work, and reconcile paper disagreements fairly. All still require M0; manuscript limitations or a method's popularity alone are not established failures.
