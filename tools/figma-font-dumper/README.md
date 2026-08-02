# Font Dumper

A tiny Figma development plugin that dumps the exact `{ family, style }` pairs
Figma knows about, for a chosen set of families.

## Why

Figma serves its own pre-loaded copies of the Google Fonts.
The exact weight/style **strings** it reports — `Extra Light` vs `ExtraLight`,
`Italic` vs `Regular Italic`, or width variants baked into the style like
`Condensed Thin Italic` — are the source of truth these design tokens must match.
Reading local font binaries is *not* reliable, because a machine's installed copy
can differ from Figma's.
`figma.listAvailableFontsAsync()` is the authoritative source, and this plugin
surfaces it in a copyable form.

## Use

1. Figma desktop → **Plugins → Development → Import plugin from manifest…**
2. Select `manifest.json` in this folder.
3. Run **Plugins → Development → Font Dumper**.
4. **Copy JSON** from the panel and hand it off (paste back to Claude, or save as
   `figma-fonts.json`).

## Configure

Edit `FAMILY_PREFIXES` in [code.js](code.js) to change which families are dumped.
Matching is case-insensitive and prefix-based on the family name exactly as Figma
reports it. Default: `["Noto", "Inter"]`.

## Output shape

```json
{
  "generatedFrom": "figma.listAvailableFontsAsync()",
  "familyCount": 3,
  "families": {
    "Noto Sans": ["Thin", "Thin Italic", "ExtraLight", "..."],
    "Inter": ["Thin", "Thin Italic", "Extra Light", "..."]
  }
}
```

## Files

- `manifest.json` — plugin manifest
- `code.js` — main thread: queries fonts, filters, posts to UI
- `ui.html` — panel with the JSON textarea + copy button
