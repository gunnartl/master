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

qmean1920 = np.nanmean(yearlyMean1920,axis=0)

cumsumchange = np.cumsum(yearlyMean2020 - yearlyMean1920, axis=0)

print(cumsumchange.shape)


from cartopy.io import shapereader
import numpy as np
import geopandas
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 12,"font.family":"DejaVu Serif", "font.serif":["Computer Modern Roman"]})
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
#divnorm=colors.TwoSlopeNorm(vmin=135., vcenter=250., vmax=365)

extremeVal = 40

plt.pcolormesh(dailyNorway_1920.lon,dailyNorway_1920.lat,3600*24*cumsumchange[-1,:,:],cmap="bwr", vmin=-extremeVal,vmax=extremeVal)
plt.title("Change in yearly runoff")
plt.colorbar(label="$\Delta$ mm")
plt.savefig("../figurer/deltaQRUNOFFMap.pdf",format="pdf",dpi=300)
plt.savefig("../figurer/deltaQRUNOFFMap.png",format="png",dpi=300)

surf1920 = xr.open_dataset("../surface/southNorway-pft8xtest1920_TL.nc")

print("tonn med vann: ",np.nansum(surf1920.AREA*3600*24*cumsumchange[-1,:,:]))

#plt.show()

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
#divnorm=colors.TwoSlopeNorm(vmin=135., vcenter=250., vmax=365)

extremeVal = 20

plt.pcolormesh(dailyNorway_1920.lon,dailyNorway_1920.lat,(cumsumchange[-1,:,:]/qmean1920),cmap="bwr", vmin=-extremeVal,vmax=extremeVal)
plt.title("Change in yearly relative runoff")
plt.colorbar(label="% change")
plt.savefig("../figurer/deltaRelativeQRUNOFFMap.pdf",format="pdf",dpi=300)
plt.savefig("../figurer/deltaRelativeQRUNOFFMap.png",format="png",dpi=300)


plt.show()
"""
import matplotlib.pyplot as plt

#plt.rcParams["figure.constrained_layout.use"]=True



plt.plot(3600*24*(np.cumsum(np.nanmean(yearlyMean2020[:,changeMask],axis=1))-np.cumsum(np.nanmean(yearlyMean1920[:,changeMask],axis=1))),label="2020-1920")
plt.legend()
plt.xlabel("Day of year")
plt.ylabel("Total liquid runoff [$mm$]")
plt.title("Runoff in gridcells with vegetation change")
plt.show()
"""