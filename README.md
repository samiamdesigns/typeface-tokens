# typeface-tokens
Design token files for popular font family and weight pairs for Tokens Studio in Figma.

Want to learn more? [Written guide](https://samiamdesigns.substack.com/p/it-took-me-2-years-to-figure-out)

## Adding a typeface

Add a typeface here only if its licence allows free use.
Client-licensed typefaces stay in the client's own folder, not in this repo.

1. Add `tokens/typeface/{font-name}.json`, following the pattern of an existing file such as `noto-sans.json`.
2. Copy the weight strings from Figma, not from the font files; `tools/figma-font-dumper` reads them.
3. Add the family to `tokens/$metadata.json`.
4. Add its Homebrew cask to the `Fonts` section of the `mac-setup` Brewfile, confirming the cask exists with `brew info --cask font-{name}` first.
