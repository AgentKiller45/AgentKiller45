#!/usr/bin/env python3
"""Create deterministic visual comparison artifacts for two equal-size images."""

import argparse
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageEnhance, ImageStat


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("reference", type=Path)
    parser.add_argument("actual", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path("visual-diff"))
    parser.add_argument("--threshold", type=int, default=16)
    return parser.parse_args()


def main():
    args = parse_args()
    reference = Image.open(args.reference).convert("RGBA")
    actual = Image.open(args.actual).convert("RGBA")
    if reference.size != actual.size:
        raise SystemExit(
            f"Image sizes differ: reference={reference.size}, actual={actual.size}. "
            "Capture both at the same viewport and device scale factor."
        )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    Image.blend(reference, actual, 0.5).save(args.output_dir / "overlay.png")

    difference = ImageChops.difference(reference, actual)
    emphasized = ImageEnhance.Contrast(difference.convert("RGB")).enhance(4.0)
    emphasized.save(args.output_dir / "difference.png")

    rgb_diff = difference.convert("RGB")
    stats = ImageStat.Stat(rgb_diff)
    mean_absolute_error = sum(stats.mean) / 3.0
    pixel_data = (
        rgb_diff.get_flattened_data()
        if hasattr(rgb_diff, "get_flattened_data")
        else rgb_diff.getdata()
    )
    maxima = [max(pixel) for pixel in pixel_data]
    changed = sum(value > args.threshold for value in maxima)
    total = reference.width * reference.height
    metrics = {
        "width": reference.width,
        "height": reference.height,
        "threshold": args.threshold,
        "mean_absolute_error": round(mean_absolute_error, 6),
        "changed_pixel_ratio": round(changed / total, 6),
        "similarity": round(1.0 - mean_absolute_error / 255.0, 6),
    }
    (args.output_dir / "metrics.json").write_text(
        json.dumps(metrics, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
