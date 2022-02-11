import xarray as xr 
import matplotlib.pyplot as plt
import numpy as np
file = xr.open_dataset("~/Documents/master/resultater/ctsm/singleSites/BESS1_no_trees_or_shrubs_SDU/lnd/hist/BESS1_no_trees_or_shrubs_SDU.clm2.h0.2001-01-01-00000.nc")
andrefila = xr.open_dataset("~/Documents/master/resultater/ctsm/singleSites/BESS1_SDU/lnd/hist/BESS1_SDU.clm2.h0.2001-01-01-00000.nc")


solar = file.FSA#.groupby("time.dayofyear").mean("time") #- 273.15
solarTree = andrefila.FSA#.groupby("time.dayofyear").mean("time") #-273.15

latflux = file.EFLX_LH_TOT#.groupby("time.dayofyear").mean("time")
latfluxTree = andrefila.EFLX_LH_TOT#.groupby("time.dayofyear").mean("time")

sensFlux = file.FSH#.groupby("time.dayofyear").mean("time")
sensFluxTree = andrefila.FSH#.groupby("time.dayofyear").mean("time")

lw = file.FIRA
lwTree = andrefila.FIRA

#EFLX_LH_TOT - total latent energiflux
#TSA - 2m temp
#FSNO - brøkdel som er snødekt
#SNOW_PERSITENACE -  
#FSA - absoberd solar radiation
#FIRA - net long wave 
# FSH_V sensible heat fom veg
# FCEV - canopy evaporation
# DHSDT_CANOPY caopy heat storage 

ground = file.FGR
groundTree = andrefila.FGR

canopyHeat = file.DHSDT_CANOPY
canopyHeatTree = andrefila.DHSDT_CANOPY

plt.plot(solar - sensFlux - latflux- lw - ground - file.DHSDT_CANOPY)

plt.plot(solarTree - sensFluxTree - latfluxTree - lwTree - groundTree - andrefila.DHSDT_CANOPY,alpha=.7)
plt.legend(["no trees", "Trees"])
plt.show()
#plt.plot((solar - sensFlux - latflux - lw - ground - canopyHeat) - (solarTree - sensFluxTree - latfluxTree - lwTree - groundTree - canopyHeatTree ))
#plt.plot(file.FSNO)
#plt.show()
print(np.mean((solar - sensFlux - latflux -lw - ground)))
print(np.mean((solarTree - sensFluxTree - latfluxTree -lwTree - groundTree)))

plt.plot(lw.groupby('time.month').mean(),label="No trees")
plt.plot(lwTree.groupby("time.month").mean(),label="Prescribed vegatation")
plt.legend()
plt.title("Longwave radiation")
plt.show()

plt.plot(latflux.groupby('time.month').mean(),label="No trees")
plt.plot(latfluxTree.groupby("time.month").mean(),label="Prescribed vegatation")
plt.title("Latent heat flux monthly average")
plt.legend()
plt.show()

plt.plot(andrefila.FSR.groupby('time.month').mean(),label="No trees")
plt.plot(file.FSR.groupby("time.month").mean(),label="Prescribed vegatation")
plt.title("Reflected solar radiation")
plt.legend()
plt.show()



"""
files = ["/home/gunnartl/Documents/master/resultater/ctsm/singleSites/BESS1_no_trees_or_shrubs_SDU/lnd/hist/BESS1_no_trees_or_shrubs_SDU.clm2.h0.1991-01-01-00000.nc",
		"/home/gunnartl/Documents/master/resultater/ctsm/singleSites/BESS1_SDU/lnd/hist/BESS1_SDU.clm2.h0.1991-01-01-00000.nc"]

notreetemps  = xr.open_dataset(files[0]).TSA.values
treetemps = xr.open_dataset(files[1]).TSA.values

plt.plot(treetemps[::2]-notreetemps[::2])
plt.plot(treetemps[1::2]-notreetemps[1::2])

plt.show()

notreetemps  = xr.open_dataset(files[0]).FSNO.groupby("time.dayofyear").mean("time")
treetemps = xr.open_dataset(files[1]).FSNO.groupby("time.dayofyear").mean("time")


plt.plot(treetemps)
plt.plot(notreetemps)
plt.show()"""

for i in file.variables:
	try:
		if file[i].units == "W/m^2":
			if(abs(file[i].values.mean()) < 10):
				#plt.plot(file[i])
				#plt.title(i)
				#plt.show()
				i=3
	except:
		continue
