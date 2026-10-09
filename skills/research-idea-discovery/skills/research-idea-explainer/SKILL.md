---
name: research-idea-explainer
description: Translate a rigorously investigated research idea into intuitive motivation, a concrete scenario, a two-case example, and a causal story a graduate student can retell. Use as part of Research Idea Discovery final delivery or for requests like 我没懂这个idea.
---

# Idea Explanation Layer — 导师先让学生听懂

Read `../research-idea-discovery/references/plain-language-idea-protocol.md` and `../research-idea-discovery/references/scientific-story-and-contributions.md`.

Output, in this order:
1. One-sentence daily-language question (≤50 Chinese characters when practical).
2. Concrete task sample: exactly what inputs, classes/labels, and output the old model uses. If no grounded case is available, mark it a hypothetical teaching example.
3. Two contrast situations holding one superficial property fixed (e.g. equally confident) but varying hypothesized task evidence. State what is observed versus hypothesized; do not invent measured results.
4. What a competent ordinary baseline does, why it may fail in the selected case, and the **most dangerous simple alternative** that might already solve it.
5. Core difference in one sentence, followed by technical terms/possible method—not before.
6. A 30-second spoken scientific story and a falsifying E0.

Forbidden: empty slogans ("confidence ≠ evidence") without operational definitions; naming a graph without an estimable edge definition; claiming baselines actually fail without evidence. If the user says 没懂, make a smaller toy example and walk through concrete inputs and prediction changes instead of repeating vocabulary.
