import sys,pandas as pd
sys.path.insert(0,'/mnt/data/janus_n8_gate/elastic')
import run_elastic_relaxation_validation as E

def case(label,theta,scale,c11=119.3,c12=27.5,tol=5e-5):
 m=E.ElasticContact(theta,E.ElasticParams(3.25,c11,c12,scale));gr,_=E.zero_ground(m);z0=gr[2];rp,_,zp=E.threshold(m,z0,+1,tol=tol);rm,_,zm=E.threshold(m,z0,-1,tol=tol);fp=rp['Fc_est'];fm=rm['Fc_est'];return dict(case=label,theta=theta,scale=scale,c11=c11,c12=c12,Fp=fp,Fm=fm,rho=(fp-fm)/(fp+fm),plus_strain=rp['principal_strain_max_abs'],minus_strain=rm['principal_strain_max_abs'],plus_disp=rp['disp_max_A'],minus_disp=rm['disp_max_A'])
rows=[]
for args in [('C_half_1p5',1.5,.5,119.3,27.5),('C_nom_1p5',1.5,1,119.3,27.5),('C_2x_1p5',1.5,2,119.3,27.5),('C_alt_1p5',1.5,1,126.8,27.4),('C_100x_1p5',1.5,100,119.3,27.5),('C_nom_3',3,1,119.3,27.5),('C_half_3',3,.5,119.3,27.5)]:
 print('RUN',args,flush=True);r=case(*args);rows.append(r);print(r,flush=True)
df=pd.DataFrame(rows);df.to_csv('/mnt/data/janus_n8_gate/n8_elastic_linear_tight.csv',index=False);print(df.to_string(index=False))
