import xarray as xr
import numpy as np
from rasterio.warp import transform

import rasterio as rio


surface = xr.open_dataset("surfdata_fenno_5x5km_simyr2000_southNorway_c181116.nc")

prøvegreie = surface.PCT_NAT_PFT.values.copy()
print(np.asarray([prøvegreie[0],prøvegreie[1]]).shape)

plant_acr = ["Bare soil","NET temperate", "NET boreal", "NDT Boreal", "BET tropical", "BET temperate", "BDT tropical", "BDT temperate", "BDT boreal", "BES temperate", "BDS temperate", "BDS boreal", "C3 arctic grass", "C3 grass", "C4 grass"]

tif = "binary_2020_TL.tif"

binary = xr.open_rasterio(tif)


# Compute the lon/lat coordinates with rasterio.warp.transform
ny, nx = len(binary['y']), len(binary['x'])
x, y = np.meshgrid(binary['x'], binary['y'])

# Rasterio works with 1D arrays
lon, lat = transform(binary.crs, {'init': 'EPSG:4326'},x.flatten(), y.flatten()) # denne funker men er visst feil --> EPSG:25833
#Crs = rio.CRS.from_epsg(25833)
#lon, lat = transform(binary.crs, Crs ,x.flatten(), y.flatten())
lon = np.asarray(lon).reshape((ny, nx))
lat = np.asarray(lat).reshape((ny, nx))
binary.coords['lon'] = (('y', 'x'), lon)
binary.coords['lat'] = (('y', 'x'), lat)

binary_masked = binary.where(binary.values > -9999)

print(binary)
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 12,"font.family":"DejaVu Serif", "font.serif":["Computer Modern Roman"]})


plants = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
relevant_plants = [2,8]#[2,3,8,11]

## PLOT DISTRIBUTION OF RELEVANT PLANTS FROM SURFACEDATASET
""" 
for i in relevant_plants:
    fig, ax = plt.subplots(nrows=1)
    im = ax.pcolormesh(surface.lsmlon.values,surface.lsmlat.values,surface.PCT_NAT_PFT.values[i,:,:])
    #im = ax.pcolormesh(surface.lsmlon.values,surface.lsmlat.values,surface.LANDFRAC_PFT.values)
    ax.set_title(plant_acr[i])
    fig.colorbar(im,ax=ax)

"""

#from matplotlib.colors import LinearSegmentedColormap
#from matplotlib.patches import Patch

#colors = ["blue","red"]#["#440154FF", "#FDE725FF"]

# PLOT BINARY

plt.figure()
plt.title("Presence and absense of trees "+tif[-11:-7])
plt.rcParams.update({'font.size': 12,"font.family":"DejaVu Serif", "font.serif":["Computer Modern Roman"]})
plt.pcolormesh(binary.lon,binary.lat, binary_masked.values.squeeze(),cmap="viridis")

plt.show()
   

kart   =  np.zeros_like(surface.PCT_NAT_PFT.values[0])
nummer =  np.zeros_like(kart)
print(binary.data.shape)

surf_lat = surface.lsmlat.values
surf_lon = surface.lsmlon.values

lat_max = surf_lat.max()
lat_min = surf_lat.min()

lon_max = surf_lon.max()
lon_min = surf_lon.min()


lats=binary.lat.values.ravel()
lons=binary.lon.values.ravel()
data=binary_masked.data.ravel()

print(np.nanmax(data), np.nanmin(data))

def find_nearest_idx(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

for i in range(len(lats)):
    if lats[i]>lat_max or lats[i]<lat_min:
        continue
    if lons[i]>lon_max or lons[i]<lon_min:
        continue
    lat_idx = find_nearest_idx(surf_lat,lats[i])
    lon_idx = find_nearest_idx(surf_lon,lons[i])
    if not np.isnan(data[i]):
        kart[lat_idx,lon_idx] += data[i]
        nummer[lat_idx,lon_idx] += 1



mask = np.divide(kart,nummer)

multMask = mask.copy()
multMask[np.isnan(mask)] = 1 #multiplication mask

addMask = mask.copy()
addMask[np.isnan(mask)] = 0 # addition mask

dataMask = mask.copy()#for filtering in  results section
dataMask[~np.isnan(mask)] = 1
dataMask[np.isnan(mask)] = 0

np.save("surfaceMask.np",dataMask)
plt.show()
plt.pcolormesh(dataMask)
plt.title("Maskadi")
plt.show()

fig, ax = plt.subplots(nrows=1)
im = ax.pcolormesh(surface.lsmlon.values,surface.lsmlat.values,mask)
fig.colorbar(im,ax=ax,label="Tree fraction")
plt.title("Upscaled tree fraction")
#plt.pcolormesh(binary.lon,binary.lat, binary_masked.values.squeeze(),alpha=.5)
plt.show()


#removing trees over treeline: 
for i in relevant_plants:
    prøvegreie[i]=np.nanprod(np.asarray([prøvegreie[i],multMask]),axis=0)
    #print(np.nanprod(np.asarray([prøvegreie[i],mask]),axis=0).shape, "heisveis")


netForestMask = surface.PCT_NAT_PFT[2].values<80
plt.figure()
plt.pcolormesh(np.nanprod(np.asarray([netForestMask,addMask]),axis=0))
plt.show()

#Adding BDTs to areas specified by map
prøvegreie[8] += addMask*50



fig, ax = plt.subplots(nrows=1)
im = ax.pcolormesh(prøvegreie[8])#-surface.PCT_NAT_PFT[8])
fig.colorbar(im,ax=ax)

sums = np.sum(prøvegreie,axis=0)



surface.PCT_NAT_PFT.values=prøvegreie/np.sum(prøvegreie,axis=0) *100 

surface.to_netcdf("southNorway-pft8x50"+tif[-11:-4]+".nc")

fig, ax = plt.subplots(nrows=1)
im = ax.pcolormesh(surface.lsmlon.values,surface.lsmlat.values,surface.PCT_NAT_PFT[8])
plt.title("BDT coverage in surface dataset " + tif[-11:-7])
fig.colorbar(im,ax=ax,label="Percent of ground covered by BDT")
plt.show()

