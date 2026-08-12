# Visual acceptance

Use metrics as diagnostic signals, not as the sole quality gate.

## Reference capture

- Capture reference and implementation at identical CSS viewport dimensions and device scale factor.
- Wait for `document.fonts.ready`, images, and network-driven layout to settle.
- Disable motion and caret rendering for deterministic screenshots.
- Keep browser, operating system, font files, and screenshot method consistent across iterations.

## Metrics

- `mean_absolute_error`: Average per-channel difference from 0 to 255. Lower is better.
- `changed_pixel_ratio`: Fraction of pixels whose largest channel difference exceeds the configured threshold.
- `similarity`: `1 - mean_absolute_error / 255`. Higher is better.

Large flat-background errors can dominate the score while small typography errors remain visually important. Always inspect the overlay and difference output.

## Default completion rule

Declare the visual loop complete only when:

1. Major region geometry and content match the approved design.
2. Similarity is at least 0.97, or remaining differences have an explained rendering or asset cause.
3. A final correction pass produces less than 0.002 similarity improvement.
4. The page remains usable at 390, 768, 1024, and 1440 CSS pixels where applicable.
5. No horizontal overflow, broken interaction, serious accessibility regression, or console error was introduced.

These are defaults. A product-specific target supplied by the user overrides them.

## Avoid metric gaming

Reject implementations that screenshot well only because they use a full-page background, hide real content, hard-code a single viewport, or replace semantic controls with raster images. Visual fidelity and implementation quality must both pass.
