# Plain-language idea teaching protocol v3.1

Goal: in 60–90 seconds of reading, an ML graduate student can explain why this project matters, what the model sees, why the status quo may fail, and how the new idea differs.

## Four-pass delivery (must proceed in this order)

1. **One-sentence intuitive research question** with subject, event, mistake, desired change. Avoid abbreviations unless already defined.
2. **One concrete scene**: an existing real task, concrete inputs/outputs, and two conditions A/B. Invented numbers or idealized examples must say "教学假设". E.g. two predictions both 0.9 confidence do not, by themselves, prove different evidence availability. Define ground-truth-supported discrimination only as an offline measurable target or as an unverified hypothesis at test time.
3. **Old approach and its limitation**: show what strong existing baselines actually optimize/decide with citations or mark the interpretation as hypothesis. Contradict common oversimplifications, e.g. not all TTA techniques minimize entropy or use confidence thresholds.
4. **New scientific question + one minimal mechanism**, with input/output, what is decided, what is frozen/updated. Only after the analogy should terms like pairwise distinguishability, information sufficiency or evidence graph appear.

## Teach-back acceptance test

Answer, in accessible words:
- "以前怎么做？" (one or two sentences)
- "具体哪里出错？" (one small input-to-output example)
- "我们到底改变哪个决策？" (one sentence)
- "如果证明不了哪个现象，就不做？" (one test)
If any missing, explanation FAILS even when novelty audits are long and sophisticated.

## Prohibitions

Do not assert a new scientific concept is objectively unstudied because it has a new name. Distinguish failure caused by corrupted input (irrecoverable) from extra harm caused by adaptation updates. Do not conflate "confidence" with all test-time adaptation baselines; list exact methods actually using entropy/pseudolabels. Avoid asserting a modality lost class information based only on a lower image-quality metric.
