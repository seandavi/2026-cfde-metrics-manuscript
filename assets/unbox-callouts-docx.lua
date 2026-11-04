-- Quarto writes DOCX callouts as raw OpenXML tables whose paragraphs
-- carry two <w:pPr> elements, which is invalid OOXML. Word and other
-- readers may silently drop the box, which is how the Glossary went
-- missing from the submitted manuscript (issue #48). For DOCX, unwrap
-- every callout into a plain level-2 heading (the callout title)
-- followed by its content, which pandoc's DOCX writer emits as
-- ordinary styled paragraphs. HTML and PDF keep the callout box.

function Callout(callout)
  local blocks = {}
  -- Quarto stores the title as a block, not inlines; titles here are
  -- plain text, so stringify it.
  local title = callout.title and pandoc.utils.stringify(callout.title) or ""
  if title ~= "" then
    table.insert(blocks, pandoc.Header(2, title, {class = "unnumbered"}))
  end
  -- A single-paragraph callout stores its content as one Block rather
  -- than a Blocks list; pandoc.Blocks normalizes both.
  for _, block in ipairs(pandoc.Blocks(callout.content)) do
    table.insert(blocks, block)
  end
  return blocks
end
