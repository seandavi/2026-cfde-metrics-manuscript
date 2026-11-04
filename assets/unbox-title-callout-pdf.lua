-- The separate box deliverables (significance.qmd and friends) are
-- titled after their single box, so in PDF the box title repeated the
-- document title directly beneath it (issue #57; the DOCX fix is in
-- unbox-callouts-docx.lua, issue #75). For PDF, a callout whose title
-- matches the document title is unwrapped into its plain content. Other
-- callouts, such as the Glossary in the main manuscript, keep their box.

local doc_title = ""

local function read_title(meta)
  doc_title = meta.title and pandoc.utils.stringify(meta.title):lower() or ""
end

local function unbox_if_title_repeats(callout)
  local title = callout.title and pandoc.utils.stringify(callout.title) or ""
  if title == "" or title:lower() ~= doc_title then
    return nil
  end
  return pandoc.Blocks(callout.content)
end

-- Meta is visited after blocks, so read the title in a first pass.
return {
  {Meta = read_title},
  {Callout = unbox_if_title_repeats},
}
