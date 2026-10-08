# Research Idea Discovery release history

## v2.7.1

- Fix pilot stdout checksum verification on Windows by hashing the exact UTF-8 bytes written to disk.

## v2.7.0 — Execution-evidence gates and regression checks

- P0: Separate dataset catalog/field declarations from evidence of actually reading a bounded local sample. Record SHA256 and parsed fields. Reject missing sample, HTML landing pages, placeholder URLs, and missing labels. Do not claim source/license/whole-dataset reproducibility from a sample check.
- P0: Guard REVIEW → PILOT with a recorded review decision tied to idea_id/revision. Guard PILOT → UPDATE with replayed run-log checks and measurements or documented failure. Reject dry runs, no-metric successes, and forged readiness flags.
- P1: Structured four-axis prior-art query coverage and source-locator records; no claim of exhaustive novelty. Coverage record needed before mechanism-logic phase when running local workflow.
- P1: Compare proposed and simple-baseline outcomes when evidence exists. Equal/worse results mark `requires_reaudit` and force renewed mechanism/motivation/story scrutiny.
- P2: Local append-only idea ledger with duplicate signatures; revising source evidence invalidates dependent assessments. Adds reproducible adversarial fixtures.
- 66 tests pass locally. These check control logic, not academic originality or real-world availability without network/tool permissions.

## v2.6.0

- Research Idea Discovery plus targeted manual ChatGPT Deep Research handoff and report return.
