---
name: research-execution-planner
description: Convert a selected research hypothesis into an accessible-dataset and model-based validation plan with compatible baselines, 48-hour E0 pilot, first-week steps, resource evidence, and explicit kill criteria. Use after evidence and feasibility investigation.
---

# Research Execution Planner — 从 Idea 到明天能做什么

Read `../research-idea-discovery/references/research-execution-protocol.md` and `../research-idea-discovery/references/experiment-protocol.md`.

Plan concretely, but do not imply the plan was executed:
1. Choose **one default reproducible stack**, not a random shopping list. Give exact official dataset/task/split, needed modalities/labels, license/access evidence, linked code repository and model checkpoint, matching architecture, evaluation metric and protocol. Add fallback only if supported.
2. State one Source/no-update baseline, one simple rival (freeze, skip, confidence threshold, reset, entropy, etc.) and strongest mechanism-near prior model on **fair compatible inputs**; flag infeasible replications and avoid comparing published metrics across incompatible splits.
3. State frozen/updatable parameters, label visibility during TTA, software/hardware budget and reasons. Never invent hours/VRAM; label UNKNOWN or measured source.
4. Design E0 **before** training anything novel: a brief step-by-step, precise data preprocessing, controlled shift/failure, recorded metrics, comparison and stop/continue decision. Keep offline annotation/oracle analysis separate from online unlabeled updates.
5. Write action-oriented 48-hour checkpoint and 7-day plan; every step has inputs, output artifact, and go/no-go.
6. Write at least two falsifiers including "target phenomenon absent" and "simple baseline solves it", plus access/compute blockers.
7. If access is not verified, first action must be data/card/checkpoint availability inspection; no fictional download or model compatibility.

Complete report also needs human-friendly motivation and paper story from `research-idea-explainer`. If no data path, recommend PIVOT/STOP/RESEARCH_MORE, not a seven-day implementation fantasy.
