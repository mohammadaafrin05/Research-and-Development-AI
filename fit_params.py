import pandas as pd
import numpy as np
#Load the data 
df=pd.read_csv("xy_data.csv")
x_obs=df["x"].to_numpy().astype(float)
y_obs=df["y"].to_numpy().astype(float)
N=len(df)
#Let's think the uniform sampling of t in (6,60)
t=np.linspace(6.0,60.0,N)
def model_xy(t,theta,M,X):
    st=np.sin(0.3*t)
    cth=np.cos(theta)
    sth=np.sin(theta)
    e_term=np.exp(M*np.abs(t))*st
    x=t*cth-e_term*sth+X
    y=42+t*sth+e_term*cth
    return x,y
def l1_objective(theta,M,X):
    x_pred,y_pred=model_xy(t,theta,M,X)
    d=np.abs(x_pred-x_obs)+np.abs(y_pred-y_obs)
    return np.mean(d)
rng=np.random.default_rng(123)
theta_grid=np.deg2rad(np.linspace(0.5,49.5,120))
M_grid=np.linspace(-0.049,0.049,120)
X_grid=np.linspace(0.5,99.5,160)
best=(None,None,None,np.inf)
for th in theta_grid:
    Ms=rng.choice(M_grid,size=24,replace=False)
    Xs=rng.choice(X_grid,size=32,replace=False)
    for m in Ms:
        for x0 in Xs:
            val=l1_objective(th,m,x0)
            if val<best[3]:
                best=(th,m,x0,val)
theta0,M0,X0,_=best
def refine(theta,M,X,iters=800):
    curr=np.array([theta,M,X],dtype=float)
    curr_val=l1_objective(*curr)
    step=np.array([np.deg2rad(2.0),0.01,2.0])
    for i in range(iters):
        improved=False
        for j in range(3):
            for direction in (+1,-1):
                trial=curr.copy()
                trial[j]+=direction*step[j]
                trial[0]=np.clip(trial[0],np.deg2rad(0.001),np.deg2rad(49.999))
                trial[1]=np.clip(trial[1],-0.0499,0.0499)
                trial[2]=np.clip(trial[2],0.001,99.999)
                val=l1_objective(*trial)
                if val<curr_val:
                    curr,curr_val=trial,val
                    improved=True
        if not improved:
            step*=0.7
            jitter=np.array([np.deg2rad(0.2),0.002,0.2])*(rng.random(3)-0.5)*2
            trial=curr+jitter
            trial[0]=np.clip(trial[0],np.deg2rad(0.001),np.deg2rad(49.999))
            trial[1]=np.clip(trial[1],-0.0499,0.0499)
            trial[2]=np.clip(trial[2],0.001,99.999)
            val=l1_objective(*trial)
            if val<curr_val:
                curr,curr_val=trial,val
    return curr,curr_val
(params,score)=refine(theta0,M0,X0,iters=800)
theta,M,X=params
theta_deg=np.rad2deg(theta)
print(f"theta (deg): {theta_deg:.6f}")
print(f"M: {M:.12f}")
print(f"X: {X:.6f}")
print(f"Mean L1 (|dx|+|dy|): {score:.6f}")
latex=(r"( t*cos({th})-e^({M}|t|)*sin(0.3 t)*sin({th})+{X},42+t*sin({th})+e^({M}|t|)*sin(0.3 t)*cos({th}) )"
         .format(th=np.deg2rad(theta_deg),M=M,X=X))
print("\nLaTeX/Desmos form:")
print(latex)
print("\nReproducibility Info:")
print("  Random seed used: 123")
# Using ASCII-only for avoiding the Windows cp1252 issues
print("  Bounds: theta in (0,50) deg,M in (-0.05,0.05),X in (0,100)")
