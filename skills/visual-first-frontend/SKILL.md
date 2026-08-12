---
name: visual-first-frontend
description: Create imaginative frontend interfaces by generating a visual design first, translating it into maintainable code, and iterating with fixed-viewport browser screenshots and pixel differences. Use for landing pages, product pages, dashboards, portfolios, or UI redesigns when visual originality and close design-to-code fidelity matter.
---

# Visual-First Frontend

Build from an approved visual target, then close the gap through measured browser-rendered comparison. Optimize both visual fidelity and implementation quality.

## Establish the contract

Collect or infer the product purpose, audience, required content, framework, target route, brand constraints, and primary viewport. Ask only about choices that materially change the result. Default to the repository's existing stack and a 1440 x 1024 desktop reference plus a 390 x 844 mobile check.

Keep user-provided copy, logos, brand assets, and functional requirements authoritative. Do not invent product claims.

## Execute the workflow

1. Inspect the repository and running application before changing code. Preserve its component conventions and unrelated changes.
2. Create two or three genuinely different visual directions when the user has not supplied a reference. Use image generation for composition, atmosphere, imagery, texture, and art direction. Do not use generated text inside images for real UI copy.
3. Obtain the user's direction choice when the alternatives would produce materially different implementations. If the user already chose a direction or supplied a reference, proceed.
4. Produce a canonical reference at an explicit viewport. Extract the design contract: page regions, component tree, grid, spacing, type scale, palette, radii, borders, shadows, imagery, and responsive behavior.
5. Separate visual assets from UI. Generate or crop illustrations, textures, and decorative media as individual assets. Implement text, controls, cards, and layout as semantic HTML and CSS.
6. Implement the page with reusable components and tokens. Match large geometry before decorative details. Avoid encoding the entire reference as a background image.
7. Run the application and capture a browser screenshot at the exact reference viewport. Disable animations, caret blinking, random content, and unstable timestamps during capture. Wait for fonts and images.
8. Compare the reference and implementation using `scripts/visual_diff.py`. Inspect the overlay/difference image, then fix discrepancies in this order: canvas and major regions; alignment and spacing; typography and wrapping; color and surfaces; icons and decoration.
9. Repeat capture, comparison, and correction until two consecutive passes yield no meaningful improvement or the acceptance targets are met. Record each score so regressions are visible.
10. Verify mobile layout, intermediate widths, interaction states, keyboard navigation, overflow, and console errors. Never improve the reference screenshot by breaking responsiveness or semantics.

## Use the visual diff tool

Run with the bundled Codex Python runtime when available:

```bash
<python> scripts/visual_diff.py reference.png actual.png --output-dir visual-diff
```

The tool requires equal image dimensions and writes `overlay.png`, `difference.png`, and `metrics.json`. Read [references/acceptance.md](references/acceptance.md) before interpreting its metrics or declaring completion.

## Guardrails

- Treat the reference as an art-direction target, not permission to flatten the UI into an image.
- Prefer CSS layout, design tokens, SVG icons, and accessible controls.
- Use absolute positioning only for genuinely layered or decorative elements.
- Preserve intentional asymmetry; do not normalize a distinctive composition into a generic template.
- Do not claim pixel-perfect completion without a same-size screenshot comparison.
- Report remaining mismatches and their causes when fonts, browser rendering, missing source assets, or dynamic content prevent exact matching.

## Deliver

Return the implemented route, reference design path, key asset paths, tested viewports, latest comparison metrics, and any known gaps. Show the final screenshot when useful.
