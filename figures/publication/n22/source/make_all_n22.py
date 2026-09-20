from __future__ import annotations
import argparse
from pathlib import Path
from n22_common import plt
from n22_figures_1_2 import figure1, figure2
from n22_figures_3_4 import figure3, figure4
from n22_figures_5_7 import figure5, figure6, figure7

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--release-root',type=Path,required=True)
    ap.add_argument('--extra-data',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--font-family',default=None)
    args=ap.parse_args()
    if args.font_family:
        plt.rcParams['font.family']='sans-serif'
        plt.rcParams['font.sans-serif']=[args.font_family]
    figure1(args.release_root,args.out); figure2(args.release_root,args.out)
    figure3(args.release_root,args.out); figure4(args.release_root,args.extra_data,args.out)
    figure5(args.release_root,args.out); figure6(args.release_root,args.out); figure7(args.release_root,args.out)

if __name__=='__main__':
    main()
