# Research Idea Discovery

[简体中文](README.md) | **English** | [Collection overview](../../README.en.md)

**Evidence-Driven Research Idea Discovery, Feasibility Validation & Scientific Review**

A personal research-idea discovery and validation plugin for ChatGPT Web, driven by the primary Research Idea Discovery Skill and supporting Skills. It does not treat idea generation as the finish line: it helps researchers find problems in prior evidence, challenge explanations, and decide what merits their time and resources.

> **This personal plugin is installed and used in ChatGPT Web; it does not consume Codex-specific task quota.** A step-by-step guide below shows how to create it with Plugin Creator and select it in a new conversation.

> **Start asking research questions while reading papers—not after reading dozens of them.** Move from reported experiments to falsifiable questions, then ask whether a problem matters, remains open, and is worth testing.

It supports computer vision, multimodal learning, robotics, machine learning, and other user-selected fields. Scope can be adapted to a target venue or research goal. The objective is not to force an idea: when evidence is insufficient, the workflow may recommend narrowing the question, researching further, or stopping.

This plugin is used in **ChatGPT Web** and does not consume Codex-specific task quota. ChatGPT model, message, and tool use remains subject to the user's account and plan. Optional Python scripts run only in a local Python environment; do not assume ChatGPT Web executes them directly.

## v3.5: Discover worthwhile problems while reading

Research Idea Discovery treats papers as **evidence, baselines, and intellectual lineage**, not just background to summarize after a literature search. For each key paper, it encourages questions such as: What does the result actually establish? What remains unproven? What is the strongest alternative explanation? Which low-cost experiment could tell these explanations apart?

### Four evidence-grounded entry points

| Entry point | Start from | What to test |
| --- | --- | --- |
| **Failure-driven** | A failure, degradation, or boundary case actually reported in a paper | After checking samples, metrics, splits, and budget, can the failure be reproduced? |
| **Reverse-engineer success** | A method with a strong reported result | Does the gain come from the claimed mechanism, or from capacity, budget, pretraining, or ordinary regularization? |
| **Triage apparent contradictions** | Findings that seem to disagree across papers | Are task, data, backbone, split, metric, and compute comparable? If not, propose a fair comparison before calling it a scientific contradiction. |
| **Translate deployment pain** | A real difficulty in hospitals, robotics, or industry | Can it become an important, measurable, testable scientific problem rather than an anecdote? |

Each lead should form a traceable chain:

**Paper → located experiment → known vs. unproven → problem/hypothesis → strongest null explanation → minimum no-new-method probe**

This puts scientific questioning inside the reading process instead of waiting until many papers have been collected and then inventing an idea from memory. Paper claims, reasonable inferences, and hypotheses to test remain distinct. A contribution statement or public code URL alone does not establish reproducibility.

### Establish the problem before choosing a method

The default is **problem-driven**: establish that a problem is real, important, and unresolved before selecting a method. **Method-driven** inspiration remains possible, but transferring a popular technique only generates a hypothesis. It must return to the independent M0 problem gate and show why it is more necessary than a simple alternative.

For suitable paper-anchored fast-start tasks, v3.5 can suggest a small set of key papers with different roles and build an evidence map and motivation candidates while reading. When literature is sparse, an open-problem discovery route remains available; the workflow does not force a paper quota. After motivation screening, it proceeds to near-neighbor research, data/code asset checks, mechanism necessity, and a minimum decisive experiment. If the motivation gate fails, it can recommend more evidence, a narrower problem, a pivot, or stopping instead of fabricating a method.

### Scientific depth and research velocity are separate

The plugin treats research value and startup speed as distinct questions:

- **Scientific Depth:** What understanding could change? Is the question important, the mechanism unresolved, and the prediction falsifiable?
- **Research Velocity:** Are data, code, weights, and licenses accessible? What time and compute are needed for the first diagnostic experiment?

A high-impact direction blocked by resources and a fast experiment with limited contribution should be reported differently. v3.5 can help set conditional short-term GO/STOP checkpoints; it does not promise a paper in two weeks or predict acceptance at any venue.

### v3.5 workflow

**Anchor papers and opportunity landscape → motivation candidates → M0 problem gate → near-neighbor and reproducibility checks → necessary mechanism and method design → minimum decisive experiment → GO / REFINE / PIVOT / STOP / RESEARCH MORE**

This is an iterative evidence-review process, not a pipeline that guarantees an idea. Structural checkers can validate whether records are complete; they cannot verify that a paper claim is true, a method is novel, or an experiment succeeded.

## Why not just an idea generator?

Typical idea generation can stop at module combinations, renamed concepts, or designing a model first and searching for motivation afterward. Research Idea Discovery connects proposal generation with adversarial review: it looks for dangerous near-neighbor papers, checks whether data and baselines are available, repeatedly challenges motivation and mechanism necessity, and prioritizes experiments that could falsify the hypothesis. It allows **REFINE, PIVOT, STOP, or RESEARCH MORE** rather than approving every idea.

