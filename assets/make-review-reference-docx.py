# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Build assets/trends-review-reference.docx from assets/trends-reference.docx.

The review-format DOCX (issue #51, used by the `review` Quarto profile)
needs three things pandoc can only take from the reference doc:

- continuous line numbers: <w:lnNumType> in the section properties;
- double spacing: line="480" on the document-default paragraph
  properties (Normal is already double-spaced in the base doc; this
  also covers styles not based on Normal);
- page numbers: a footer part holding a centered PAGE field.

Re-run after changing trends-reference.docx:

    uv run assets/make-review-reference-docx.py
"""

import re
import zipfile
from pathlib import Path

ASSETS = Path(__file__).resolve().parent
BASE_DOCX = ASSETS / "trends-reference.docx"
REVIEW_DOCX = ASSETS / "trends-review-reference.docx"

FOOTER_PART = "word/footer1.xml"
FOOTER_REL_ID = "rIdReviewFooter"

FOOTER_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r><w:r><w:fldChar w:fldCharType="separate"/></w:r><w:r><w:t>1</w:t></w:r><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p></w:ftr>
"""

# Child order follows CT_SectPr: footerReference, footnotePr, ..., lnNumType.
SECT_PR = f"""<w:sectPr>
      <w:footerReference w:type="default" r:id="{FOOTER_REL_ID}" />
      <w:footnotePr>
        <w:numRestart w:val="eachSect" />
      </w:footnotePr>
      <w:lnNumType w:countBy="1" w:distance="360" w:restart="continuous" />
    </w:sectPr>"""


def replace_once(text: str, pattern: str, replacement: str, part: str) -> str:
    """Substitute exactly one regex match, failing loudly if the base doc changed shape."""
    new_text, count = re.subn(pattern, replacement, text, flags=re.S)
    if count != 1:
        raise SystemExit(f"{part}: expected one match for {pattern!r}, found {count}")
    return new_text


def patch_part(name: str, xml: str) -> str:
    """Return the review version of one package part."""
    if name == "[Content_Types].xml":
        override = (
            f'<Override PartName="/{FOOTER_PART}" ContentType="application/'
            'vnd.openxmlformats-officedocument.wordprocessingml.footer+xml" />'
        )
        return replace_once(xml, r"</Types>", override + "</Types>", name)
    if name == "word/_rels/document.xml.rels":
        relationship = (
            '<Relationship Type="http://schemas.openxmlformats.org/officeDocument/'
            f'2006/relationships/footer" Id="{FOOTER_REL_ID}" Target="footer1.xml" />'
        )
        return replace_once(xml, r"</Relationships>", relationship + "</Relationships>", name)
    if name == "word/document.xml":
        return replace_once(xml, r"<w:sectPr>.*?</w:sectPr>", SECT_PR, name)
    if name == "word/styles.xml":
        return replace_once(
            xml,
            r'(<w:pPrDefault>\s*<w:pPr>\s*<w:spacing w:after="200") />',
            r'\1 w:line="480" w:lineRule="auto" />',
            name,
        )
    return xml


def main() -> None:
    with zipfile.ZipFile(BASE_DOCX) as base:
        if FOOTER_PART in base.namelist():
            raise SystemExit(f"{BASE_DOCX.name} already has {FOOTER_PART}")
        with zipfile.ZipFile(REVIEW_DOCX, "w", zipfile.ZIP_DEFLATED) as review:
            for info in base.infolist():
                data = base.read(info)
                if info.filename.endswith((".xml", ".rels")):
                    data = patch_part(info.filename, data.decode("utf-8")).encode("utf-8")
                review.writestr(info, data, zipfile.ZIP_DEFLATED)
            # Reuse a base timestamp so re-running yields identical bytes.
            footer_info = zipfile.ZipInfo(FOOTER_PART, date_time=base.infolist()[0].date_time)
            review.writestr(footer_info, FOOTER_XML, zipfile.ZIP_DEFLATED)
    print(f"wrote {REVIEW_DOCX.relative_to(ASSETS.parent)}")


if __name__ == "__main__":
    main()
