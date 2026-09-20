from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
M=ROOT/'manifests'
EXPECTED={f'FIG-0{i}' for i in range(1,8)}
VALID_ROLES={'hero','validation','control','robustness','mechanism','context'}

def main():
    found=set()
    for p in sorted(M.glob('FIG-*.json')):
        d=json.loads(p.read_text(encoding='utf-8')); fid=d['figure_id']; found.add(fid)
        assert d['publication_gate']=='BENCHMARK_PASS', (fid,d['publication_gate'])
        assert d['qa']['scientific']=='PASS' and d['qa']['visual']=='PASS'
        assert d['provenance']['class']=='SIMULATION_EXECUTED'
        assert d['provenance']['manuscript_evidence_eligible'] is True
        assert d['final_size']['width_mm']==177.8
        assert d['final_size']['min_text_pt']>=7.0
        assert d['final_size']['min_line_pt']>=0.55
        assert d['visual_qa']['render_opened'] is True
        assert d['visual_qa']['final_size_inspected'] is True
        for panel in d['panels']:
            assert panel['role'] in VALID_ROLES
            assert panel['evidence_ids']
            assert panel['source_paths']
            if panel.get('uncertainty_shown'):
                assert panel.get('uncertainty_definition')
        source=(p.parent/d['exports']['source']).resolve()
        assert source.exists(), (fid,source)
    assert found==EXPECTED,(found,EXPECTED)
    print('N22 MANIFEST CONTRACT: PASS')
if __name__=='__main__': main()
