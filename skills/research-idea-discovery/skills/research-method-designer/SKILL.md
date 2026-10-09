---
name: research-method-designer
description: Design and adversarially validate an implementable scientific method from a research motivation or selected idea. Requires operational estimators, interfaces, objectives, update timeline, strongest simple alternatives, code integration plan and decisive experiments; avoid module stacking and unsupported claims.
---

# Research Method Designer — 真的推导方法，不是给模块起名

Read `../research-idea-discovery/references/method-design-and-necessity.md` and `../research-idea-discovery/references/researcher-value-acceptance.md` alongside prior-art and feasibility protocols.

## Researcher-mode question

For every proposed mechanism, answer: **"I could write which function, pass which data into it, optimize what, and check what tomorrow?"** If the answer is not concrete, it is a mechanism idea, NOT an implementable solution.

1. Start from ONE falsifiable failure mode, strongest known baseline and two alternative causal explanations. Write the exact measurable behavior the mechanism is intended to change.
2. Consider THREE competing mechanisms, not automatically three innovations: (a) no-new-model strongest simple baseline; (b) minimal novel mechanism; (c) more complex mechanism only if a clear distinct prediction justifies it. Evaluate simplicity, plausibility, prior-art collision, observability and compute. Choose ONE default build.
3. Produce a **Method Specification**: task/domain; known and unknown input/output types/shapes; precisely defined score/estimator and its label/data access; module connection point to a *verified* codebase; objective terms and gradient target; inference vs adaptation time sequence; teacher/anchor/cache origin; failure/abstention behavior; computational complexity and resource uncertainties. Use pseudocode or readable formulas, marked PROPOSED; no invented architectural dimensions.
4. For each potential contribution (1–3, do not force) include **what changes compared to closest prior, an independently testable prediction, one necessary ablation, status and evidence required**. If C1 and C2 measure exactly the same mechanism, merge. Dataset curation, experiments, or new module names are not automatic innovations.
5. Rule out pseudo-label leakage, oracle supervision, target-label-based threshold tuning, test-order leakage, checkpoint/dataset mismatch, and any source-data assumption not supported by the chosen TTA setting. Unknowns remain blockers.
6. Specify exactly HOW an implementer finds/inserts code (filename/function if actually inspected; otherwise mark as TO_LOCATE rather than invent). Start with an E0 that uses source and simple-rival predictions before new training.
7. Offer RED TEAM reviewer and researcher objections. If independent source cannot observe proposed latent information, discuss the identifiability limitation and what external signal would be required.
8. Report STOP/REFINE/E0 decision based on real evidence, not a ready-looking flowchart.

Do not imply this skill can run any external repository by itself. If the user only asks a small follow-up, respond narrowly. If domain is not deep learning, translate 'model/loss/gradient' into the domain's actual operational equations, instruments, controls and proof steps.
