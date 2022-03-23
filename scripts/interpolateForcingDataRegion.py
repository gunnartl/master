import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

import pyproj
import math

P = pyproj.Proj(proj='utm', zone=33, ellps='WGS84', preserve_units=True)

def LatLon_To_XY(Lat,Lon):
    return P(Lat,Lon)    

def XY_To_LatLon(x,y):
    return P(x,y,inverse=True) 

surface = "../surface/surfdata_fenno_5x5km_simyr2000_southNorway_c181116.nc"

surfaceData = xr.open_dataset(surface)

lon = surfaceData.lon.values
lat = surfaceData.lat.values

surfaceData.close()

meshLon,meshLat = np.meshgrid(lon,lat)

meshY,meshX = LatLon_To_XY(meshLat,meshLon)

plt.pcolormesh(meshX,meshY,surfaceData.PCT_NAT_PFT[2])
plt.show()


forcingdata = xr.open_dataset("Solar/clmforc.COSMOREA6.Solr.1995-01.nc",decode_times=False)
times = forcingdata.time
#data = forcingdata.SWDIFDS_RAD.values
#lat  = forcingdata.LATIXY.values
#lon  = forcingdata.LONGXY.values
#plt.pcolormesh(lon,lat,data)
#plt.scatter(meshLon,meshLat)
#plt.show()

interpolert = np.zeros([times.size,lat.size,lon.size])
print(interpolert.shape,forcingdata.SWDIFDS_RAD.shape)

for i in range(times.size):
	print(i)
	Y,X = LatLon_To_XY(forcingdata.LATIXY.values,forcingdata.LONGXY.values)
	interpolert[i] = interpolate.griddata((X.flatten(), Y.flatten())
                                  , forcingdata.SWDIFDS_RAD.values[i].flatten()
                                  , (meshX, meshY)
                                  , method="linear"
                                  )




#plt.pcolormesh(meshLon,meshLat,interpolert,cmap="plasma")
#plt.show()


ds = xr.Dataset({
    'SWDIFDS_RAD': xr.DataArray(
                data   = interpolert,
                dims   = ['time',"lat","lon"],
                coords = {'time': times,"lat":np.arange(lat.size),"lon":np.arange(lon.size)},
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
print(ds)
ds.to_netcdf("test_interp.nc")

"""
T
WIND
Q
PS
FLDS

PRECIPmms

"""