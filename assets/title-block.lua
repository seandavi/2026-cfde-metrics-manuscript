-- Quarto's DOCX and PDF title pages print author names only; the
-- affiliations, corresponding-author emails and keywords reach the HTML
-- title block but not the files the editor sees (issue #75). This
-- filter builds that block from Quarto's normalized author metadata
-- (`by-author`, `affiliations`, both numbered by Quarto) and rewrites
-- `author` as a list of title-page lines:
--
--   1. names, each with superscript affiliation numbers and * for
--      corresponding authors;
--   2. one line per affiliation, prefixed by its number;
--   3. a * line with the corresponding authors' emails, in the Trends
--      form "email (initials surname)".
--
-- Pandoc's DOCX writer sets each `author` entry as an Author-styled
-- paragraph; for PDF, assets/title.tex lays the same lines out under
-- \maketitle. Keywords go in a paragraph at the start of the body, which
-- both formats place directly after the abstract.

local function superscript(text)
  return pandoc.Superscript({pandoc.Str(text)})
end

local function join_inlines(parts, sep)
  local result = pandoc.Inlines({})
  for i, part in ipairs(parts) do
    if i > 1 then
      result:extend(sep)
    end
    result:extend(part)
  end
  return result
end

local function is_corresponding(author)
  return author.attributes ~= nil
    and pandoc.utils.stringify(author.attributes.corresponding or "") == "true"
end

local function author_line(authors)
  local names = {}
  for _, author in ipairs(authors) do
    local marks = {}
    for _, affiliation in ipairs(author.affiliations or {}) do
      table.insert(marks, pandoc.utils.stringify(affiliation.number))
    end
    if is_corresponding(author) then
      table.insert(marks, "*")
    end
    local name = pandoc.Inlines(author.name.literal)
    if #marks > 0 then
      name:insert(superscript(table.concat(marks, ",")))
    end
    table.insert(names, name)
  end
  return join_inlines(names, {pandoc.Str(","), pandoc.Space()})
end

local function affiliation_line(affiliation)
  local parts = {}
  for _, key in ipairs({"name", "city"}) do
    if affiliation[key] then
      table.insert(parts, pandoc.Inlines(affiliation[key]))
    end
  end
  local region = {}
  for _, key in ipairs({"region", "postal-code"}) do
    if affiliation[key] then
      table.insert(region, pandoc.utils.stringify(affiliation[key]))
    end
  end
  if #region > 0 then
    table.insert(parts, pandoc.Inlines(table.concat(region, " ")))
  end
  if affiliation.country then
    table.insert(parts, pandoc.Inlines(affiliation.country))
  end
  local line = pandoc.Inlines({superscript(pandoc.utils.stringify(affiliation.number))})
  line:extend(join_inlines(parts, {pandoc.Str(","), pandoc.Space()}))
  return line
end

-- "Casey Greene" -> "C. Greene", "Ethan M. Lange" -> "E.M. Lange".
local function initials_and_family(name)
  local initials = ""
  for word in pandoc.utils.stringify(name.given or ""):gmatch("[^%s%.]+") do
    initials = initials .. pandoc.text.sub(word, 1, 1) .. "."
  end
  return initials .. " " .. pandoc.utils.stringify(name.family or "")
end

-- Trends format: *Correspondence: jqsmith@univ.edu (J.Q. Smith).
local function correspondence_line(authors)
  local contacts = {}
  for _, author in ipairs(authors) do
    if is_corresponding(author) and author.email then
      local email = pandoc.utils.stringify(author.email)
      local contact = pandoc.Inlines({
        pandoc.Link(email, "mailto:" .. email),
        pandoc.Space(),
        pandoc.Str("(" .. initials_and_family(author.name) .. ")"),
      })
      table.insert(contacts, contact)
    end
  end
  if #contacts == 0 then
    return nil
  end
  local line = pandoc.Inlines({superscript("*"), pandoc.Str("Correspondence:"), pandoc.Space()})
  line:extend(join_inlines(contacts, {pandoc.Str(";"), pandoc.Space()}))
  return line
end

local function keywords_para(keywords)
  local words = {}
  for _, keyword in ipairs(keywords) do
    table.insert(words, pandoc.utils.stringify(keyword))
  end
  return pandoc.Para({
    pandoc.Strong({pandoc.Str("Keywords:")}),
    pandoc.Space(),
    pandoc.Str(table.concat(words, "; ")),
  })
end

function Pandoc(doc)
  local meta = doc.meta
  local authors = meta["by-author"]
  if authors and #authors > 0 then
    local names = {}
    for _, author in ipairs(authors) do
      table.insert(names, pandoc.utils.stringify(author.name.literal))
    end
    -- PDF document properties keep the plain names.
    meta["author-meta"] = table.concat(names, "; ")

    local lines = pandoc.List({author_line(authors)})
    for _, affiliation in ipairs(meta.affiliations or {}) do
      lines:insert(affiliation_line(affiliation))
    end
    local correspondence = correspondence_line(authors)
    if correspondence then
      lines:insert(correspondence)
    end
    meta.author = lines:map(pandoc.MetaInlines)
  end

  if meta.keywords and #meta.keywords > 0 then
    doc.blocks:insert(1, keywords_para(meta.keywords))
  end

  doc.meta = meta
  return doc
end
