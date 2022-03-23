import xarray as xr 
import matplotlib.pyplot as plt
#from matplotlib.font_manager import FontProperties
import numpy as np
import time

from matplotlib import colors

plotMask = np.ndarray.astype(np.load("../surface/surfaceMask.np.npy"),int)

print(plotMask.shape)

#font = FontProperties()
#font.set_family('serif')
#font.set_size("12")

print("gottem")


path_1920 = "/home/gunnartl/Documents/master/resultater/ctsm/southNorway1920/"
path_2020 = "/home/gunnartl/Documents/master/resultater/ctsm/southNorway2020/"

#monthly resolution
m1995 = "southNorway_2020.clm2.h0.1995-02-01-00000.nc"
m2005 = "southNorway_2020.clm2.h0.2005-02-01-00000.nc"
m2015 = "southNorway_2020.clm2.h0.2015-02-01-00000.nc"

m1900 = "southNorway_1920.clm2.h0.1900-02-01-00000.nc"
m1910 = "southNorway_1920.clm2.h0.1910-02-01-00000.nc"
m1920 = "southNorway_1920.clm2.h0.1920-02-01-00000.nc"

#diurnal resolution
d1995 = "southNorway_2020.clm2.h1.1995-01-01-00000.nc"
d2005 = "southNorway_2020.clm2.h1.2005-01-01-00000.nc"
d2015 = "southNorway_2020.clm2.h1.2015-01-01-00000.nc"

d1900 = "southNorway_1920.clm2.h1.1900-01-01-00000.nc"
d1910 = "southNorway_1920.clm2.h1.1910-01-01-00000.nc"
d1920 = "southNorway_1920.clm2.h1.1920-01-01-00000.nc"

#print(xr.open_dataset(path_1920+m1920).FSA.mean())

dailyNorway_1920 = xr.concat([xr.open_dataset(path_1920+d1900).FSNO,xr.open_dataset(path_1920+d1910).FSNO,xr.open_dataset(path_1920+d1920).FSNO],dim="time")
dailyNorway_2020 = xr.concat([xr.open_dataset(path_2020+d1995).FSNO,xr.open_dataset(path_2020+d2005).FSNO,xr.open_dataset(path_2020+d2015).FSNO],dim="time")

variable = "TSKIN"

#monthlyNorway_1920 = xr.concat([xr.open_dataset(path_1920+m1900)[variable],xr.open_dataset(path_1920+m1910)[variable],xr.open_dataset(path_1920+m1920)[variable]],dim="time")
#monthlyNorway_2020 = xr.concat([xr.open_dataset(path_2020+m1995)[variable],xr.open_dataset(path_2020+m2005)[variable],xr.open_dataset(path_2020+m2015)[variable]],dim="time")

#print(dailyNorway_1920)

snowDays2020 = np.nansum((dailyNorway_2020.groupby("time.dayofyear").mean().values > 0),axis=0)
snowDays1920 = np.nansum((dailyNorway_1920.groupby("time.dayofyear").mean().values > 0),axis=0)

plt.figure(figsize=(10,5))
plt.rcParams.update({'font.size': 12,"font.family":"DejaVu Serif", "font.serif":["Computer Modern Roman"]})

from cartopy.io import shapereader
import numpy as np
import geopandas
import matplotlib.pyplot as plt

import cartopy.crs as ccrs

# get natural earth data (http://www.naturalearthdata.com/)

# get country borders
resolution = '10m'
category = 'cultural'
name = 'admin_0_countries'

shpfilename = shapereader.natural_earth(resolution, category, name)

# read the shapefile using geopandas
df = geopandas.read_file(shpfilename)

# read the Norwegian borders
poly = df.loc[df['ADMIN'] == 'Norway']['geometry'].values[0]

plt.figure(figsize=(7,5))
ax = plt.axes(projection=ccrs.PlateCarree())



ax.add_geometries(poly, crs=ccrs.PlateCarree(), facecolor='none', 
                  edgecolor='0.5')
ax.set_aspect('auto')
ax.set_ylim([60.4, 62.75])
ax.set_xlim([6.4, 12.4])
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_xticks([7,8,9,10,11,12])
ax.set_yticks([60.5,61,61.5,62,62.5])
divnorm=colors.TwoSlopeNorm(vmin=135., vcenter=250., vmax=365)

plt.pcolormesh(dailyNorway_1920.lon,dailyNorway_1920.lat,(snowDays1920),cmap="winter", norm = divnorm)
plt.colorbar(label="$\Delta$ days")
plt.title("Average number of snow days per year 1920")


plt.tight_layout()
plt.savefig("../figurer/avgSnowDaysRegion1920.pdf",format="pdf",dpi=300)
plt.savefig("../figurer/avgSnowDaysRegion1920.png",format="png",dpi=300)

plt.show()

plt.figure(figsize=(7,5))
ax = plt.axes(projection=ccrs.PlateCarree())