## Core capabilities

### Discover research opportunities

Start from failure cases, method boundaries, hidden assumptions, and tensions in the literature to form falsifiable hypotheses. Focus on substantive contributions to the question and mechanism; adding a Router, Adapter, or Attention block is not novelty by itself.

### Validate data and experimental feasibility

Researchers do not need to arrive with a verified dataset. The workflow searches for public or derivable datasets, open baselines, pretrained weights, labels, and evaluation protocols, then checks for a low-cost validation path. When local tools are available, scripts can inspect a bounded sample, fields, and hashes. Discovering metadata or filling in a card does not prove access, licensing, or completed experiments.

### Audit near neighbors and mechanism-level novelty

Compare more than titles and keywords: inspect the problem, assumptions, computational mechanism, training objective, evaluation protocol, and method boundaries. Look for renamed contributions, module stacking, and simple variants of existing mechanisms. Search records improve traceability; they do not prove exhaustive coverage or scientific novelty.

### Re-examine motivation and scientific logic

The workflow checks whether the problem matters, studies dangerous near neighbors and mechanism necessity, revisits the motivation in light of that comparison, and only then develops the scientific argument:

**M1 Motivation Review → N Novelty Audit → L Mechanism Logic and Necessity → M2 Motivation Recheck → S Scientific Argument**

Key questions include: Why should the mechanism solve the problem? Would a simple baseline suffice? Has a nearby paper already solved it? Can the experiments distinguish the proposed mechanism from alternatives?

### Design a minimum decisive experiment and accept falsification

Prioritize small experiments that can quickly support or refute the hypothesis. Consider simple competitors, mechanism ablations, strong baselines, negative results, and computational cost. If a simple baseline matches or outperforms the proposal, the workflow requires re-examining the mechanism, motivation, and claims. Experiments that have not been run must be labeled as plans, not results.

### Deep-research handoff and research memory

When evidence remains insufficient, the Skill can prepare a targeted ChatGPT Deep Research prompt based on the current gaps. The user starts the research and returns the report to the original workflow. Candidate ideas, near neighbors, rejection reasons, and experiment feedback can be stored in a local work directory; this is not automatic ChatGPT cloud memory or a background task.

### Mentor-style research decision report

After evidence review, the plugin can organize its findings into a decision-oriented report covering a plain-language explanation, motivation, related-work position, falsifiable hypothesis, evidence-supported potential contributions, scientific story, reviewer risks, feasibility, and the next decisive experiment. Claims are labeled `VERIFIED`, `CONDITIONAL`, `UNKNOWN`, or `HYPOTHESIS`, with Idea, Evidence, Contribution, and Paper Claim kept distinct. The report format does not turn unverified points into established results.

## Research workflow

**Opportunity discovery:** literature investigation → failure analysis → idea seeds

**Value screening:** data search and anchoring → feasibility → motivation review → novelty → mechanism logic → motivation recheck

**Scientific validation:** hypothesis → scientific argument → reviewer-style critique → minimum decisive experiment

**Decision:** **GO / REFINE / PIVOT / STOP / RESEARCH MORE**

This process can backtrack and iterate; it is not a one-shot answer pipeline. The full phase order, roles, and evidence gates are in the primary [`SKILL.md`](skills/research-idea-discovery/SKILL.md) and its `references/` files.

## Create and install this plugin in ChatGPT Web

This repository contains open-source Skill/plugin files. It does not mean the plugin is already installed in a ChatGPT account or listed in the public directory. You can create a personal plugin using **Plugin Creator** in ChatGPT Web; availability depends on the account, workspace, and current product features.

1. Start a new ChatGPT Web conversation and select or mention **Plugin Creator**.
2. Send the prompt below. It is a template for this repository; whether the creator can read GitHub or install directly depends on account and tool permissions.

   ```text
   Please create and install a personal ChatGPT plugin named Research Idea Discovery based on this GitHub repository:

   https://github.com/zms618/no-heartburn-academic-skills

   Use skills/research-idea-discovery/skills/research-idea-discovery/SKILL.md as the primary specification, and preserve the references, examples, and auxiliary Skills in that project directory. Follow evidence-driven idea discovery, data and experiment feasibility checks, mechanism-level near-neighbor review, motivation and logic rechecks, minimum decisive experiments, and explicit recommendations to stop or change direction.

   Do not present search leads or planned experiments as verified evidence. Do not claim that ChatGPT Web automatically runs the repository's Python scripts. ChatGPT Web use does not require a Codex task or a separately configured API key for this Skill. Complete installation to my personal plugin list through the available interface.
   ```

3. Review the plugin instructions and reference paths. If the creator cannot read GitHub, upload `skills/research-idea-discovery/SKILL.md` and the required references from this project directory.
4. In a new ChatGPT conversation, select the personal plugin and specify your field, goal, and desired research stage.

