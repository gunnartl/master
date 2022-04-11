import xarray as xr 
import matplotlib.pyplot as plt
#from matplotlib.font_manager import FontProperties
import numpy as np
import time

from cartopy.io import shapereader
import numpy as np
import geopandas
plt.rcParams.update({'font.size': 12,"font.family":"DejaVu Serif", "font.serif":["Computer Modern Roman"]})

import cartopy.crs as ccrs
from matplotlib import colors

plotMask = np.ndarray.astype(np.load("../surface/surfaceMask.np.npy"),int)



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

#dailyNorway_1920 = xr.concat([xr.open_dataset(path_1920+d1900).FSNO,xr.open_dataset(path_1920+d1910).FSNO,xr.open_dataset(path_1920+d1920).FSNO],dim="time")
#dailyNorway_2020 = xr.concat([xr.open_dataset(path_2020+d1995).FSNO,xr.open_dataset(path_2020+d2005).FSNO,xr.open_dataset(path_2020+d2015).FSNO],dim="time")

variables = ["TSKIN","TSA","EFLX_LH_TOT","FSH","FIRA","FSH_G","FSR","FSH_V","FSA"]

monthlyNorway_1920 = xr.concat([xr.open_dataset(path_1920+m1900)[variables],xr.open_dataset(path_1920+m1910)[variables],xr.open_dataset(path_1920+m1920)[variables]],dim="time")
monthlyNorway_2020 = xr.concat([xr.open_dataset(path_2020+m1995)[variables],xr.open_dataset(path_2020+m2005)[variables],xr.open_dataset(path_2020+m2015)[variables]],dim="time")

print(monthlyNorway_1920.TSKIN.min())

def mapPlotter(vals,lon,lat, extremes, cbar, title, filename):

	# get country borders
	resolution = '10m'
	category = 'cultural'
	name = 'admin_0_countries'

	shpfilename = shapereader.natural_earth(resolution, category, name)

	# read the shapefile using geopandas
	df = geopandas.read_file(shpfilename)

	# read the Norwegian borders
	poly = df.loc[df['ADMIN'] == 'Norway']['geometry'].values[0] # Omriss av norge for bruk i alle plot
	
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
	divnorm=colors.TwoSlopeNorm(vmin=-extremes, vcenter=0., vmax=extremes)
	plt.pcolormesh(lon,lat,vals*plotMask,cmap="bwr",norm=divnorm)
	plt.colorbar(label=cbar)
	plt.title(title)
	plt.tight_layout()
	plt.savefig(filename+".pdf",format="pdf",dpi=300)
	plt.savefig(filename+".png",format="png",dpi=300) 
	plt.show()


# Soil temp upper layer 
plotValues = np.mean(monthlyNorway_2020.TSKIN.values-monthlyNorway_1920.TSKIN.values,axis=0)
mapPlotter(plotValues,monthlyNorway_1920.lon,monthlyNorway_1920.lat,max(abs(plotValues.ravel())),"$\Delta ^o$C","Change in soil temperature - yearly average", "../figurer/deltaTSKINRegion")

# Latent het flux 
plotValues = np.mean(monthlyNorway_2020.EFLX_LH_TOT.values-monthlyNorway_1920.EFLX_LH_TOT.values,axis=0)
mapPlotter(plotValues,monthlyNorway_1920.lon,monthlyNorway_1920.lat,max(abs(plotValues.ravel())),"$\Delta$ W/$m^2$","Change in latent heat flux - yearly average", "../figurer/deltaEFLX_LH_TOTRegion")

# Sensible heat flux 
plotValues = np.mean(monthlyNorway_2020.FSH.values-monthlyNorway_1920.FSH.values,axis=0)
mapPlotter(plotValues,monthlyNorway_1920.lon,monthlyNorway_1920.lat,max(abs(plotValues.ravel())),"$\Delta$ W/$m^2$","Change in sensible heat flux - yearly average", "../figurer/deltaFSHRegion")

# Ground heat flux  
plotValues = np.mean(monthlyNorway_2020.FSH_G.values-monthlyNorway_1920.FSH_G.values,axis=0)
mapPlotter(plotValues,monthlyNorway_1920.lon,monthlyNorway_1920.lat,max(abs(plotValues.ravel())),"$\Delta$ W/$m^2$","Change in ground heat flux - yearly average", "../figurer/deltaFSH_GRegion")

# Absorbed radiation 
plotValues = np.mean(monthlyNorway_2020.FSA.values-monthlyNorway_1920.FSA.values,axis=0)
mapPlotter(plotValues,monthlyNorway_1920.lon,monthlyNorway_1920.lat,max(abs(plotValues.ravel())),"$\Delta$ W/$m^2$","Change in absorbed solar radiation - yearly average", "../figurer/deltaFSARegion")

# Relative change absorbed radiation: 
plotValues = np.mean(monthlyNorway_2020.FSA.values-monthlyNorway_1920.FSA.values,axis=0)/np.mean(monthlyNorway_1920.FSA.values,axis=0)
mapPlotter(plotValues,monthlyNorway_1920.lon,monthlyNorway_1920.lat,max(abs(plotValues.ravel())),"%$\Delta$","Relative change in absorbed solar radiation - yearly average", "../figurer/relativeDeltaFSARegion")

# LW radiation: 
plotValues = np.mean(monthlyNorway_2020.FIRA.values-monthlyNorway_1920.FIRA.values,axis=0)/np.mean(monthlyNorway_1920.FSA.values,axis=0)
mapPlotter(plotValues,monthlyNorway_1920.lon,monthlyNorway_1920.lat,max(abs(plotValues.ravel())),"$\Delta$ W/$m^2$","Change in net longwave radiation - yearly average", "../figurer/deltaFIRARegion")