ax.add_geometries(poly, crs=ccrs.PlateCarree(), facecolor='none', 
                  edgecolor='0.5')
ax.set_aspect('auto')
ax.set_ylim([60.4, 62.75])
ax.set_xlim([6.4, 12.4])
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_xticks([7,8,9,10,11,12])
ax.set_yticks([60.5,61,61.5,62,62.5])
divnorm=colors.TwoSlopeNorm(vmin=135, vcenter=250., vmax=365)

plt.pcolormesh(dailyNorway_1920.lon,dailyNorway_1920.lat,(snowDays2020),cmap="winter", norm = divnorm)
plt.colorbar(label="$\Delta$ days")
plt.title("Average number of snow days per year 1920")


plt.tight_layout()
plt.savefig("../figurer/avgSnowDaysRegion2020.pdf",format="pdf",dpi=300)
plt.savefig("../figurer/avgSnowDaysRegion2020.png",format="png",dpi=300)

plt.show()

absorbed1920 = months_1920.FSA.values
absorbed2020 = months_2020.FSA.values

"""
verdier = np.mean(monthlyNorway_2020.values-monthlyNorway_1920.values,axis=0)


plt.figure(figsize=(10,5))
plt.rcParams.update({'font.size': 12,"font.family":"DejaVu Serif", "font.serif":["Computer Modern Roman"]})
divnorm=colors.TwoSlopeNorm(vmin=-max(abs(verdier.ravel())), vcenter=0., vmax=max(abs(verdier.ravel())))
plt.pcolormesh(monthlyNorway_1920.lon,monthlyNorway_1920.lat,verdier,cmap="seismic",norm=divnorm)
plt.colorbar(label="$\Delta ^o$C")
plt.title("Change in soil temperature - yearly average")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.savefig("../figurer/delta"+variable+"Region.pdf",format="pdf",dpi=300)
plt.savefig("../figurer/delta"+variable+"Region.png",format="png",dpi=300) 
plt.show()



snitt1920 = monthlyNorway_1920.groupby("time.month").mean()
snitt2020 = monthlyNorway_2020.groupby("time.month").mean()

plot2 = np.zeros(12)
plot1 = np.zeros(12)

for i in range(35,40):
	for j in range(60,80):
		plot1 += snitt2020[:,i,j]
		plot2 += snitt1920[:,i,j]

plt.plot(plot1)
plt.plot(plot2)
#plt.plot(np.mean(np.mean(snitt2020,axis=1),axis=1))
#plt.plot(np.mean(np.mean(snitt1920,axis=1),axis=1))
plt.show()

from cartopy.io import shapereader
import numpy as np
import geopandas
import matplotlib.pyplot as plt

import cartopy.crs as ccrs

# get natural earth data (http://www.naturalearthdata.com/)

# get country borders
resolution = '10m'
category = 'cultural'
name = 'admin_0_countries'

shpfilename = shapereader.natural_earth(resolution, category, name)

# read the shapefile using geopandas
df = geopandas.read_file(shpfilename)

# read the Norwegian borders
poly = df.loc[df['ADMIN'] == 'Norway']['geometry'].values[0]

plt.figure(figsize=(10,5))
ax = plt.axes(projection=ccrs.PlateCarree())



ax.add_geometries(poly, crs=ccrs.PlateCarree(), facecolor='none', 
                  edgecolor='0.5')

ax.set_extent([6.5, 12.5, 60.4, 62.75], crs=ccrs.PlateCarree())
ax.pcolormesh(monthlyNorway_1920.lon,monthlyNorway_1920.lat,verdier,cmap="seismic",norm=divnorm)

plt.show()"""



"""
temp1920 = months_1920.TSA.values
temp2020 = months_2020.TSA.values

plt.figure(figsize=(10,5))
plt.rcParams.update({'font.size': 12,"font.family":"serif"})
divnorm=colors.TwoSlopeNorm(vmin=-.3, vcenter=0., vmax=.3)
plt.pcolormesh(norway_1920.lon,norway_1920.lat,np.mean(temp2020-temp1920,axis=0),cmap="seismic",norm=divnorm)
plt.colorbar(label="$\Delta$ degrees  C")
plt.title("Change in 2m temperature - yearly average")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.savefig("../figurer/deltaTRegion.pdf",format="pdf",dpi=300) 


lh1920 = months_1920.EFLX_LH_TOT.values
lh2020 = months_2020.EFLX_LH_TOT.values

plt.figure(figsize=(10,5))
plt.rcParams.update({'font.size': 12,"font.family":"serif"})
divnorm=colors.TwoSlopeNorm(vmin=-3, vcenter=0., vmax=3)
plt.pcolormesh(norway_1920.lon,norway_1920.lat,np.mean(lh2020-lh1920,axis=0),cmap="seismic",norm=divnorm)
plt.colorbar(label="$\Delta$ degrees  C")
plt.title("Change in latent heat flux - yearly average")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.savefig("../figurer/deltaLhRegion.pdf",format="pdf",dpi=300) 
plt.show()

"""