A personal plugin is not thereby added to ChatGPT's public directory. Model, web search, file, and tool availability still depend on the ChatGPT account, selected model, and permissions. See [OpenAI's plugin guide](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt).

## Example prompts

**Discover candidate questions from a research area**

> My area is multimodal domain generalization, and I am targeting a top computer vision venue. Start from specific failure cases in relevant work and identify candidate scientific questions. Investigate available data and baselines, then rigorously review motivation, novelty, mechanism necessity, and validation cost. Separate verified evidence from hypotheses that still need testing.

**Review an existing idea**

> Evaluate this idea as a strict reviewer. Find the most dangerous near-neighbor work first. Then assess whether the problem is real, the mechanism necessary, a simpler alternative sufficient, and which experiments are most likely to falsify my claims. If evidence is insufficient, recommend REFINE, PIVOT, STOP, or further research.

**Prepare a deep-research handoff**

> We do not yet have a strong candidate. Summarize the search scope, rejected ideas, and key evidence gaps, then create a targeted prompt I can copy into ChatGPT Deep Research. Do not claim to have started Deep Research automatically.

## Optional local tools

The `scripts/` directory provides tools for literature metadata search, dataset discovery and sample checks, feasibility-card validation, workflow state gates, review and experiment records, idea ledgers, and Deep Research report handoff. They support local work and traceability; they do not replace full-paper verification or scientific judgment. Some local data sources may optionally use an API key; network access, dataset licenses, credentials, and experiment execution each require the appropriate permissions.

Note: `scripts/pilot_bridge.py` runs a user-specified local command only when `--execute` is explicitly provided; its default is `DRY_RUN`. Inspect the command and working directory first. ChatGPT Web does not run this script on the user's behalf.

Run the test suite from this project directory:

```bash
python -m unittest discover -s tests -v
```

Use each script's `--help` to see its options. Never describe a dry run, empty log, or planned experiment as completed work.

## Design principles and limitations

1. **Feasibility matters:** An idea without a credible validation path is not a mature research plan.
2. **Novelty is more than adding modules:** Terminology changes and module combinations do not automatically create substantive contributions.
3. **Establish motivation before storytelling:** The argument must follow from the problem, mechanism, and evidence.
4. **Evidence over confidence:** Label what is verified, inferred, and unknown.
5. **Try to falsify first:** Prioritize experiments that could disprove the central hypothesis.
6. **Zero strong ideas is acceptable:** State uncertainty and identify the next evidence needed.

The Skill does not guarantee a novel direction, exhaustive literature coverage, or acceptance at any venue. Research breadth depends on available sources and tools. Real data access and GPU experiments require authorization and an execution environment. Reviewer roles are workflow perspectives, not separately deployed models. Deep Research handoff currently means generating a prompt and manually returning the report; it does not launch a cloud research task automatically.

**The goal is not to convince you that an idea is good, but to help determine whether it remains worth your research time and resources after repeated scrutiny.**

## 🙏 Acknowledgements & Inspirations

Research Idea Discovery was shaped by ideas from open-source projects in AI-assisted scientific research. We thank their authors and contributors for sharing their work with the community:

- [ResearchStudio-Idea](https://github.com/microsoft/ResearchStudio) — Evidence-grounded ideation, literature-driven problem discovery, and idea evaluation.
- [CCFA-Skills](https://github.com/mikubaka88/CCFA-Skills) — Scientific storytelling, idea refinement, reviewer-oriented evaluation, and consistency between claims and evidence.
- [ARIS (Auto-Research-In-Sleep)](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) — Iterative research workflows, adversarial review, experimental feedback, and idea refinement.
- [RW Research Skill](https://github.com/ozrwayne/rw-research-skill) — Structured research processes, literature investigation, and evidence-based reasoning.
- [TaShan Research Skills](https://github.com/TashanGKD/tashan-research-skills) — Modular research Skills, evidence management, and workflow organization.
- [AI Night-Scientist](https://github.com/microsoft/ai_night_scientist) — Iterative scientific hypothesis exploration and AI-assisted research discovery.
- [PatSnap Skills](https://github.com/patsnap/skills) — Ideas for identifying potentially valuable technical innovations from existing research and development materials.

Building on these inspirations, this project independently organizes an evidence-review workflow for research ideas: **Idea Discovery → Feasibility Validation → Motivation Review → Novelty Audit → Mechanism and Logic Checks → Scientific Argument → Experimental Feedback**. These acknowledgements indicate conceptual or workflow inspiration; they do not imply official collaboration, endorsement, or full integration of upstream projects. Acknowledgement is separate from license compliance: any code, documentation, or templates actually copied, adapted, or redistributed remain subject to their applicable licenses.

## Version and license

Current release: **v3.5.0**. The [`CHANGELOG.md`](CHANGELOG.md) records release changes without turning this page into a version-by-version feature log. Licensed under MIT; see [`../../LICENSE`](../../LICENSE).
