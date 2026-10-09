# v3.2 研究生真实使用场景的桌面模拟（含负面审查）

> 模拟性质：一位研究生要求「研究部分模态缺失时，TTA 会错误更新语义类别边界；请提出三个创新点和方法」。这里是**角色扮演/桌面审计**，没有训练模型、没有实测精度、没有独立 GPU 执行。URL 来自 2026-10-09 的公开查询；仍需本地数据、许可及模型参数核验。任何数字用于讲原理均是 TOY。

## Reviewer verdict

**REFINE + GO_E0 / NOVELTY UNVERIFIED**。已有 UniModalShift 模态选择、DASP 稳定/可塑 TTA、MiDl 缺失模态 TTA、SuMi 多模态噪声 TTA 和 PASLE 候选伪标签。"选择性更新"、"信息丢失"、"避免错误伪标签"都不新；主张必须缩到：测试输入中**类别对层面**可判别性变化对 TTA 错误更新的增量解释能力（在熵/置信度/模态质量控制之后），且有无标签可观测代理。

## 30 秒人话

视频没了，音频还能区别狗叫和关门，却不一定能区别开门和关门；把一个样本直接叫做"可信/不可信"可能太粗。研究问题是：**能不能知道哪些类别边界还有依据，并只在这些地方让模型自我更新？** 这仍是未经实验确认的科学假设。

## Hypothesis and its most dangerous flaw

H1：匹配整体置信度、模态质量和伪标签策略后，类别对的任务证据代理分数仍能预测测试时更新伤害。H0：代理只重复置信度/模态质量，并无增量信息；或者源模型本身已足够鲁棒，无明显 adaptation-induced harm。若 H0 成立，停止方法开发。

**信息不可辨识**：如果只剩模态对开/关门不含区分信息，任何无额外数据的方法不能凭空恢复标签。正确目标是减少自强化和校准不确定性，不是"修复所有边界"。

## Method alternatives, NOT three fake innovations

M0：Source frozen + confidence threshold / skip-update (强简单对手)。
M1（首选候选）：从 source validation 的各模态类别对判别先验和无标签输入的可观测稳定性，估计每个 (i,j) 的 proxy e_ij(x)。**源域先验不等于当前样本证据**；是否有效必须由 E1 检验。条件于相同熵/模态可靠性评估其预测错误更新的增量价值。
M2（只有 M1 成功才做）：小型 Adapter 的边界选择性目标：较高 e_ij 且 pseudo ordering 稳定的 pair 用停止梯度 teacher margin 作目标；低 e_ij pair 仅惩罚相对冻结 source 的 margin 幅度增大；Adapter 接在实际代码融合路径（待代码检查确定），不能声称低 e_ij 的共享参数绝对不变。

### Proposed math (illustrative, not proven)

```
score_ij = f(source_pair_prior_ij, available_modality, sample_stability_ij)
margin_ij(theta,x) = logit_i(theta,x) - logit_j(theta,x)
L_supported = sum_{(i,j) with score high} w_ij * D(margin_ij(theta,x), stopgrad(teacher_margin_ij(x)))
L_limit = sum_{(i,j) with score low} max(0, abs(margin_ij(theta,x)) - abs(margin_ij(source,x)) - delta)^2
L = L_supported + lambda * L_limit + mu * parameter_regularizer
```

Here `f`, `D`, teacher confidence / threshold / calibration, and memory/time budgets are open design questions; no claim the above ensures improvement. `teacher` may itself be wrong. Preserve direction versus preserve magnitude is a design choice to test. Labels at TTA are not used. All labels used to evaluate pairwise errors are offline only.

## Conditional contributions — do not force 3

1. *Diagnostic finding (E0 pending)*: pairwise semantic discriminability predicts update-caused harm beyond conventional confidence/missingness measures. Compare within confidence strata; stratified AUC/reliability and paired harm rates. If no residual effect, REJECT.
2. *Minimal mechanism (E2/E3 pending)*: a simple observed pairwise proxy conditionally gates adaptation while controlling changes in unsupported margins. Compare to source freeze, threshold, candidate-label strategies; paired seed-aware metrics, efficiency, ablations of proxy and protective term. If equivalent to simple rival, MERGE/STOP.
3. *Optional protocol contribution (not yet independent)*: only if genuinely new benchmark/diagnostic protocol, enough representative cases, and evaluation uptake. Otherwise no third scientific contribution.

## Concrete starter stack and risk

- Candidate: Kinetics50-C / audio+video via https://github.com/he4cs/DASP . The README documents dataset archives, corruption generation, model checkpoints and config entries; **availability, license, local runnable compatibility NOT VERIFIED**.
- **CHECKPOINT MAPPING RED FLAG**: DASP README external resources table and destination filenames appear to swap names (Kinetics50 table shows `cav-mae-ft-vgg.pth` while directory names use `cav-mae-ft-ks50.pth`). DO NOT guess. Inspect actual config, checkpoint keys, final classifier output and label mapping, verify class count before inference. Do not automatically use the VGGSound checkpoint with Kinetics labels.
- Baselines: Source frozen and DASP config in same stack; threshold / skip update locally added and controlled. PASLE is conceptually dangerous but **its original code does not automatically run on CAV-MAE Kinetics50**. Implement only a fair matched-control equivalent after checking methodological assumptions.
- Modality *missing* is not the same as synthetic Gaussian corruption. Need explicit mask/zero-fill/missing-token acceptance and genuine information removal protocol; if the model cannot accept missing inputs, report as BLOCKED and first test corruption-only condition without rebranding it as missing-modality.

## First executable researcher actions (no fictional download)

1. Open DASP README + configs + checkpoint metadata; inspect and write `artifact_inventory.csv`: URL, access, license, dataset labels, `state_dict` shapes/classes, preprocessing, memory limits, unresolved issues. If mapping unresolved, STOP before training.
2. On truly available small legal subset, log source predictions and paired sample ids for clean, audio-only corruption, video-only corruption, and missing-modality conditions only if supported; produce `predictions_source.csv`.
3. Run paired *unadapted vs adapted* predictions on **same corrupted inputs**, track accuracy and per-pair confusion, confidence-stratified error flips, stability and severe corruption. Produce `e0_harm_by_pair.csv`. Test labels used only offline; no test-label-driven tuning.
4. Compare against skip-update/confidence and matched modality gating controls; plot stratified residual explanatory power; if no pair-specific effect remain, **PIVOT/STOP**.

## Four real PhD-student objections caught

- "What exactly is the per-pair score?" → f must be operational and measured without target labels; until then, NOT IMPLEMENTATION READY.
- "Can a pair mask really freeze an unrelated boundary?" → NO, gradients through shared weights can interfere; add low-pair margin drift diagnostic, maybe gradient constraints, never claim exact isolation.
- "What happens at t+1?" → keep last Adapter, update using unlabeled current batch; recompute per-sample score and teacher with a documented snapshot policy; reset on shift as controlled alternative. Cache only allowed source statistics and teacher states.
- "Are three modules three scientific contributions?" → NO. Without independent novelty and falsifying tests, report two *potential* claims or one method claim rather than three.

This example is a template of useful reasoning and reproducibility caveats, NOT a completed empirical research result.
