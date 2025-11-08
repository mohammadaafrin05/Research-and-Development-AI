import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

SEED=123
print("Reproducibility Info:")
print("  Random seed used:", SEED)
print("  Bounds:theta in (0,50) deg,M in (-0.05,0.05),X in (0,100)")
df=pd.read_csv("xy_data.csv")
x_obs=df["x"].to_numpy().astype(float)
y_obs=df["y"].to_numpy().astype(float)
N=len(df)
theta_deg=28.11838783351749
theta=np.deg2rad(theta_deg)
M=0.02138876265111492
X=54.901774766592396
t=np.linspace(6.0,60.0,N)
def model_xy(t,theta,M,X):
    st=np.sin(0.3*t)
    cth=np.cos(theta)
    sth=np.sin(theta)
    e_term=np.exp(M*np.abs(t))*st
    x=t*cth-e_term*sth+X
    y=42+t*sth+e_term*cth
    return x,y
x_fit,y_fit=model_xy(t,theta,M,X)
mae_l1=np.mean(np.abs(x_fit-x_obs)+np.abs(y_fit-y_obs))
rmse=np.sqrt(np.mean((x_fit-x_obs)**2+(y_fit-y_obs)**2))
print(f"L1 error={mae_l1:.4f},RMSE={rmse:.4f}")
plt.figure(figsize=(7,5))
plt.scatter(x_obs,y_obs,s=14,label="Observed data")
plt.plot(x_fit, y_fit,linewidth=2,label="Fitted curve")
plt.xlabel("x")
plt.ylabel("y")
plt.title(f"Observed Data vs. Fitted Curve (theta={theta_deg:.2f} deg,M={M:.5f},X={X:.2f})")
plt.legend()
plt.tight_layout()
plt.savefig("fit_report.png",dpi=160)
plt.show()
