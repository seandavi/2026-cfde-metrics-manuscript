# Multidimensional Evaluation Frameworks for the NIH Common Fund Data Ecosystem

[![HTML Manuscript](https://img.shields.io/badge/manuscript-HTML-blue.svg)](https://seandavi.github.io/2026-cfde-metrics-manuscript/)
[![PDF Manuscript](https://img.shields.io/badge/manuscript-PDF-blue.svg)](https://seandavi.github.io/2026-cfde-metrics-manuscript/manuscript.pdf)
[![GitHub Actions Status](https://github.com/seandavi/2026-cfde-metrics-manuscript/workflows/Manubot/badge.svg)](https://github.com/seandavi/2026-cfde-metrics-manuscript/actions)

## Manuscript description

This paper proposes a structured approach to evaluating large-scale NIH biomedical data resources, organized around three complementary frameworks: *public value* (user engagement, citations, scientific impact), *scientific data quality* (metadata completeness, FAIR compliance, representativeness), and *operations and finance* (infrastructure reliability, software health, cost sustainability). We argue that the relative importance of each framework shifts predictably across a data resource's lifecycle — from early infrastructure-building, through active use, to long-term sustainability — and that embedding this lifecycle logic into evaluation design is essential for informed decision-making.

The NIH Common Fund Data Ecosystem (CFDE), a cross-cutting initiative that harmonizes metadata across 19 Common Fund programs through five specialized centers, serves as both the motivating case study and the testbed for these ideas. We describe the Integration and Coordination Center's (ICC) implementation of a centralized dashboard that automatically collects publication, citation, GitHub, and web analytics data across the portfolio, and report on the practical challenges of onboarding projects, balancing transparency with privacy, and iteratively expanding metric coverage through a cross-center Metrics Working Group.

The manuscript is built using [Manubot](https://manubot.org/), with source content in the [`content`](content) directory.

## Manubot

<!-- usage note: do not edit this section -->

Manubot is a system for writing scholarly manuscripts via GitHub.
Manubot automates citations and references, versions manuscripts using git, and enables collaborative writing via GitHub.
An [overview manuscript](https://greenelab.github.io/meta-review/ "Open collaborative writing with Manubot") presents the benefits of collaborative writing with Manubot and its unique features.
The [rootstock repository](https://git.io/fhQH1) is a general purpose template for creating new Manubot instances, as detailed in [`SETUP.md`](SETUP.md).
See [`USAGE.md`](USAGE.md) for documentation how to write a manuscript.

Please open [an issue](https://git.io/fhQHM) for questions related to Manubot usage, bug reports, or general inquiries.

### Repository directories & files

The directories are as follows:

+ [`content`](content) contains the manuscript source, which includes markdown files as well as inputs for citations and references.
  See [`USAGE.md`](USAGE.md) for more information.
+ [`output`](output) contains the outputs (generated files) from Manubot including the resulting manuscripts.
  You should not edit these files manually, because they will get overwritten.
+ [`webpage`](webpage) is a directory meant to be rendered as a static webpage for viewing the HTML manuscript.
+ [`build`](build) contains commands and tools for building the manuscript.
+ [`ci`](ci) contains files necessary for deployment via continuous integration.

### Local execution

The easiest way to run Manubot is to use [continuous integration](#continuous-integration) to rebuild the manuscript when the content changes.
If you want to build a Manubot manuscript locally, install the [conda](https://conda.io) environment as described in [`build`](build).
Then, you can build the manuscript on POSIX systems by running the following commands from this root directory.

```sh
# Activate the manubot conda environment (assumes conda version >= 4.4)
conda activate manubot

# Build the manuscript, saving outputs to the output directory
bash build/build.sh

# At this point, the HTML & PDF outputs will have been created. The remaining
# commands are for serving the webpage to view the HTML manuscript locally.
# This is required to view local images in the HTML output.

# Configure the webpage directory
manubot webpage

# You can now open the manuscript webpage/index.html in a web browser.
# Alternatively, open a local webserver at http://localhost:8000/ with the
# following commands.
cd webpage
python -m http.server
```

Sometimes it's helpful to monitor the content directory and automatically rebuild the manuscript when a change is detected.
The following command, while running, will trigger both the `build.sh` script and `manubot webpage` command upon content changes:

```sh
bash build/autobuild.sh
```

### Continuous Integration

Whenever a pull request is opened, CI (continuous integration) will test whether the changes break the build process to generate a formatted manuscript.
The build process aims to detect common errors, such as invalid citations.
If your pull request build fails, see the CI logs for the cause of failure and revise your pull request accordingly.

When a commit to the `main` branch occurs (for example, when a pull request is merged), CI builds the manuscript and writes the results to the [`gh-pages`](https://github.com/seandavi/2026-cfde-metrics-manuscript/tree/gh-pages) and [`output`](https://github.com/seandavi/2026-cfde-metrics-manuscript/tree/output) branches.
The `gh-pages` branch uses [GitHub Pages](https://pages.github.com/) to host the following URLs:

+ **HTML manuscript** at https://seandavi.github.io/2026-cfde-metrics-manuscript/
+ **PDF manuscript** at https://seandavi.github.io/2026-cfde-metrics-manuscript/manuscript.pdf

For continuous integration configuration details, see [`.github/workflows/manubot.yaml`](.github/workflows/manubot.yaml).

## License

<!--
usage note: edit this section to change the license of your manuscript or source code changes to this repository.
We encourage users to openly license their manuscripts, which is the default as specified below.
-->

[![License: CC BY 4.0](https://img.shields.io/badge/License%20All-CC%20BY%204.0-lightgrey.svg)](http://creativecommons.org/licenses/by/4.0/)
[![License: CC0 1.0](https://img.shields.io/badge/License%20Parts-CC0%201.0-lightgrey.svg)](https://creativecommons.org/publicdomain/zero/1.0/)

Except when noted otherwise, the entirety of this repository is licensed under a CC BY 4.0 License ([`LICENSE.md`](LICENSE.md)), which allows reuse with attribution.
Please attribute by linking to https://github.com/seandavi/2026-cfde-metrics-manuscript.

Since CC BY is not ideal for code and data, certain repository components are also released under the CC0 1.0 public domain dedication ([`LICENSE-CC0.md`](LICENSE-CC0.md)).
All files matched by the following glob patterns are dual licensed under CC BY 4.0 and CC0 1.0:

+ `*.sh`
+ `*.py`
+ `*.yml` / `*.yaml`
+ `*.json`
+ `*.bib`
+ `*.tsv`
+ `.gitignore`

All other files are only available under CC BY 4.0, including:

+ `*.md`
+ `*.html`
+ `*.pdf`
+ `*.docx`

Please open [an issue](https://github.com/seandavi/2026-cfde-metrics-manuscript/issues) for any question related to licensing.
