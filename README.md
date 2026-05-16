# Multidimensional Evaluation Frameworks for the NIH Common Fund Data Ecosystem

[![HTML Manuscript](https://img.shields.io/badge/manuscript-HTML-blue.svg)](https://seandavi.github.io/2026-cfde-metrics-manuscript/)
[![PDF Manuscript](https://img.shields.io/badge/manuscript-PDF-blue.svg)](https://seandavi.github.io/2026-cfde-metrics-manuscript/index.pdf)
[![Render](https://github.com/seandavi/2026-cfde-metrics-manuscript/actions/workflows/render.yml/badge.svg)](https://github.com/seandavi/2026-cfde-metrics-manuscript/actions/workflows/render.yml)

## Manuscript description

This paper proposes a structured approach to evaluating large-scale NIH biomedical data resources, organized around three complementary frameworks: *public value* (user engagement, citations, scientific impact), *scientific data quality* (metadata completeness, FAIR compliance, representativeness), and *operations and finance* (infrastructure reliability, software health, cost sustainability). We argue that the relative importance of each framework shifts predictably across a data resource's lifecycle — from early infrastructure-building, through active use, to long-term sustainability — and that embedding this lifecycle logic into evaluation design is essential for informed decision-making.

The NIH Common Fund Data Ecosystem (CFDE), a cross-cutting initiative that harmonizes metadata across 19 Common Fund programs through five specialized centers, serves as both the motivating case study and the testbed for these ideas. We describe the Integration and Coordination Center's (ICC) implementation of a centralized dashboard that automatically collects publication, citation, GitHub, and web analytics data across the portfolio, and report on the practical challenges of onboarding projects, balancing transparency with privacy, and iteratively expanding metric coverage through a cross-center Metrics Working Group.

## How this repository is built

The manuscript is authored in [Quarto](https://quarto.org) and uses [quartobot](https://github.com/quartobot/quartobot) — the manubot manuscript-as-software pattern adapted for Quarto — to resolve citations from persistent identifiers at render time.

### Repository layout

- `index.qmd` — front matter (title, authors, abstract, keywords) and `{{< include >}}` of the content chunks
- `content/` — manuscript prose in markdown chunks; cite citations as `@doi:…`, `@pmid:…`, `@isbn:…`, `@url:…` directly in prose
- `content/images/` — figures
- `references.bib` — hand-curated bibliography entries (currently empty)
- `references.json` — auto-resolved entries written by `quartobot resolve` (gitignored; regenerated on every render)
- `assets/trends-journals.csl` — citation style (Cell Press Trends journals; non-superscript bracketed numeric, e.g. `[1]`, `[1,5,7]`)
- `_quarto.yml` — project config; wires the `quartobot resolve` pre-render hook
- `_version-banner.html[.template]` — per-commit version banner injected into the HTML output
- `.github/workflows/render.yml` — CI render and deploy via the upstream quartobot reusable workflow

### Local build

Install Quarto and the `quartobot` CLI:

```sh
brew install --cask quarto
uv tool install git+https://github.com/quartobot/quartobot
```

Render the manuscript:

```sh
quarto render
```

The pre-render hook resolves all `@doi:`, `@pmid:`, `@isbn:`, `@url:` cite keys into `references.json` before pandoc runs; pandoc-citeproc then merges that with `references.bib`. Outputs land at `index.html`, `index.pdf`, and `index.docx`.

### Continuous integration

Every push and PR triggers `.github/workflows/render.yml`, which renders HTML/PDF/DOCX, embeds the commit's permalink in the HTML banner, deploys to GitHub Pages at `https://seandavi.github.io/2026-cfde-metrics-manuscript/`, and posts a sticky preview comment on PRs. Per-commit snapshots live at `/v/<sha>/`; PR previews at `/pr/<n>/`.

## License

[![License: CC BY 4.0](https://img.shields.io/badge/License%20All-CC%20BY%204.0-lightgrey.svg)](http://creativecommons.org/licenses/by/4.0/)
[![License: CC0 1.0](https://img.shields.io/badge/License%20Parts-CC0%201.0-lightgrey.svg)](https://creativecommons.org/publicdomain/zero/1.0/)

Except when noted otherwise, the entirety of this repository is licensed under a CC BY 4.0 License ([`LICENSE.md`](LICENSE.md)). Code, data, and config files matched by these glob patterns are also released under CC0 1.0 ([`LICENSE-CC0.md`](LICENSE-CC0.md)): `*.sh`, `*.py`, `*.yml`/`*.yaml`, `*.json`, `*.bib`, `*.tsv`, `.gitignore`.

Please open [an issue](https://github.com/seandavi/2026-cfde-metrics-manuscript/issues) for licensing questions.
