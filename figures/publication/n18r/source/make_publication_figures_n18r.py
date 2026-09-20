from __future__ import annotations

import argparse
from pathlib import Path
import matplotlib.pyplot as plt

from n18r_figures_1_2 import figure1, figure2
from n18r_figures_3_4 import figure3, figure4
from n18r_figures_5_6 import figure5, figure6


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--release", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--font-family", default="Arial",
                    help="Figure text font; ACS Nano venue render must use literal Arial.")
    args = ap.parse_args()
    plt.rcParams.update({
        "font.family": args.font_family,
        "font.sans-serif": [args.font_family],
        "mathtext.fontset": "custom",
        "mathtext.rm": args.font_family,
        "mathtext.it": f"{args.font_family}:italic",
        "mathtext.bf": f"{args.font_family}:bold",
        "mathtext.sf": args.font_family,
        "mathtext.fallback": "stix",
    })
    root = args.release.resolve()
    out = args.out.resolve()
    for fn in [figure1, figure2, figure3, figure4, figure5, figure6]:
        fn(root, out)
    print(f"WROTE {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
