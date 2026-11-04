#!/usr/bin/env python3
"""Flag cited references with incomplete metadata.

Scans the render targets (`*.qmd`) and manuscript chunks (`content/**/*.md`)
for citation keys, looks each one up in the bibliography (`references.json`,
written by `quartobot resolve`, plus hand-curated `references.bib`), and
reports every cited entry missing an author, title, container/publisher,
issued year, or DOI. Web pages need a URL and accessed date instead of a DOI.
It also lists the keys whose `references.bib` entry overrides the resolved
one, so a shadowed resolver entry is never silent.

Run `quartobot resolve --from-scan . --output references.json
--id-mode citation-key` (or `quarto render`) first so references.json exists.

Usage: python3 ci/check_refs.py [PROJECT_DIR]

Exits 1 if any cited entry has a finding or any cited key is missing from the
bibliography, 0 otherwise.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

# Pandoc citation keys: start with a word character, allow internal
# punctuation. Trailing punctuation is not part of the key.
CITE_KEY_RE = re.compile(r"(?<![\w.@])@([\w][\w:.#$%&\-+?<>~/]*)")
TRAILING_PUNCTUATION = ":.#$%&-+?<>~/"
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
CROSSREF_PREFIXES = ("fig-", "tbl-", "sec-", "eq-", "lst-", "thm-")
WEB_TYPES = {"webpage", "post", "post-weblog", "software"}


def cited_keys(project: Path) -> dict[str, set[Path]]:
    """Map each citation key to the files that cite it."""
    sources = sorted(project.glob("*.qmd")) + sorted(project.glob("content/**/*.md"))
    keys: dict[str, set[Path]] = {}
    for path in sources:
        text = HTML_COMMENT_RE.sub("", path.read_text(encoding="utf-8"))
        for match in CITE_KEY_RE.finditer(text):
            key = match.group(1).rstrip(TRAILING_PUNCTUATION)
            if key.startswith(CROSSREF_PREFIXES):
                continue
            keys.setdefault(key, set()).add(path.relative_to(project))
    return keys


def load_bib_as_csl(bib_path: Path) -> list[dict]:
    """Convert hand-curated BibLaTeX to CSL JSON with pandoc."""
    if quarto := shutil.which("quarto"):
        cmd = [quarto, "pandoc"]
    elif pandoc := shutil.which("pandoc"):
        cmd = [pandoc]
    else:
        sys.exit("check_refs: need quarto or pandoc on PATH to read references.bib")
    result = subprocess.run(
        [*cmd, str(bib_path), "--from", "biblatex", "--to", "csljson"],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout or "[]")


def has_name(person: dict) -> bool:
    return bool(person.get("family") or person.get("literal"))


def findings(entry: dict) -> list[str]:
    """Return the missing-metadata findings for one CSL JSON entry."""
    problems: list[str] = []
    authors = entry.get("author") or []
    if not authors:
        problems.append("no author")
    elif not all(has_name(a) for a in authors):
        problems.append("author with no name (dropped consortium/institution?)")
    if not entry.get("title"):
        problems.append("no title")
    if not (entry.get("container-title") or entry.get("publisher")):
        problems.append("no container-title or publisher")
    date_parts = (entry.get("issued") or {}).get("date-parts") or [[]]
    if not date_parts[0]:
        problems.append("no issued year")
    if entry.get("type") in WEB_TYPES:
        if not entry.get("URL"):
            problems.append("no URL")
        if not entry.get("accessed"):
            problems.append("no accessed date")
    elif not entry.get("DOI"):
        problems.append("no DOI")
    return problems


def main() -> int:
    project = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    json_path = project / "references.json"
    if not json_path.exists():
        sys.exit(f"check_refs: {json_path} not found; run `quartobot resolve` first")
    bibliography = {e["id"]: e for e in json.loads(json_path.read_text(encoding="utf-8"))}
    bib_path = project / "references.bib"
    if bib_path.exists():
        # references.bib is listed after references.json in `bibliography:`,
        # so pandoc uses its entry when a key is in both.
        curated = {e["id"]: e for e in load_bib_as_csl(bib_path)}
        overridden = sorted(curated.keys() & bibliography.keys())
        if overridden:
            print(f"references.bib overrides {len(overridden)} resolved entries:")
            for key in overridden:
                print(f"  {key}")
            print()
        bibliography.update(curated)

    keys = cited_keys(project)
    flagged = 0
    for key in sorted(keys):
        where = ", ".join(str(p) for p in sorted(keys[key]))
        entry = bibliography.get(key)
        problems = ["not in references.json or references.bib"] if entry is None else findings(entry)
        if problems:
            flagged += 1
            print(f"{key}\n  cited in: {where}")
            for problem in problems:
                print(f"  - {problem}")
    print(f"\n{flagged} of {len(keys)} cited entries flagged.")
    return 1 if flagged else 0


if __name__ == "__main__":
    sys.exit(main())
