import xarray as xr 
import glob 
import numpy as np
from scipy import interpolate


import pyproj
import math

P = pyproj.Proj(proj='utm', zone=33, ellps='WGS84', preserve_units=True)

def LatLon_To_XY(Lat,Lon):
    return P(Lat,Lon)    

def XY_To_LatLon(x,y):
    return P(x,y,inverse=True)

surface = "surfdata_fenno_5x5km_simyr2000_southNorway_c181116.nc"

surfaceData = xr.open_dataset(surface)

lon = surfaceData.lon.values
lat = surfaceData.lat.values

surfaceData.close()

meshLon,meshLat = np.meshgrid(lon,lat)

meshY,meshX = LatLon_To_XY(meshLat,meshLon)


solarPath = "../Solar/*2016-02g*"
solarFiles = glob.glob(solarPath)
solarVars = ["SWDIFDS_RAD","SWDIRS_RAD"]

precipPath = "../Precip/*2019gdf*"
precipFiles = glob.glob(precipPath)

tphwlPath = "../TPHWL/*2016-02*"
tphwlFiles = glob.glob(tphwlPath)
tphwdVars = ["T","WIND","Q","PS","FLDS"]

forcingFiles = sorted(solarFiles+precipFiles+tphwlFiles)

print(forcingFiles)
for filename in forcingFiles:
	print(filename[3:])
	file = xr.open_dataset(filename,decode_times=False)
	#file.time.encode["units"] = "hours since 1995-12-01 01:00:00+0"
	#crop = file.where((file.lat>604) & (file.lat<650) & (file.lon<469) & (file.lon>348),drop=True)
	crop = file.isel(lat=slice(603,653),lon=slice(410,470)) # hardcoded to cover area, could be automated
	file.close()
	#crop = file.isel(LATIXY=slice(maxLat,minLat),LONGXY=slice(maxLon,minLon))
	#crop = file.where((file.LATIXY<maxLat)&(file.LATIXY>minLat)&(file.LONGXY<maxLon)&(file.LONGXY>minLon),drop=True)
	if filename.split("/")[1]=="Solar":
		times = crop.time
		interpolert = np.zeros([len(solarVars),crop.time.size,lat.size,lon.size])
        for j in range(len(solarVars)):
    		for i in range(crop.time.size):
    			
    			Y,X = LatLon_To_XY(crop.LATIXY.values,crop.LONGXY.values)
    			interpolert[j,i] = interpolate.griddata((X.flatten(), Y.flatten())
                                      , crop.[solarVars[j]].values[i].flatten()
                                      , (meshX, meshY)
                                      , method="linear"
                                      )

		ds = xr.Dataset({
    		'SWDIFDS_RAD': xr.DataArray(
                data   = interpolert[0],
                dims   = ['time',"lat","lon"],
                coords = {'time': times,"lat":lat,"lon":lon},
                attrs  = {
                    '_FillValue': -999.9,
                    'units'     : 'W/m2'
                    }
                ),
            'SWDIRS_RAD': xr.DataArray(
                data   = interpolert[1],
                dims   = ['time',"lat","lon"],
                coords = {'time': times,"lat":lat,"lon":lon},
                attrs  = {
                    '_FillValue': -999.9,
                    'units'     : 'W/m2'
                    }
                ),
    		'LATIXY': xr.DataArray(
                data   = meshLat,
                dims   = ['lat',"lon"],
                ),
    		'LONGXY': xr.DataArray(
                data   = meshLon,
                dims   = ['lat',"lon"],
                )
            },
        attrs = {'history': 'extracted and interpolated from COSMOREA6-data'}
    	)
		ds.to_netcdf(filename[3:])

	if filename.split("/")[1]=="Precip":
		times = crop.time
		interpolert = np.zeros([crop.time.size,lat.size,lon.size])
		for i in range(crop.time.size):
			
			Y,X = LatLon_To_XY(crop.LATIXY.values,crop.LONGXY.values)
			interpolert[i] = interpolate.griddata((X.flatten(), Y.flatten())
                                  , crop.PRECIPmms.values[i].flatten()
                                  , (meshX, meshY)
                                  , method="linear"
                                  )

		ds = xr.Dataset({
    		'PRECIPmms': xr.DataArray(
                data   = interpolert,
                dims   = ['time',"lat","lon"],
                coords = {'time': times,"lat":lat,"lon":lon},
                ),
    		'LATIXY': xr.DataArray(
                data   = meshLat,
                dims   = ['lat',"lon"],
                ),
    		'LONGXY': xr.DataArray(
                data   = meshLon,
                dims   = ['lat',"lon"],
                )
            },
        attrs = {'history': 'extracted and interpolated from COSMOREA6-data'}
    	)
		ds.to_netcdf(filename[3:])

	if filename.split("/")[1]=="TPHWL":
		times = crop.time
		interpolert = np.zeros([len(tphwdVars),crop.time.size,lat.size,lon.size])
		for j in range(len(tphwdVars)):
			for i in range(crop.time.size):
				
				Y,X = LatLon_To_XY(crop.LATIXY.values,crop.LONGXY.values)
				interpolert[j,i] = interpolate.griddata((X.flatten(), Y.flatten())
	                                  , crop[tphwdVars[j]].values[i].flatten()
	                                  , (meshX, meshY)
	                                  , method="linear"
	                                  )

		ds = xr.Dataset({
    		'T': xr.DataArray(
                data   = interpolert[0],
                dims   = ['time',"lat","lon"],
                coords = {'time': times,"lat":lat,"lon":lon},
                ),
    		'WIND': xr.DataArray(
                data   = interpolert[1],
                dims   = ['time',"lat","lon"],
                coords = {'time': times,"lat":lat,"lon":lon},
                ),
    		'Q': xr.DataArray(
                data   = interpolert[2],
                dims   = ['time',"lat","lon"],
                coords = {'time': times,"lat":lat,"lon":lon},
                ),
    		'PS': xr.DataArray(
                data   = interpolert[3],
                dims   = ['time',"lat","lon"],
                coords = {'time': times,"lat":lat,"lon":lon},
                ),
    		'FLDS': xr.DataArray(
                data   = interpolert[4],
                dims   = ['time',"lat","lon"],
                coords = {'time': times,"lat":lat,"lon":lon},
                ),
    		'LATIXY': xr.DataArray(
                data   = meshLat,
                dims   = ['lat',"lon"],
                ),
    		'LONGXY': xr.DataArray(
                data   = meshLon,
                dims   = ['lat',"lon"],
                )
            },
        attrs = {'history': 'extracted and interpolated from COSMOREA6-data'}
    	)
		ds.to_netcdf(filename[3:])


	#crop.to_netcdf(filename[3:])

