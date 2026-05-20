-- Trends Open initial submission requires that figures NOT be embedded
-- in the main manuscript document; figure legends stay inline as
-- paragraphs and the figure files are uploaded separately in Editorial
-- Manager. This filter unwraps every Figure block into its caption
-- (Quarto's crossref filter has already prefixed each caption with
-- "Figure N:" by the time this filter runs) and removes any remaining
-- standalone inline images (icons, link decorations, etc.).

local fig_count = 0

function Figure(elem)
  fig_count = fig_count + 1
  local caption_blocks = (elem.caption and elem.caption.long) or {}
  if #caption_blocks == 0 then
    -- No caption — emit a minimal placeholder paragraph so the figure
    -- citation in the running text still has a referent.
    return pandoc.Para({
      pandoc.Strong({pandoc.Str("Figure " .. fig_count .. ".")}),
      pandoc.Space(),
      pandoc.Str("[caption missing]")
    })
  end

  -- If Quarto's crossref didn't add a "Figure N:" prefix, prepend one.
  -- Test by checking whether the first inline of the first caption
  -- block is a Str that starts with "Figure".
  local first = caption_blocks[1]
  local first_inlines = first.content or {}
  local has_prefix = false
  if #first_inlines > 0 and first_inlines[1].t == "Str" then
    has_prefix = string.match(first_inlines[1].text, "^Figure") ~= nil
  end

  if not has_prefix then
    local prefix = {
      pandoc.Strong({pandoc.Str("Figure " .. fig_count .. ".")}),
      pandoc.Space(),
    }
    local new_inlines = {}
    for _, p in ipairs(prefix) do table.insert(new_inlines, p) end
    for _, c in ipairs(first_inlines) do table.insert(new_inlines, c) end
    first.content = new_inlines
  end

  return caption_blocks
end

function Image(elem)
  -- Strip any remaining inline images (icons, external-link glyphs).
  return {}
end
