# Release notes

## v0.6.0 — 2026-10-08

### Added

- Build a semantic argument map for all paper figures, tables, algorithms, and teasers, including their roles, first-use stages, and later reuse.
- Track all essential visuals for the current stage before declaring it complete; explain cross-figure argument links and allow multiple necessary figures.
- Distinguish a true architecture diagram from a pipeline or algorithm listing, and state clearly when no architecture diagram is present.
- Add `check_figure_coverage.py` to audit a human-reviewed figure plan and stage records. It checks supplied records; it does not parse PDFs or verify that a client displayed an image.

### Updated

- Keep the stable plugin ID `paper-reading` while synchronizing the v0.6.0 reading workflow and helper scripts.
- Update project guides and installation links for the renamed `no-heartburn-academic-skills` repository.

## v0.5.3 — 2026-10-08

### Added

- Add conditional one-click next-stage navigation while preserving explicit reader consent and the seven-stage reading flow.
- Prefer verified, inline paper figures; distinguish an actual image display from sandbox download links and provide download links only as a fallback.
- Add the verified sandbox download-link helper to the PDF crop script.
- Add an in-repository screenshot example of a Transformer Self-Attention explanation. Its diagram is an explanatory schematic, not an original paper figure.

### Updated

- Make ChatGPT the primary use case while retaining Codex compatibility; clarify that account/model and client limits still apply.
- Keep the package identifier `paper-reading` and the `academic-skills` collection structure while updating to the supplied v0.5.3 workflow.
- Add tests for stage navigation, preview/download wording, and verified fallback links.

## v0.5.0 — 2026-10-08

### Added

- A seven-stage paper-reading guide with a clear boundary between the first three overview stages and the subsequent deep-reading stages.
- An optional seventh stage for evidence review, reviewer-style analysis, and research transfer.
- `crop_pdf_asset.py` for rendering a full PDF page or a user-selected crop.
- `make_figure_card.py` for adding a short reading guide around an unchanged, verified figure crop, with a pixel-preservation check.
- Plugin manifests, dependency declarations, automated checks, and usage documentation.

### Notes

- The plugin is named `paper-reading`; its client-facing display name is **论文带读**.
- The reading framework is preserved from the supplied v0.5.0 source. This release organizes the plugin under the `academic-skills` repository and aligns its package name, skill path, metadata, and documentation.
- The plugin provides instructions and two image utilities. PDF interpretation, web verification, image rendering in chat, and conversation continuity depend on the host AI client and its tools.
- No user papers, datasets, chat logs, credentials, or model weights are included.
