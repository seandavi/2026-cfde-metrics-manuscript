# Lifecycle-aware evaluation of biomedical data ecosystems

[![Website](https://img.shields.io/badge/preview-website-blue.svg)](https://seandavi.github.io/2026-cfde-metrics-manuscript/)
[![Render](https://github.com/seandavi/2026-cfde-metrics-manuscript/actions/workflows/render.yml/badge.svg)](https://github.com/seandavi/2026-cfde-metrics-manuscript/actions/workflows/render.yml)

Manuscript source for an [Opinion article](https://www.cell.com/trends-open/information-for-authors/article-types) prepared for submission to *[Trends Open](https://www.cell.com/trends-open)* (Cell Press).

**Live preview**: https://seandavi.github.io/2026-cfde-metrics-manuscript/ — navbar walks between the main manuscript and the three separate-file submission deliverables (Significance, Outstanding questions, Key references).

## Manuscript description

This paper proposes a structured approach to evaluating large-scale NIH biomedical data resources, organized around three complementary frameworks: *public value* (user engagement, citations, scientific impact), *scientific data quality* (metadata completeness, FAIR compliance, representativeness), and *operations and finance* (infrastructure reliability, software health, cost sustainability). We argue that the relative importance of each framework shifts predictably across a data resource's lifecycle, and that embedding this lifecycle logic into evaluation design is essential for informed decision-making.

The NIH [Common Fund Data Ecosystem](https://commonfund.nih.gov/dataecosystem) (CFDE) serves as both motivating case study and operational testbed. We describe the Integration and Coordination Center's first portfolio-wide dashboard for automated metric collection across publication, citation, GitHub, and web-analytics sources, and report on the practical challenges of onboarding projects, balancing transparency with privacy, and expanding metric coverage through a cross-center Metrics Working Group.

## How this repository is built

The manuscript is authored in [Quarto](https://quarto.org) as a multi-target **website** with four entry points: a main manuscript and three Editorial-Manager-ready separate-file deliverables. Citations are resolved from persistent identifiers (DOI / PubMed ID / ISBN / URL) by [**quartobot**](https://github.com/quartobot/quartobot) running as a Quarto pre-render hook.

Quartobot brings the [Manubot](https://manubot.org/) manuscript-as-software pattern — git-versioned source, automatic citation resolution, per-commit permalinks, CI builds — to Quarto. The repo here is a real-world test of quartobot's website-project support, with several findings filed upstream (see [quartobot/quartobot#103](https://github.com/quartobot/quartobot/issues/103)).

### Entry points

| File | Role | Output |
|---|---|---|
| `index.qmd` | Main manuscript: title page, abstract, body, glossary, references. Includes the chunks under `content/`. | website home + `index.{pdf,docx}` for Editorial Manager |
| `significance.qmd` | Trends-required 75-word Significance statement (separate-file submission deliverable). | `significance.{pdf,docx}` for Editorial Manager |
| `outstanding-questions.qmd` | "Outstanding questions" box (separate-file deliverable, ≤2,000 chars). | `outstanding-questions.{pdf,docx}` |
| `key-references.qmd` | "Key references" box: 5 anchor refs with annotations (separate-file deliverable). | `key-references.{pdf,docx}` |

The website navbar links between the four; on disk each renders to a navigable HTML page plus standalone Word and PDF documents for upload to Editorial Manager.

### Repository layout

- `index.qmd`, `significance.qmd`, `outstanding-questions.qmd`, `key-references.qmd` — top-level render targets
- `content/` — manuscript prose in markdown chunks; citations as `@doi:…`, `@pmid:…`, `@isbn:…`, `@url:…` directly in prose; cross-refs as `@fig-name` / `@tbl-name`
- `content/images/` — figures
- `content/boxes/` — the Significance / Outstanding Questions / Key References / Glossary content (included by the corresponding `*.qmd` wrappers, with Glossary inlined in the main manuscript)
- `references.bib` — hand-curated bibliography entries (currently empty)
- `references.json` — auto-resolved entries written by `quartobot resolve` (gitignored; regenerated on every render)
- `assets/trends-journals.csl` — citation style (Cell Press *Trends* journals; non-superscript bracketed numeric, e.g. `[1]`, `[1,5,7]`)
- `assets/custom-dictionary.txt` — spell-check additions
- `_quarto.yml` — project config; wires the `quartobot resolve` pre-render hook, the navbar, and per-format options
- `.github/workflows/render.yml` — CI render and deploy via the upstream Quartobot reusable workflow
- `cover_letter.md` — Trends Open submission cover letter

### Local build

Install [Quarto](https://quarto.org/docs/get-started/), the [quartobot CLI](https://github.com/quartobot/quartobot), and (for PDF) [TinyTeX](https://yihui.org/tinytex/):

```sh
brew install --cask quarto
uv tool install git+https://github.com/quartobot/quartobot
quarto install tinytex
```

Render everything:

```sh
quarto render
```

The pre-render hook resolves all `@doi:`, `@pmid:`, `@isbn:`, `@url:` cite keys into `references.json` before pandoc runs; pandoc-citeproc merges that with `references.bib` at render time. Outputs land in `_site/` — one HTML page, one PDF, and one DOCX per entry point.

### Continuous integration

Every push to `main` and every PR triggers `.github/workflows/render.yml`, which uses the [Quartobot reusable workflow](https://github.com/quartobot/quartobot/blob/main/.github/workflows/render-reusable.yml) to render and deploy. Outputs land on the `gh-pages` branch:

- **Latest from `main`**: https://seandavi.github.io/2026-cfde-metrics-manuscript/
- **Per-commit snapshots**: `/v/<sha>/` (immutable; tagged commits preserved indefinitely)
- **PR previews**: `/pr/<n>/` with a sticky comment linking back to the preview

The deployed website is HTML-only (per the [#103](https://github.com/quartobot/quartobot/issues/103) limitation in the upstream per-format render loop). Authors produce the submission PDF / DOCX files locally with `quarto render` for Editorial Manager upload.

## License

[![License: CC BY 4.0](https://img.shields.io/badge/License%20All-CC%20BY%204.0-lightgrey.svg)](http://creativecommons.org/licenses/by/4.0/)
[![License: CC0 1.0](https://img.shields.io/badge/License%20Parts-CC0%201.0-lightgrey.svg)](https://creativecommons.org/publicdomain/zero/1.0/)

Except when noted otherwise, the entirety of this repository is licensed under a CC BY 4.0 License ([`LICENSE.md`](LICENSE.md)). Code, data, and config files matched by these glob patterns are also released under CC0 1.0 ([`LICENSE-CC0.md`](LICENSE-CC0.md)): `*.sh`, `*.py`, `*.yml`/`*.yaml`, `*.json`, `*.bib`, `*.tsv`, `.gitignore`.

Please open [an issue](https://github.com/seandavi/2026-cfde-metrics-manuscript/issues) for licensing questions.
