import xarray as xr 
import numpy as np

changeMask = np.load("../surface/changemask5.npy")

path_1920 = "/home/gunnartl/Documents/master/resultater/ctsm/southNorway1920/"
path_2020 = "/home/gunnartl/Documents/master/resultater/ctsm/southNorway2020/"

#daily resolution
d1995 = "southNorway_2020.clm2.h2.1995-01-01-00000.nc"
d2005 = "southNorway_2020.clm2.h2.2005-01-01-00000.nc"
d2015 = "southNorway_2020.clm2.h2.2015-01-01-00000.nc"

d1900 = "southNorway_1920.clm2.h2.1900-01-01-00000.nc"
d1910 = "southNorway_1920.clm2.h2.1910-01-01-00000.nc"
d1920 = "southNorway_1920.clm2.h2.1920-01-01-00000.nc"

variable = "QRUNOFF"

dailyNorway_1920 = xr.concat([xr.open_dataset(path_1920+d1900)[variable],xr.open_dataset(path_1920+d1910)[variable],xr.open_dataset(path_1920+d1920)[variable]],dim="time")
dailyNorway_2020 = xr.concat([xr.open_dataset(path_2020+d1995)[variable],xr.open_dataset(path_2020+d2005)[variable],xr.open_dataset(path_2020+d2015)[variable]],dim="time")


yearlyMean2020 = dailyNorway_2020.groupby("time.dayofyear").mean().values
yearlyMean1920 = dailyNorway_1920.groupby("time.dayofyear").mean().values

print("start")

import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 12,"font.family":"DejaVu Serif", "font.serif":["Computer Modern Roman"]})


print(yearlyMean1920[:,changeMask].shape)
plt.figure(figsize=(7,5))

plt.plot(3600*24*np.cumsum(np.nanmean(yearlyMean1920[:,changeMask],axis=1)),label="1920")#,ciao come va? alloraaaa maddaiii se fai il bravo ti do un biscotto! 
plt.plot(3600*24*np.cumsum(np.nanmean(yearlyMean2020[:,changeMask],axis=1)),label="2020")
plt.legend()
plt.xlabel("Day of year")
plt.ylabel("Total liquid runoff [$mm$]")
plt.title("Average runoff in gridcells with vegetation change")
plt.savefig("../figurer/cumulative"+variable+"AverageLine.pdf",format="pdf",dpi=300)
plt.savefig("../figurer/cumulative"+variable+"AverageLine.png",format="png",dpi=300) 
plt.show()

plt.figure(figsize=(7,5))
plt.plot(3600 * (np.nanmean(yearlyMean2020[:,changeMask],axis=1)-np.nanmean(yearlyMean1920[:,changeMask],axis=1)),label="2020-1920")
plt.xlabel("Day of year")
plt.legend()
plt.ylabel("$\Delta$ Total liquid runoff [$mm/h$]")
plt.title("Average change in runoff in gridcells with vegetation change")
plt.savefig("../figurer/delta"+variable+"AverageLine.pdf",format="pdf",dpi=300)
plt.savefig("../figurer/delta"+variable+"AverageLine.png",format="png",dpi=300) 

plt.show()

plt.figure(figsize=(7,5))
plt.plot(3600 *24 * np.cumsum((np.nanmean(yearlyMean2020[:,changeMask],axis=1)-np.nanmean(yearlyMean1920[:,changeMask],axis=1))),label="2020-1920")
plt.xlabel("Day of year")
plt.legend()
plt.ylabel("Cumulative $\Delta$ total liquid runoff [$mm$]")
plt.title("Cumulative change in runoff in gridcells with vegetation change")
plt.savefig("../figurer/cumulativeChange"+variable+"AverageLine.pdf",format="pdf",dpi=300)
plt.savefig("../figurer/cumulativeChange"+variable+"AverageLine.png",format="png",dpi=300) 

plt.show()

variable = "QVEGT"

dailyNorway_1920 = xr.concat([xr.open_dataset(path_1920+d1900)[variable],xr.open_dataset(path_1920+d1910)[variable],xr.open_dataset(path_1920+d1920)[variable]],dim="time")
dailyNorway_2020 = xr.concat([xr.open_dataset(path_2020+d1995)[variable],xr.open_dataset(path_2020+d2005)[variable],xr.open_dataset(path_2020+d2015)[variable]],dim="time")


yearlyMean2020 = dailyNorway_2020.groupby("time.dayofyear").mean().values
yearlyMean1920 = dailyNorway_1920.groupby("time.dayofyear").mean().values

print("start")

import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 12,"font.family":"DejaVu Serif", "font.serif":["Computer Modern Roman"]})


print(yearlyMean1920[:,changeMask].shape)
plt.figure(figsize=(7,5))

plt.plot(3600*24*np.cumsum(np.nanmean(yearlyMean1920[:,changeMask],axis=1)),label="1920")#,ciao come va? alloraaaa maddaiii se fai il bravo ti do un biscotto! 
plt.plot(3600*24*np.cumsum(np.nanmean(yearlyMean2020[:,changeMask],axis=1)),label="2020")
plt.legend()
plt.xlabel("Day of year")
plt.ylabel("Total transpiratin from vegetation [$mm$]")
plt.title("Cumulative transpiration in gridcells with vegetation change")
plt.savefig("../figurer/cumulative"+variable+"AverageLine.pdf",format="pdf",dpi=300)
plt.savefig("../figurer/cumulative"+variable+"AverageLine.png",format="png",dpi=300) 
plt.show()

