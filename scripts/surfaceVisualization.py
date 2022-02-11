import xarray as xr 
import matplotlib.pyplot as plt
import numpy as np

sites = ["BESS1","GROT2","ROND3","KNUT3","DOVR0"]
sitenames = ["Jotunheimen","Groltli","Rondane","Knutshø","Dovre"]
pft_acr = ["Bare soil","NET temperate", "NET boreal", "NDT Boreal", "BET tropical", "BET temperate", "BDT tropical", "BDT temperate", "BDT boreal", "BES temperate", "BDS temperate", "BDS boreal", "C3 arctic grass", "C3 grass", "C4 grass"]
relevant_plants = [0,2,8,11,12]

table = np.zeros((len(sites),len(relevant_plants)))


for i,site in enumerate(sites):
	table[i,:] = xr.open_dataset("../resultater/inputdata/"+site+"/surfdata_"+site+"_simyr2000.nc").PCT_NAT_PFT[relevant_plants].values.squeeze()
print("Site            Bare soil   NET boreal   BDT boreal  BDS boreal  C3 arctic grass     sum")
for i in range(len(sites)):
	print("{:13s}{:12.2f}{:13.2f}{:13.2f}{:11.2f}{:10.2f}{:16.1f}".format(sitenames[i], table[i,0],table[i,1],table[i,2],table[i,3],table[i,4],sum(table[i,:])))



"""
Site            Bare soil   NET boreal   BDT boreal  BDS boreal  C3 arctic grass    sum
Jotunheimen          1.00        23.23         0.08      18.35     57.35           100.0
Groltli             11.61         3.45         0.42      23.26     61.26           100.0
Rondane              6.39         6.94         0.30       9.36     77.02           100.0
Knutshø              0.00         6.20         0.05      15.11     78.65           100.0
Dovre               49.10         1.27         0.12      13.22     36.27           100.0
"""