from __future__ import annotations
import argparse, hashlib
from pathlib import Path
import pymupdf as fitz
from PIL import Image

EXPECTED_MM={
 'Figure_1_credibility_registry_asymmetry_N22R':(177.8,80.0),
 'Figure_2_prepared_state_directional_depinning_N22R':(177.8,116.0),
 'Figure_3_same_spectrum_mechanism_N22R':(177.8,114.0),
 'Figure_4_compact_elastic_robustness_N22R':(177.8,116.0),
 'Figure_5_boundary_registry_switching_N22R':(177.8,116.0),
 'Figure_6_vector_mode_locking_N22R':(177.8,124.0),
 'Figure_7_thermal_hierarchy_N22R':(177.8,116.0),
}

def mm_to_pt(x): return x/25.4*72.0

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('figure_dir',type=Path); ap.add_argument('--require-arial',action='store_true'); args=ap.parse_args()
    out=args.figure_dir.resolve(); sums=[]
    for stem,(wmm,hmm) in EXPECTED_MM.items():
        for ext in ['pdf','svg','eps','png']:
            p=out/f'{stem}.{ext}'
            if not p.exists() or p.stat().st_size==0: raise AssertionError(f'missing/empty export: {p}')
            sums.append((hashlib.sha256(p.read_bytes()).hexdigest(),p.name))
        doc=fitz.open(out/f'{stem}.pdf'); page=doc[0]; rect=page.rect
        if abs(rect.width-mm_to_pt(wmm))>0.15 or abs(rect.height-mm_to_pt(hmm))>0.15:
            raise AssertionError(f'{stem}: wrong PDF canvas {rect.width:.3f}x{rect.height:.3f} pt')
        fonts={str(f[3]) for f in page.get_fonts(full=True)}
        if args.require_arial:
            if not any('Arial' in name for name in fonts): raise AssertionError(f'{stem}: literal Arial missing: {sorted(fonts)}')
            bad=('Arimo','Liberation','DejaVu','STIX','ComputerModern')
            if any(any(token in name for token in bad) for name in fonts):
                raise AssertionError(f'{stem}: non-Arial fallback font leaked: {sorted(fonts)}')
        doc.close()
        png=Image.open(out/f'{stem}.png'); expected=(round(wmm/25.4*300),round(hmm/25.4*300))
        if any(abs(a-b)>1 for a,b in zip(png.size,expected)): raise AssertionError(f'{stem}: wrong PNG canvas {png.size}, expected {expected} +/-1')
        print(stem,'PASS',sorted(fonts),png.size)
    (out/'N22R_FIGURE_SHA256SUMS.txt').write_text(''.join(f'{h}  {n}\n' for h,n in sorted(sums,key=lambda z:z[1])),encoding='utf-8')
    print('N22R FIGURE EXPORT PREFLIGHT: PASS')
if __name__=='__main__': main()
