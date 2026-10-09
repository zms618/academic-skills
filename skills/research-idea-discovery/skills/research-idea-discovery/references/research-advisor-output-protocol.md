# v3.4 addendum — Portfolio first when user asks broad discovery

The final report described below applies **after a shortlisted motivation survives**. New DISCOVER/OPEN_EXPLORE requests seeking CVPR Best Paper-level questions first need two earlier human-facing deliverables: (1) Motivation Landscape, which compares genuinely distinct problem cards with real sources and scientific necessity; (2) Shortlisted Gap Investigation, which shows established explanations, closest methods, unresolved testable gap and adverse results for 2–3 shortlisted problems. An archive of M0 pass flags is not a substitute. If no gap survives, do not output a fictitious method plan; provide negative results and next targeted evidence checks. Details in `motivation-portfolio-and-cvpr.md`.

# Research Advisor Output Protocol v3.2 — USER-FACING MANDATORY DELIVERABLE

## v3.3 First deliverable: scientific problem, not idea

Before report sections 1–11, output a compact **M0 Motivation Evidence Card**: concrete task/failure; source+Table/Figure+setting; why it matters; strongest matched baseline; two non-novel alternative explanations; first no-new-model falsifier; M0 verdict. For PROBE_ONLY/RESEARCH_MORE/REJECT_OR_REFRAME, do not include method/Loss/contributions or extensive feasibility plans; replace the ordinary candidate report with a neutral problem-evidence reading/measurement task and condition to revisit. Full downstream report is allowed only once M0 PASS_FOR_IDEATION. Maintain M1/M2 independent rechecks.

The final answer is a **mentor's actionable research memo**, not a dump of M1/N/L/M2/S audit logs. Applies when user requests a complete Idea Discovery/Refinement outcome. Keep modest length in STANDARD mode and provide DEEP audit details only when they are useful. User must understand the idea and know an E0 next step without rereading.

**First paragraph (mandatory, 3–5 lines):** Current decision/status; one-sentence intuitive Idea; why it is worth testing and the single biggest unknown; first real action. DO NOT lead with a 20-paper matrix or four new English modules.

## Mandatory readable sections, in order

1. **导师结论**: PROMISING_SEED / CONDITIONAL_CANDIDATE / STRONG_CANDIDATE / NEEDS_EVIDENCE / HIGH_RISK / REJECT; GO_E0 / REFINE / PIVOT / STOP / RESEARCH_MORE. Strong must mean evidentially defensible, not a fabricated venue promise.
2. **30 秒人话 + 一个对照例子**: task input→output, ordinary existing decision, A and B under one superficially same feature but different hypothesized information; label invented numbers 玩具示例.
3. **Motivation**: real importance → confirmed or hypothesized failure → why existing strong method might fail → one refined question. Do not misstate nearest papers.
4. **现有工作与撞车风险**: 2–5 named verified (or explicit UNVERIFIED) near-neighbors, what they genuinely do, what remains unproved. Do not invent novelty gap.
5. **可证伪的科学假设与 Potential Contributions**: 1–3 possible contributions with novelty/evidence statuses and required discriminating experiments; no forced three.
6. **科学故事线**: observation→failure→possible cause→insight→method→supporting/needed evidence. At least one alternate explanation; separate hypothesized cause from verified fact.
7a. **方法的可实现细节（MANDATORY on full research/method request）**: One minimal method, operational score from observable data without test labels, I/O, module integration, training vs test-time two-step update, Loss or algorithm with gradient target/frozen weights and explicit unknown hyperparameters, inference fallback, O(class/time/memory) costs, hardest technical assumption, and an actual unit test/first edit to make. If mechanism cannot be identified/implemented without labels or source data forbidden by protocol, mark METHOD_NOT_READY and propose E0 rather than fake code.
7b. **Method alternatives and independent contribution check**: M0 simplest no-new-model solution, M1 smallest candidate method, M2 only if necessary; for 1–3 distinct potential contributions cite closest collision and unique decisive ablation. A graph or router is not a contribution by itself. Name one technical assumption that could make mechanism impossible.
7. **可行性落地表**: primary and backup **specific dataset** (if identifiable), official links, actual availability/license/status; **one matching checkpoint/backbone**, source, freeze/update strategy; Source + simple rival + most relevant reproducible strong baseline, and matching eval protocol. Unknown items must be explicit, not blank or "完全可行".
8. **马上做的 E0（48 小时内的可执行检查）**: five numbered micro-steps with inputs, artifact/metric, GO/NO-GO; if access unverified, step 1 must actually check access. Time target is organizational, not guaranteed execution duration.
9. **第一周计划与 Kill Criteria**: actionable days 1–7 with artifact and dependency; at least "problem absent", "simple rival solves it", "no data access" as appropriate. Specify what changes if failed.
9a. **研究员试用审查**: What exact file/data/checkpoint to inspect, what function to implement, input/output, saved artifact and falsifying result; include red-team review and fix identified blanks BEFORE final report. Simulated, not real external execution.
10. **最大审稿反对意见 + 审稿对策**: 2–3 mechanistic attacks and experiment/verification for each, not invented acceptance ratings.
11. **最后一句人话总结 + 导师下一步建议**: "以前…现在…下一步先测…".

Completeness is not proven validity; never promise paper acceptance, pretend model checkpoints or datasets were actually downloaded, or tell the user to obtain data without having searched. For QUICK, compress to fewer paragraphs but always provide sections 1, 2, 3, 7, 8, 9, 11. For detailed follow-up Q&A, respond to the question and don't force report outline.

## No-good-Idea route

If none meets standard: say NO_DEFENSIBLE_IDEA_FOUND; show why top candidates failed in 2–4 clear lines, the **specific missing evidence**, an actionable cheap check if possible, and a targeted, complete copy-paste Deep Research prompt using existing handoff protocol. Do not invent a strong candidate or fill potential contributions for a rejected idea.

If answer is empty jargon, absent operable estimator or unrealistically certain about source vs test-label access, return to the method-design gate and rewrite, not a polished but false final.


## v3.5 paper-anchored final result
Add a concise Research Lineage section **before method design**: anchor source and Figure/Table, exact validated vs conjectural observation, strongly contradicting follow-up papers, unresolved question and first no-new-model test. Preserve user-facing plain-language summary and shortlisted motivations. For applied researchers, state reuse-ready assets with real access status and conditional day-1/day-14 GO/STOP checkpoints. Explain if the chosen scientific question is impactful but difficult to run, or easy but incremental. When no paper source supports the gap, disclose that before proposing network changes.
