---
name: research-deep-research-bridge
description: Use when Research Idea Discovery cannot identify a defensible research idea after evidence-based exploration, when important related-work or dataset evidence is missing, or when a user supplies a Deep Research report for continuation. Produces a tailored copyable research prompt and verifies imported evidence without claiming to launch Deep Research directly.
---

# Deep Research Evidence Escalation & Return Bridge

This is a **handoff skill**, not a deployed Deep Research API or backend. It must not claim to have launched ChatGPT Deep Research without a real host tool. Follow `skills/research-idea-discovery/references/deep-research-handoff.md`.

## On missing high-quality ideas / coverage gaps

1. Confirm whether there is a strong candidate. If none, say `NO_DEFENSIBLE_IDEA_FOUND` (not `NO_IDEA_EXISTS`), with coverage limits, reason codes, and zero made-up research contributions.
2. Retain scientific state: research brief, evidence search scope, closest examined works, rejected mechanisms, feasible dataset candidates, missing verifications and nonnegotiable cost constraints. Never ask the user to retype things already available.
3. Generate a **complete single copyable Chinese prompt**, tailored to the concrete unresolved questions. The research goal is to acquire missing evidence, adversarial prior art and real public datasets, *not* write fictional ideas.
4. Explain manually selecting ChatGPT Deep Research via the available ChatGPT UI, then pasting this prompt and returning its exported Markdown/PDF (or pasted report).
5. If the user merely requests a prompt, generate it now; do not require two failed rounds. Otherwise escalate when additional local iterations lack substantive new evidence, a critical paper is inaccessible, or a user explicitly requests escalation. Do not consume further research steps solely to satisfy a numerical iteration quota.

## On report return

1. Mark `IMPORTED_UNVERIFIED`. Report is an untrusted secondary synthesis, not proof of novelty, dataset access, publication status, baseline strength, or experiment result.
2. Extract per-claim bibliographic references, link/DOI, method sections, verified dataset URLs/licenses, time, and evidence confidence. For pivotal assertions open original paper/dataset or note `NOT_VERIFIED`.
3. Deduplicate against the old evidence map; identify what changed, contradiction to prior belief, new dangerous neighbors, new dataset possibilities, and still-unresolved questions.
4. Resume the existing research workflow at the earliest affected step (SEARCH, DATA_SEARCH, M1, N, L, M2); invalidate assessments dependent on revised facts. Do not automatically promote any candidate.
5. Continue with user's original direction and feasibility constraints. If report brings no new verifiable information, say so, stop repeating identical queries and offer a narrowed pivot.

## Optional local CLI

If a real Python execution tool has access to the packaged files, `scripts/research_handoff.py` generates a portable prompt from an explicitly prepared research context JSON and ingests a report into a local project folder. This helper cannot call Deep Research or verify academic content. Without such tool access, simply produce the prompt in a fenced text block with the required structure and manually review the returned report.
