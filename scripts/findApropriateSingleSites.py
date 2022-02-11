import xarray as xr
import numpy as np
import glob 
import matplotlib.pyplot as plt

# KNUT3 DOVR0 BESS1 ROND3 GROT2
paf = "/home/gunnartl/Documents/master/resultater/ctsm/singleSites/*SDU/lnd/hist/*1991*.nc"

#files = ["/home/gunnartl/Documents/master/resultater/ctsm/singleSites/KNUT3_no_trees_or_shrubs_SDU/lnd/hist/KNUT3_no_trees_or_shrubs_SDU.clm2.h0.1991-01-01-00000.nc",
#		"/home/gunnartl/Documents/master/resultater/ctsm/singleSites/KNUT3_SDU/lnd/hist/KNUT3_SDU.clm2.h0.1991-01-01-00000.nc"]
#		"/home/gunnartl/Documents/master/resultater/ctsm/singleSites/DOVR0/lnd/hist/DOVR0.clm2.h0.1991-01-01-00000.nc",
#		"/home/gunnartl/Documents/master/resultater/ctsm/singleSites/BESS1/lnd/hist/BESS1.clm2.h0.1991-01-01-00000.nc",
#		"/home/gunnartl/Documents/master/resultater/ctsm/singleSites/ROND3/lnd/hist/ROND3.clm2.h0.1991-01-01-00000.nc",
#		"/home/gunnartl/Documents/master/resultater/ctsm/singleSites/GROT2/lnd/hist/GROT2.clm2.h0.1991-01-01-00000.nc"]



files = sorted(glob.glob(paf))

print(files)

hjerkiNorm = np.array([-6.8,  -7.2,  -5.2,  -1.0,  3.6,  8.0, 10.8,  9.7,  5.7,  0.1, -4.0,  -6.4])#,  0.6]) #9310
grotliNorm = np.array([-7.8,  -8.0,  -5.6,  -1.4,  3.1,  7.7, 11.1, 10.1,  6.3,  0.5, -4.2,  -7.6])#,  0.4]) #15890
høvrinNorm = np.array([-6.6,  -7.2,  -5.1,  -0.9,  3.8,  8.2, 11.2, 10.0,  6.0,  0.4, -3.8,  -6.4])#,  0.8])# 16271



rmse = 100

for i in files:
	file = xr.open_dataset(i)
	name = i[83:88]
	#print(file.time)
	normal = file.TSA.groupby("time.month").mean("time").values.squeeze()-273.15
	if (rmse > np.mean(np.sqrt((normal - hjerkiNorm)**2))):
		rmse = np.mean(np.sqrt((normal - hjerkiNorm)**2))
		print(np.mean(np.sqrt((normal - hjerkiNorm)**2)))
		print(name)
	plt.plot(normal,"--",label=name)




plt.plot(hjerkiNorm,label="Hjerkinn")
plt.plot(grotliNorm,label="Grotli")
plt.plot(høvrinNorm,label="Høvringen")
plt.legend()

plt.show()
