from __future__ import annotations
import json, math, sys
from pathlib import Path
import numpy as np
ROOT=Path('/mnt/data/janus_audit'); sys.path.insert(0,str(ROOT))
import janus_fourier_landscapes_v12 as J
RNG=np.random.default_rng(20260919); TOL=1e-12

def rot(a):
    c,s=math.cos(a),math.sin(a); return np.array([[c,-s],[s,c]],float)
R60=rot(math.pi/3); Rm60=rot(-math.pi/3)

def star(shell):
    g1=Rm60@np.asarray(shell[0],float)
    return np.array([np.linalg.matrix_power(R60,j)@g1 for j in range(6)])
STARS=[star(sh) for sh in J.SHELLS]

def ref_batch(pts,W,phi,need_derivs=False):
    pts=np.asarray(pts,float); E0=6*W[0]
    om=np.zeros(len(pts),complex)
    if need_derivs:
        g=np.zeros((len(pts),2),float); H=np.zeros((len(pts),2,2),float)
    for wl,ph,st in zip(W,phi,STARS):
        for j0,G in enumerate(st):
            j=j0+1
            phase=pts@G + ((-1)**j)*ph
            term=wl*np.exp(1j*phase); om+=term
            if need_derivs:
                rt=np.real(1j*term); rh=np.real(-term)
                g += rt[:,None]*G[None,:]
                H += rh[:,None,None]*(G[:,None]*G[None,:])[None,:,:]
    u=np.real(om)/E0; im=np.abs(np.imag(om))/E0
    if need_derivs: return u,g/E0,H/E0,im
    return u,im

def ref_contact(Rc,theta,pos,W,phi):
    R=J.rotation_matrix(theta); pts=Rc[None,:] + pos@R.T-pos
    u,g,H,im=ref_batch(pts,W,phi,True)
    return float(u.mean()),g.mean(0),H.mean(0),float(im.max())

geom={}
for i,(sh,st) in enumerate(zip(J.SHELLS,STARS),1):
    geom[f'shell_{i}']={
        'C6_cycle_error':float(max(np.linalg.norm(st[(j+1)%6]-R60@st[j]) for j in range(6))),
        'stored_even_rep_error':float(max(np.linalg.norm(st[k]-sh[m]) for m,k in enumerate([1,3,5]))),
        'opposite_pair_error':float(max(np.linalg.norm(st[(j+3)%6]+st[j]) for j in range(3))),
    }

results={'tolerance':TOL,'geometry':geom,'configs':{}}
for key,d in J.DFT_TABLE.items():
    W=np.array(d['W'],float); phi=np.deg2rad(np.array(d['phi'],float)); land=J.dft_landscape(key)
    pts=RNG.uniform(-3,3,(20000,2))
    um=np.asarray(land.potential(pts[:,0],pts[:,1]))
    ur,im=ref_batch(pts,W,phi,False)
    max_u=float(np.max(np.abs(um-ur))); max_im=float(np.max(im))
    dpts=pts[:1000]; urd,gr,Hr,imd=ref_batch(dpts,W,phi,True)
    max_g=max_h=0.0
    for idx,r in enumerate(dpts):
        U,g,H=J.contact_ugh(float(r[0]),float(r[1]),np.ones(land.n_terms,complex),land)
        max_u=max(max_u,abs(U-urd[idx])); max_g=max(max_g,float(np.max(np.abs(g-gr[idx])))); max_h=max(max_h,float(np.max(np.abs(H-Hr[idx]))))
    results['configs'][key]={
        'n_potential_points':20000,'n_derivative_points':1000,
        'max_abs_potential_residual':max_u,'max_abs_gradient_residual':max_g,'max_abs_hessian_residual':max_h,
        'max_normalized_imag_reference':max(max_im,float(imd.max())),'energy_unit_meV':land.energy_unit_meV,
        'pass':bool(max(max_u,max_g,max_h)<TOL)
    }

key='2H_MoSSe_Se-S-Se-S'; d=J.DFT_TABLE[key]
W=np.array(d['W'],float); phi=np.deg2rad(np.array(d['phi'],float)); land=J.dft_landscape(key); pos=J.make_hexagonal_flake(6)
contact={'N':int(len(pos)),'n_tests':50,'max_abs_potential_residual':0.,'max_abs_gradient_residual':0.,'max_abs_hessian_residual':0.,'max_normalized_imag_reference':0.}
for _ in range(50):
    th=float(RNG.uniform(0,5)); Rc=RNG.uniform(-2,2,2)
    S=J.contact_factors(th,land.vectors,pos); U,g,H=J.contact_ugh(float(Rc[0]),float(Rc[1]),S,land)
    Ur,gr,Hr,im=ref_contact(Rc,th,pos,W,phi)
    contact['max_abs_potential_residual']=max(contact['max_abs_potential_residual'],abs(U-Ur))
    contact['max_abs_gradient_residual']=max(contact['max_abs_gradient_residual'],float(np.max(np.abs(g-gr))))
    contact['max_abs_hessian_residual']=max(contact['max_abs_hessian_residual'],float(np.max(np.abs(H-Hr))))
    contact['max_normalized_imag_reference']=max(contact['max_normalized_imag_reference'],im)
contact['pass']=bool(max(contact['max_abs_potential_residual'],contact['max_abs_gradient_residual'],contact['max_abs_hessian_residual'])<TOL)
results['finite_contact_primary_2H']=contact
results['normalization_contract']={'primary_W1_meV':float(W[0]),'expected_E0_6W1_meV':float(6*W[0]),'module_energy_unit_meV':float(land.energy_unit_meV),'hex_shell_6_site_count':int(len(pos)),'expected_N':127,'pass':bool(abs(land.energy_unit_meV-6*W[0])<TOL and len(pos)==127)}
allres=[]
for v in results['configs'].values(): allres += [v['max_abs_potential_residual'],v['max_abs_gradient_residual'],v['max_abs_hessian_residual']]
allres += [contact['max_abs_potential_residual'],contact['max_abs_gradient_residual'],contact['max_abs_hessian_residual']]
geommax=max(max(v.values()) for v in geom.values())
globalmax=max(allres); ok=globalmax<TOL and geommax<TOL and results['normalization_contract']['pass']
results['summary']={'global_max_differential_residual':float(globalmax),'global_max_geometry_residual':float(geommax),'all_under_1e-12':bool(ok),'material_input_gate':'PASS' if ok else 'FAIL'}
out=ROOT/'angeli_differential_audit.json'; out.write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps(results,indent=2))
