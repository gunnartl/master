import xarray as xr
import numpy as np
from rasterio.warp import transform

surface = xr.open_dataset("surfdata_360x720cru_16pfts_Irrig_CMIP6_simyr2000_scand_c170824.nc")

prøvegreie = surface.PCT_NAT_PFT.values.copy()
print(np.asarray([prøvegreie[0],prøvegreie[1]]).shape)

plant_acr = ["Bare soil","NET temperate", "NET boreal", "NDT Boreal", "BET tropical", "BET temperate", "BDT tropical", "BDT temperate", "BDT boreal", "BES temperate", "BDS temperate", "BDS boreal", "C3 arctic grass", "C3 grass", "C4 grass"]

tif = "change_TL.tif"

flippedipp = xr.open_rasterio(tif)


# Compute the lon/lat coordinates with rasterio.warp.transform
ny, nx = len(flippedipp['y']), len(flippedipp['x'])
x, y = np.meshgrid(flippedipp['x'], flippedipp['y'])

# Rasterio works with 1D arrays
lon, lat = transform(flippedipp.crs, {'init': 'EPSG:4326'},x.flatten(), y.flatten())
lon = np.asarray(lon).reshape((ny, nx))
lat = np.asarray(lat).reshape((ny, nx))
flippedipp.coords['lon'] = (('y', 'x'), lon)
flippedipp.coords['lat'] = (('y', 'x'), lat)

flippedipp_masked = flippedipp.where(flippedipp.values > -9999)

print(flippedipp)
import matplotlib.pyplot as plt

plants = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
relevant_plants = [2,3,8,11]
"""
for i in relevant_plants:
    fig, ax = plt.subplots(nrows=1)
    im = ax.pcolormesh(surface.lsmlon.values,surface.lsmlat.values,surface.PCT_NAT_PFT.values[i,:,:])
    #im = ax.pcolormesh(surface.lsmlon.values,surface.lsmlat.values,surface.LANDFRAC_PFT.values)
    ax.set_title(plant_acr[i])
    fig.colorbar(im,ax=ax)

"""
plt.pcolormesh(flippedipp.lon,flippedipp.lat, flippedipp_masked.values.squeeze())
plt.show()

"""    

kart   =  np.zeros_like(surface.PCT_NAT_PFT.values[0])
nummer =  np.zeros_like(kart)
print(flippedipp.data.shape)

surf_lat = surface.lsmlat.values
surf_lon = surface.lsmlon.values

lats=flippedipp.lat.values.ravel()
lons=flippedipp.lon.values.ravel()
data=flippedipp_masked.data.ravel()

def find_nearest_idx(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

for i in range(len(lats)):
    lat_idx = find_nearest_idx(surf_lat,lats[i])
    lon_idx = find_nearest_idx(surf_lon,lons[i])
    if not np.isnan(data[i]):
        kart[lat_idx,lon_idx] += data[i]
        nummer[lat_idx,lon_idx] += 1

mask = kart/nummer

fig, ax = plt.subplots(nrows=1)
im = ax.pcolormesh(mask)
fig.colorbar(im,ax=ax)


for i in relevant_plants:
    prøvegreie[i]=np.nanprod(np.asarray([prøvegreie[i],mask]),axis=0)
    print(np.nanprod(np.asarray([prøvegreie[i],mask]),axis=0).shape, "heisveis")

fig, ax = plt.subplots(nrows=1)
im = ax.pcolormesh(prøvegreie[2]-surface.PCT_NAT_PFT[2])
fig.colorbar(im,ax=ax)

sums = np.sum(prøvegreie,axis=0)


surface.PCT_NAT_PFT.values=prøvegreie/np.sum(prøvegreie,axis=0) *100 

surface.to_netcdf("surfdata_360x720cru_16pfts_Irrig_CMIP6_simyr2000_scand_c170824_basic_"+tif[-11:-4]+".nc")

fig, ax = plt.subplots(nrows=1)
im = ax.pcolormesh(np.sum(surface.PCT_NAT_PFT/np.sum(surface.PCT_NAT_PFT,axis=0),axis=0))
fig.colorbar(im,ax=ax)
plt.show()

"""