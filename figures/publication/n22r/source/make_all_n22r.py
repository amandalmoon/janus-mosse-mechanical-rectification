from __future__ import annotations
import argparse, os, subprocess, sys
from pathlib import Path

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--release-root',type=Path,required=True)
    p.add_argument('--extra-data',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--font-family',default='Arial')
    a=p.parse_args()
    a.out.mkdir(parents=True,exist_ok=True)
    env=os.environ.copy()
    env['N22R_RELEASE_ROOT']=str(a.release_root.resolve())
    env['N22R_EXTRA_DATA']=str(a.extra_data.resolve())
    env['N22R_OUT']=str(a.out.resolve())
    env['N22R_FONT_FAMILY']=a.font_family
    here=Path(__file__).resolve().parent
    for stem in ['figure1_n22r.py','figure2_n22r.py','figure3_n22r.py','figure4_n22r.py','figure5_n22r.py']:
        subprocess.run([sys.executable,str(here/stem)],check=True,env=env)
    subprocess.run([sys.executable,str(here/'figure6_n22r.py'),'--release',str(a.release_root.resolve()),'--out',str(a.out.resolve())],check=True,env=env)
    subprocess.run([sys.executable,str(here/'figure7_n22r.py'),'--release',str(a.release_root.resolve()),'--out',str(a.out.resolve())],check=True,env=env)
if __name__=='__main__': main()
