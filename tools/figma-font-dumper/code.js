// Font Dumper — lists every {family, style} pair Figma knows, filtered to the
// families we care about, and hands them to the UI as JSON for easy copying.
//
// Why this exists: Figma serves its own pre-loaded copies of the Google Fonts,
// and the exact weight/style STRINGS it reports (e.g. "Extra Light" vs
// "ExtraLight", or "Italic" vs "Regular Italic") are the source of truth our
// design tokens must match. figma.listAvailableFontsAsync() is that source.
//
// Edit FAMILY_PREFIXES to change which families are dumped. Matching is
// case-insensitive and prefix-based on the family name exactly as Figma reports it.

const FAMILY_PREFIXES = ["Noto", "Inter"];

figma.showUI(__html__, { width: 520, height: 640 });

(async () => {
  const all = await figma.listAvailableFontsAsync();
  const wanted = all.filter((f) => {
    const fam = f.fontName.family.toLowerCase();
    return FAMILY_PREFIXES.some((p) => fam.startsWith(p.toLowerCase()));
  });

  // Group styles under each family, preserving Figma's own ordering.
  const byFamily = {};
  for (const f of wanted) {
    const fam = f.fontName.family;
    (byFamily[fam] = byFamily[fam] || []).push(f.fontName.style);
  }

  const payload = {
    generatedFrom: "figma.listAvailableFontsAsync()",
    familyCount: Object.keys(byFamily).length,
    families: byFamily,
  };

  figma.ui.postMessage(payload);
})();
