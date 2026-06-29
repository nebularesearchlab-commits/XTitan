#!/usr/bin/env python3
"""
CLI quick inspect for Cassini PDS3 products (BIDR .IMG, LBDR .TAB).

Examples:
  python scripts/peek_pds.py ../Inference_Data/BIEQI69S314_D220_T071S01_V03.IMG
  python scripts/peek_pds.py product.IMG --plot --sample 512
  python scripts/peek_pds.py LBDR_02_D294_V02.TAB --label-only
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Allow running from M5_Inference without installing as a package.
M5_ROOT = Path(__file__).resolve().parents[1]
if str(M5_ROOT) not in sys.path:
    sys.path.insert(0, str(M5_ROOT))

from src.pds_io import load_pds3_label, read_pds3_image, summarize_product  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Quick-read summary for PDS3 Cassini RADAR files.")
    parser.add_argument("path", type=Path, help="Path to .IMG, .TAB, or .LBL product")
    parser.add_argument("--label", type=Path, default=None, help="Detached .LBL if not alongside product")
    parser.add_argument("--label-only", action="store_true", help="Print raw label text only")
    parser.add_argument("--json", action="store_true", help="Emit summary as JSON")
    parser.add_argument("--plot", action="store_true", help="Show matplotlib preview (IMAGE products only)")
    parser.add_argument(
        "--sample",
        type=int,
        default=None,
        metavar="N",
        help="Load at most N lines/samples for preview (saves memory)",
    )
    args = parser.parse_args()

    if not args.path.is_file():
        print(f"ERROR: file not found: {args.path}", file=sys.stderr)
        return 1

    if args.label_only:
        _, text = load_pds3_label(args.path, label_path=args.label)
        print(text)
        return 0

    summary = summarize_product(args.path, label_path=args.label)
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(json.dumps(summary, indent=2))

    if args.plot and summary.get("product_kind") == "pds3_image":
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("ERROR: matplotlib required for --plot (pip install matplotlib)", file=sys.stderr)
            return 1

        crop = args.sample
        arr, _ = read_pds3_image(
            args.path,
            label_path=args.label,
            max_lines=crop,
            max_samples=crop,
        )
        plt.figure(figsize=(10, 6))
        plt.imshow(arr, aspect="auto", cmap="gray")
        plt.colorbar(label=summary.get("image", {}).get("note", "value"))
        plt.title(summary.get("product_id", args.path.name))
        plt.tight_layout()
        plt.show()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
