#!/usr/bin/env python3
"""Generate Tokens Studio typeface sets from a Figma font dump.

Reads a dump produced by the Font Dumper plugin (figma.listAvailableFontsAsync),
filters each family to its CORE styles (normal width, no Display/Condensed/etc.),
and writes one <slug>.json per family in the repo's canonical format:

    { "fontFamilies": { <slug>: {value, type, description} },
      "fontWeights":  { <slug>-<num>-<name>[-italic]: {value, type, description} } }

The weight VALUE string is preserved verbatim from Figma (spacing/casing intact) —
that string is the whole point of this project. Only the token KEY is normalized.

Usage:
    python3 generate_tokens.py DUMP.json SELECTED.json OUTDIR
      DUMP.json     full plugin output ({families: {name: [styles]}})
      SELECTED.json { "Noto Sans Arabic": "noto-sans-arabic", ... }  family -> file slug
      OUTDIR        directory to write <slug>.json into
"""
import json, re, sys, os

WIDTHS = ["ExtraCondensed", "SemiCondensed", "Condensed"]

# weight string (lowercased, despaced) -> (number, canonical key-slug)
WEIGHT_MAP = {
    "thin": (100, "thin"),
    "extralight": (200, "extralight"),
    "ultralight": (200, "extralight"),
    "light": (300, "light"),
    "demilight": (350, "demilight"),
    "regular": (400, "regular"),
    "medium": (500, "medium"),
    "semibold": (600, "semibold"),
    "bold": (700, "bold"),
    "extrabold": (800, "extrabold"),
    "ultrabold": (800, "extrabold"),
    "black": (900, "black"),
}


def is_core(style):
    """True if style is normal-width and not a Display optical variant."""
    s = style.strip()
    if s.startswith("Display"):
        return False
    return not any(s.startswith(w) for w in WIDTHS)


def parse_weight(style):
    """(number, slug, is_italic) from a CORE style string. Verbatim value handled by caller."""
    s = style.strip()
    italic = s.endswith("Italic")
    if italic:
        s = s[: -len("Italic")].strip()
    key = s.replace(" ", "").lower()
    if key == "":            # bare "Italic" == Regular Italic
        return 400, "regular", True
    if key not in WEIGHT_MAP:
        raise ValueError(f"unknown weight in style {style!r}")
    num, slug = WEIGHT_MAP[key]
    return num, slug, italic


def specimen_url(family):
    return "https://fonts.google.com/noto/specimen/" + family.replace(" ", "+")


def build_set(family, slug, styles):
    core = [s for s in styles if is_core(s)]
    weights = {}
    for st in core:
        num, wslug, italic = parse_weight(st)
        key = f"{slug}-{num}-{wslug}" + ("-italic" if italic else "")
        weights[key] = {
            "value": st,                       # VERBATIM from Figma
            "type": "fontWeights",
            "description": f"weight : {num}\nstyle : {'italic' if italic else 'normal'}",
        }
    # sort by (weight number, italic-after-upright)
    ordered = dict(sorted(weights.items(),
                          key=lambda kv: (int(kv[1]['description'].split()[2]),
                                          kv[0].endswith('-italic'))))
    return {
        "fontFamilies": {
            slug: {
                "value": family,
                "type": "fontFamilies",
                "description": f"Download this font - {specimen_url(family)}",
            }
        },
        "fontWeights": ordered,
    }


def main():
    dump_path, selected_path, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
    dump = json.load(open(dump_path))["families"]
    selected = json.load(open(selected_path))
    os.makedirs(outdir, exist_ok=True)
    for family, slug in selected.items():
        if family not in dump:
            print(f"!! {family!r} not in dump — skipped"); continue
        data = build_set(family, slug, dump[family])
        out = os.path.join(outdir, f"{slug}.json")
        with open(out, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"wrote {out}  ({len(data['fontWeights'])} weights)")


if __name__ == "__main__":
    main()
