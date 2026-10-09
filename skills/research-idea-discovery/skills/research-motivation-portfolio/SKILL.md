---
name: research-motivation-portfolio
description: Generate and compare several independently grounded research motivations before researching innovation points. Use when targeting major vision conferences or CVPR best-paper aspirations, scouting multiple scientific problems, or selecting a few defensible directions for targeted gap research.
---

# Motivation Portfolio & CVPR High-Impact Screening

Read `../research-idea-discovery/references/motivation-portfolio-and-cvpr.md` and `../research-idea-discovery/references/motivation-first-gate.md`.

This is a **problem comparison skill**, not an idea generator. Work on a family of 5–8 candidate motivations if available; disclose honest shortfall, source maturity, duplicates and contrary evidence. Quote actual numbers only when source verified; otherwise use descriptive qualitative cards. Evaluate scientific necessity, size of conceptual gap, vision-task relevance, potential broad impact, hypothesis falsifiability, strongest simpler explanation and cheapest decisive probe. Shortlist 2–3 (fewer if evidence truly warrants), ensuring each survivor is a different failure or hypothesis family. Do not invent three strong ideas merely to comply with a count.

Then review M0 per shortlisted motivation and perform targeted prior-art gap exploration **separately for each**, recording concrete prior claims, full-text status and which portion remains unresolved. If nearest work already solves the gap, explicitly remove that motivation and return to the backup; no method-first rationalization. Output a Motivation Landscape Report (before novel method proposals) and a Gap-Survivors Decision Report (before costly methods). When user requests CVPR Best Paper, treat it as a very high aspiration based on CVPR's research values, not official award criteria or a success probability. Run `scripts/motivation_portfolio.py` for structural validation when possible; its PASS never independently verifies papers or science.

## v3.5 literature ancestry (mandatory for paper-first discovery)
Each portfolio problem must name the source paper(s), exact experiment location and observed-vs-hypothesized distinction. Different papers can support the same scientific problem; deduplicate. Prefer independent refutation and post-publication follow-ups. Motivation ranking judges importance and evidence, not how quickly a hot mechanism can be dropped into code. See `research-paper-anchor-scout` and `references/paper-lineage-and-critical-reading.md`.
