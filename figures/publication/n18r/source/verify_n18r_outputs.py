from __future__ import annotations

import hashlib
from pathlib import Path
import sys

import pymupdf as fitz
from PIL import Image
from matplotlib import font_manager

EXPECTED_MM = {
    'Figure_1_symmetry_contracts_N18R': (177.8, 132.0),
    'Figure_2_branch_resolved_depinning_N18R': (177.8, 124.0),
    'Figure_3_extended_size_shape_similarity_N18R': (177.8, 120.0),
    'Figure_4_boundary_registry_switching_N18R': (177.8, 121.0),
    'Figure_5_vector_mode_map_floquet_N18R': (177.8, 124.0),
    'Figure_6_thermal_stationary_hierarchy_N18R': (177.8, 102.0),
}

def mm_to_pt(mm: float) -> float:
    return mm / 25.4 * 72.0

def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit('usage: verify_n18r_outputs.py FIGURE_DIR')
    out = Path(sys.argv[1]).resolve()
    arial = font_manager.findfont('Arial', fallback_to_default=False)
    print('ARIAL_PATH', arial)
    sums = []
    for stem, (wmm, hmm) in EXPECTED_MM.items():
        for ext in ['pdf', 'svg', 'eps', 'png']:
            p = out / f'{stem}.{ext}'
            if not p.exists() or p.stat().st_size == 0:
                raise AssertionError(f'missing/empty export: {p}')
            sums.append((hashlib.sha256(p.read_bytes()).hexdigest(), p.name))

        pdf = out / f'{stem}.pdf'
        doc = fitz.open(pdf)
        page = doc[0]
        rect = page.rect
        if abs(rect.width - mm_to_pt(wmm)) > 0.15 or abs(rect.height - mm_to_pt(hmm)) > 0.15:
            raise AssertionError(f'{stem}: wrong PDF canvas {rect.width:.3f}x{rect.height:.3f} pt')
        font_names = {str(f[3]) for f in page.get_fonts(full=True)}
        if not any('Arial' in name for name in font_names):
            raise AssertionError(f'{stem}: literal Arial not embedded: {sorted(font_names)}')
        if any(('Arimo' in name or 'Liberation' in name) for name in font_names):
            raise AssertionError(f'{stem}: fallback font leaked into PDF: {sorted(font_names)}')
        doc.close()

        png = Image.open(out / f'{stem}.png')
        expected_px = (round(wmm / 25.4 * 300), round(hmm / 25.4 * 300))
        # Matplotlib rasterization can differ by one pixel across backends because the
        # physical canvas is converted from floating-point inches to integer pixels.
        if any(abs(a-b) > 1 for a,b in zip(png.size, expected_px)):
            raise AssertionError(f'{stem}: wrong PNG canvas {png.size}, expected {expected_px} +/- 1 px')
        print(stem, 'PASS', sorted(font_names), png.size)

    manifest = out / 'N18R_FIGURE_SHA256SUMS.txt'
    manifest.write_text(''.join(f'{h}  {name}\n' for h, name in sorted(sums, key=lambda x: x[1])), encoding='utf-8')
    print('N18R VENUE RENDER PREFLIGHT: PASS')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
