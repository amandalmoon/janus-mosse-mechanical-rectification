import sys, numpy as np, pandas as pd
from scipy.optimize import brentq
sys.path.insert(0,'/mnt/data/janus_resolve/Janus_mechanical_rectification_v18_ProfessorCorrected_release/source')
import janus_fourier_landscapes_v12 as J
import new_physics_v18 as NP
land=J.dft_landscape('2H_MoSSe_Se-S-Se-S');A=np.column_stack([J.A1,J.A2]);xyA=A@np.array([0.,0.]);xyB=A@np.array([1/3,1/3])
def boundary_mask(pos):
 n=len(pos); out=[]
 for i in range(n):
  d=np.linalg.norm(pos-pos[i],axis=1); neigh=np.sum((d>1e-6)&(np.abs(d-1)<1e-6));out.append(neigh<6)
 return np.array(out)
def wf(theta,pos,w):
 R=J.rotation_matrix(theta);delta=pos@R.T-pos;ph=delta@land.vectors.T;return np.sum(w[:,None]*np.exp(1j*ph),axis=0)/w.sum()
def energy(theta,pos,w,xy):
 S=wf(theta,pos,w);return J.contact_ugh(xy[0],xy[1],S,land,0,0)[0]
rows=[]
for phi in [20,25]:
 pos,R=NP.make_fixedN_triangle(phi,127);edge=boundary_mask(pos)
 for ew in [0.5,0.75,1.0,1.25,1.5]:
  w=np.ones(len(pos));w[edge]=ew
  def dE(th):return energy(th,pos,w,xyA)-energy(th,pos,w,xyB)
  grid=np.linspace(2.4,3.3,181);rootv=np.nan
  for a,b in zip(grid[:-1],grid[1:]):
   if dE(a)==0 or dE(a)*dE(b)<0:
    rootv=a if dE(a)==0 else brentq(dE,a,b,xtol=1e-12);break
  rows.append(dict(phi=phi,edge_weight=ew,edge_sites=int(edge.sum()),ground_switch_deg=rootv))
  print(phi,ew,rootv)
pd.DataFrame(rows).to_csv('/mnt/data/janus_resolve/edge_weight_ground_switch.csv',index=False)
