import glob
import xarray as xr
import numpy as np
from datetime import datetime

a = xr.open_dataset("surfdata_KNUT3_simyr2000.nc")

print(a.natpft)

for i in a:
	if ((a[i].long_name == "monthly height top") or (a[i].long_name =="monthly height bottom")):
		print(a[i].long_name)
		print(a[i].values.squeeze().shape)

pft_acr = ["Bare soil","NET temperate", "NET boreal", "NDT Boreal", "BET tropical", "BET temperate", "BDT tropical", "BDT temperate", "BDT boreal", "BES temperate", "BDS temperate", "BDS boreal", "C3 arctic grass", "C3 grass", "C4 grass"]


pfts = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
relevant_pfts = [2,3,8,11] # corresponds to NET boreal, NDT Boreal, BDT boreal, BDS boreal

x_akse = ["		", "Jan","Feb","Mar","Apr", "Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

for i in relevant_pfts:
	print(pft_acr[i],a["MONTHLY_HEIGHT_TOP"].values.squeeze()[:,i])