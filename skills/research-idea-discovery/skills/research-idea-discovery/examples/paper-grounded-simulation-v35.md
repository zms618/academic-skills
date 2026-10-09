# v3.5 Researcher Desk Simulation — problem-driven AND method-driven (toy case)

**This is a simulated reasoning exercise, NOT a literature verification or a completed run.**

Researcher focus: low-compute multimodal DG; medical preferred; CVPR best-paper-quality scientific standard. Start with benchmark/failure paper, recent strong mechanism paper and critical contrasting paper. The titles MMDG-Bench/MER-DG/DrFuse are example *leads*, not automatically compatible model baselines.

1. **Paper reading plus questions.** A benchmark paper reports an aggregate comparison. Before explaining why complex DG methods sometimes trail ERM, locate exact table, dataset/domain splits, model and optimizer selection. If incomparable: `PROBE_ONLY`, not a robust phenomenon.
2. **Success reverse-engineering.** A method reports a regularization gain. Investigate whether it changes invariance, reduces overfit, acts as generic entropy regularizer or differs in hyperparameters; test an ordinary regularizer, matched-budget simple rival and one controlled intervention.
3. **Apparent contradiction.** If one paper claims fusion helps and another reports degradation, check modality, task, setting, benchmark version, source domains, target domain, metric and training budget before claiming science contradicts.
4. **Method-driven temptation.** A researcher suggests applying Mamba/GRPO/graph routing because they are popular. Without actual motivating evidence, pause at M0; if useful, treat a method as an exploratory hypothesis, not an independent motivation.
5. **Practical next action.** Locate a specific table and confirm code checkpoint/data access before promising new training. Record: paper locator → experiment assumptions → observed vs hypothesized comparison → baseline to run → CSV or log to save → kill condition.

**Advice:** A high-impact question with limited assets can remain promising but blocked; an easy-to-code baseline with no unresolved scientific claim is fast but not CVPR best-paper-level. Do not blend the two into one score. If no reliable paper evidence survives, report NONE and return to evidence scouting.
