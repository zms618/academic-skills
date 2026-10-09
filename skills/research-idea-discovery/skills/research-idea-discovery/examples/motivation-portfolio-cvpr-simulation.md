# v3.4 adversarial example: CVPR-aspiring Multimodal Domain Generalization

**This is a desk-based research scenario, NOT verified evidence for real paper metrics.**

Research question universe (DO NOT treat explanations below as established):
1. **Fusion hurts after unseen-domain shift.** Is a multimodal predictor sometimes worse than the better single modality under matched source and target conditions? Mundane alternative: one noisy modality, unfair model size or tuning. Test same backbone/seed and single-modality controls. No invented benchmark values.
2. **Complex MMDG loses to ERM.** Are some purported generalization gains fragile to strong reproducible ERM? Mundane alternative: unequal tuning/model-selection or data splits. First action: verify official benchmark tables and match resources. One table with unmatched conditions is `PROBE_ONLY`.
3. **Training-domain cross-modal correlations fail in target domain.** Does learned cross-modal co-occurrence shortcut dominate invariant task evidence? Alternative: source label imbalance, modality preprocessing. Need paired counterfactual/control or independent domains.
4. **Multimodal performance hides subgroup failures.** Does aggregate accuracy conceal reproducible harm in low-evidence category relationships? Alternative: scarce subgroup samples and random variability. Need confidence intervals and several seeds.
5. **Strong pretrained models can erase gains of specialized DG.** Is the observed DG failure regime dependent on backbone scale/pretraining? Alternative: incomparable pretraining datasets or contamination.
6. **DG benchmark shift semantics do not match deployment.** Are benchmark corruptions mostly superficial whereas deployment shifts change causal information? Alternative: benchmark claims only specific coverage; verify intended scope rather than attack a straw man.

Do not label the six descriptions true without original paper Table/Figure and matching settings. These are 6 **candidate questions requiring evidence**. Compare their distinct failure families and supply `source_status` for each; retain only 2–3 deserving M0. For example one might prioritize #2 (simple-baseline contradiction) and #1 (fusion negative transfer) IF official tables support them; #3 remains a conceptual high-upside probe, not a proven fact. After a neutral first-pass M0 check, retrieve relevant nearby mechanisms on BOTH surviving questions and remove whichever prior work fully explains. Only then invent a necessary method. Report `NO_DEFENSIBLE_MOTIVATION_YET` if needed.

### Bad output that must be rejected

"Our best paper will solve multi-modal DG with three innovations: asymmetric router, causal relation graph, adaptive gating. This is novel and solves all unknown shifts." **Failure:** no located paper result, no class of affected samples, no fixed protocol, no reason for method, no rival, no unique scientific observation.

### Useful output

"Current state: 6 hypotheses, 2 source-located phenomena, 1 counterevidence, 3 uncited leads; 2 shortlisted for neutral gap research. For each, show original table locator, matched protocol caveats and a no-new-model falsifier. No methods approved yet." All numbers in this quoted illustration refer only to the *invented trial scenario*, not published literature.