plt.figure(figsize=(7,5))
plt.plot(3600 * (np.nanmean(yearlyMean2020[:,changeMask],axis=1)-np.nanmean(yearlyMean1920[:,changeMask],axis=1)),label="2020-1920")
plt.xlabel("Day of year")
plt.legend()
plt.ylabel("$\Delta$ Transpiration [$mm/h$]")
plt.title("Average change in transpiration in gridcells with vegetation change")
plt.savefig("../figurer/delta"+variable+"AverageLine.pdf",format="pdf",dpi=300)
plt.savefig("../figurer/delta"+variable+"AverageLine.png",format="png",dpi=300) 

plt.show()

cumSumTrans = np.cumsum((np.nanmean(yearlyMean2020[:,changeMask],axis=1)-np.nanmean(yearlyMean1920[:,changeMask],axis=1)))

plt.figure(figsize=(7,5))
plt.plot(3600 *24 * cumSumTrans,label="2020-1920")
plt.xlabel("Day of year")
plt.legend()
plt.ylabel("Cumulative $\Delta$ transpiration[$mm$]")
plt.title("Cumulative change in transpiration in gridcells with vegetation change")
plt.savefig("../figurer/cumulativeChange"+variable+"AverageLine.pdf",format="pdf",dpi=300)
plt.savefig("../figurer/cumulativeChange"+variable+"AverageLine.png",format="png",dpi=300) 

plt.show()


variable = "QVEGE"

dailyNorway_1920 = xr.concat([xr.open_dataset(path_1920+d1900)[variable],xr.open_dataset(path_1920+d1910)[variable],xr.open_dataset(path_1920+d1920)[variable]],dim="time")
dailyNorway_2020 = xr.concat([xr.open_dataset(path_2020+d1995)[variable],xr.open_dataset(path_2020+d2005)[variable],xr.open_dataset(path_2020+d2015)[variable]],dim="time")


yearlyMean2020 = dailyNorway_2020.groupby("time.dayofyear").mean().values
yearlyMean1920 = dailyNorway_1920.groupby("time.dayofyear").mean().values

print("start")

import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 12,"font.family":"DejaVu Serif", "font.serif":["Computer Modern Roman"]})


print(yearlyMean1920[:,changeMask].shape)
plt.figure(figsize=(7,5))

plt.plot(3600*24*np.cumsum(np.nanmean(yearlyMean1920[:,changeMask],axis=1)),label="1920")#,ciao come va? alloraaaa maddaiii se fai il bravo ti do un biscotto! 
plt.plot(3600*24*np.cumsum(np.nanmean(yearlyMean2020[:,changeMask],axis=1)),label="2020")
plt.legend()
plt.xlabel("Day of year")
plt.ylabel("Total evaporation from vegetation [$mm$]")
plt.title("Cumulative evaporatin from vegetation in gridcells with vegetation change")
plt.savefig("../figurer/cumulative"+variable+"AverageLine.pdf",format="pdf",dpi=300)
plt.savefig("../figurer/cumulative"+variable+"AverageLine.png",format="png",dpi=300) 
plt.show()

plt.figure(figsize=(7,5))
plt.plot(3600 * (np.nanmean(yearlyMean2020[:,changeMask],axis=1)-np.nanmean(yearlyMean1920[:,changeMask],axis=1)),label="2020-1920")
plt.xlabel("Day of year")
plt.legend()
plt.ylabel("$\Delta$ evaporation from vegetation [$mm/h$]")
plt.title("Average change in evaporation from vegetaition in gridcells with vegetation change")
plt.savefig("../figurer/delta"+variable+"AverageLine.pdf",format="pdf",dpi=300)
plt.savefig("../figurer/delta"+variable+"AverageLine.png",format="png",dpi=300) 

plt.show()

cumSumEvap = np.cumsum((np.nanmean(yearlyMean2020[:,changeMask],axis=1)-np.nanmean(yearlyMean1920[:,changeMask],axis=1)))

plt.figure(figsize=(7,5))
plt.plot(3600 *24 * cumSumEvap,label="2020-1920")
plt.xlabel("Day of year")
plt.legend()
plt.ylabel("Cumulative $\Delta$ evaporation from vegetation [$mm$]")
plt.title("Cumulative change in evaporation from vegetation in gridcells with vegetation change")
plt.savefig("../figurer/cumulativeChange"+variable+"AverageLine.pdf",format="pdf",dpi=300)
plt.savefig("../figurer/cumulativeChange"+variable+"AverageLine.png",format="png",dpi=300) 

plt.show()


plt.figure(figsize=(7,5))
plt.plot(3600 *24 * (cumSumEvap+cumSumTrans),label="2020-1920")
plt.xlabel("Day of year")
plt.legend()
plt.ylabel("Cumulative $\Delta$ evapotranspiration [$mm$]")
plt.title("Cumulative change in evapotranspiration in gridcells with vegetation change")
plt.savefig("../figurer/cumulativeChange"+"EvapTrans"+"AverageLine.pdf",format="pdf",dpi=300)
plt.savefig("../figurer/cumulativeChange"+"EvapTrans"+"AverageLine.png",format="png",dpi=300) 

plt.show()