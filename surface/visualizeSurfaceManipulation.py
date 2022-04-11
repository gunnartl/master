import xarray as xr
import numpy as np
from rasterio.warp import transform
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Patch
import rasterio as rio





def openTif(name):
    "Opens geotif file with norting easting axes returns dataarray with lat lon axes "
    binary = xr.open_rasterio(name)


    # Compute the lon/lat coordinates with rasterio.warp.transform
    ny, nx = len(binary['y']), len(binary['x'])
    x, y = np.meshgrid(binary['x'], binary['y'])

    # Rasterio works with 1D arrays
    lon, lat = transform(binary.crs, {'init': 'EPSG:4326'},x.flatten(), y.flatten()) # denne funker men er visst feil --> EPSG:25833
    #Crs = rio.CRS.from_epsg(25833)
    #lon, lat = transform(highres2020.crs, Crs ,x.flatten(), y.flatten())
    lon = np.asarray(lon).reshape((ny, nx))
    lat = np.asarray(lat).reshape((ny, nx))
    binary.coords['lon'] = (('y', 'x'), lon)
    binary.coords['lat'] = (('y', 'x'), lat)

    highres2020 = binary.where(binary.values > -9999)
    return(highres2020)


def twoMapPlotter(x0,y0,val0,x1,y1,val1,suptitle,subtitle0,subtitle1,filename,skip=1,binary=False,cbarlabel=False,minmax=False):
    
    plt.rcParams.update({'font.size': 20,"font.family":"DejaVu Serif", "font.serif":["Computer Modern Roman"]})
    fig, ax = plt.subplots(nrows=1, ncols=2,figsize=(17,7.6))
    ax[0].set_title(subtitle0)
    ax[1].set_title(subtitle1)
    ax[1].set_yticklabels([])

    if minmax != False:
        im=ax[0].pcolormesh(x0,y0, val0,vmin=minmax[0],vmax=minmax[1],cmap="viridis")
        ax[1].pcolormesh(x1,y1, val1,vmin=minmax[0],vmax=minmax[1],cmap="viridis")

    elif skip==1:
        im=ax[0].pcolormesh(x0,y0, val0,cmap="viridis")
        ax[1].pcolormesh(x1,y1, val1,cmap="viridis")
    else:
        ax[0].pcolormesh(x0[::skip,::skip],y0[::skip,::skip], val0[::skip,::skip],cmap="viridis")
        ax[1].pcolormesh(x1[::skip,::skip],y1[::skip,::skip], val1[::skip,::skip],cmap="viridis")
    if binary:
        colors =  ["#440154FF", "#FDE725FF"] # colors of the ends of viridis cmap
        legend_elements = [Patch(facecolor=color, edgecolor='w') for color in colors]
        fig.legend(handles=legend_elements,
                  labels=["Absence","Presence"],
                  bbox_to_anchor=(0.1185,0), 
                  loc="lower left", 
                  bbox_transform=fig.transFigure, 
                  ncol=2,
                  fontsize=16)
    else:
        fig.subplots_adjust(right=0.9)
        cbar_ax = fig.add_axes([0.92, 0.15, 0.025, 0.7])
        fig.colorbar(im, cax=cbar_ax,label=cbarlabel)

    fig.suptitle(suptitle,fontsize=22)
    fig.text(0.5, 0.03, 'Longitude', ha='center')
    fig.text(0.06,.45, 'Latitude', ha='center',rotation='vertical')
    #fig.tight_layout()
    plt.subplots_adjust(wspace=0.05)
    plt.savefig(filename,format="pdf",dpi=300)
    plt.show()


#plot original binary maps
#twoMapPlotter(highres1920.lon,highres1920.lat,highres1920.values.squeeze(),
#              highres2020.lon,highres2020.lat,highres2020.values.squeeze(),
#              "Modelled presence and absence of trees","1920","2020","../figurer/AdamsResultat.pdf",skip=5,binary=True)

#plot upscaled TreeFraction
initialSurface = xr.open_dataset("surfdata_fenno_5x5km_simyr2000_southNorway_c181116.nc")
treeFraction2020 = np.load("treefraction2020_TL.npy")
treeFraction1920 = np.load("treefraction1920_TL.npy")


print(initialSurface.lsmlon.values.shape)
twoMapPlotter(initialSurface.lsmlon,initialSurface.lsmlat,treeFraction1920,
              initialSurface.lsmlon,initialSurface.lsmlat,treeFraction2020,
              "Upscaled fractional presence of trees","1920","2020","../figurer/treeFractions.pdf",cbarlabel="Fraction of gridcell with tree precence")

#plot initial values of pft8 - Boreal broadleaf decidous trees
plottemaske = np.load("surfaceMask.np.npy")
plt.figure(figsize=(8,6))
plt.rcParams.update({'font.size': 14,"font.family":"DejaVu Serif", "font.serif":["Computer Modern Roman"]})
plt.pcolormesh(initialSurface.lsmlon,initialSurface.lsmlat,(initialSurface.PCT_NAT_PFT[8]),vmin=0,vmax=100,cmap="viridis")
plt.title("Initial distribution of \nboreal broadleaf decidous trees")
plt.ylabel("Latitude")
plt.xlabel("Longitude")
plt.colorbar(label="% of ground covered by Boreal BDT")
plt.savefig("../figurer/InitialBBDTdist.pdf",format="pdf",dpi=300)
plt.show()



# prosess plot: 
surface1920 = xr.open_dataset("southNorway-pft8x501920_TL.nc")
surface2020 = xr.open_dataset("southNorway-pft8x502020_TL.nc")

removed = np.nanprod([initialSurface.PCT_NAT_PFT[8],treeFraction1920],axis=0)
added = np.nansum([removed,treeFraction1920*50],axis=0)
fig, ax = plt.subplots(nrows=2, ncols=2,figsize=(10,7))
plt.rcParams.update({'font.size': 18,"font.family":"DejaVu Serif", "font.serif":["Computer Modern Roman"]})
im = ax[0,0].pcolormesh(initialSurface.lsmlon,initialSurface.lsmlat,(initialSurface.PCT_NAT_PFT[8]),vmin=0,vmax=100,cmap="viridis")
ax[0,0].set_xticklabels([])
ax[0,0].set_title("Initial distribution",fontsize=16)

ax[0,1].pcolormesh(initialSurface.lsmlon,initialSurface.lsmlat,removed,vmin=0,vmax=100,cmap="viridis")
ax[0,1].set_yticklabels([])
ax[0,1].set_xticklabels([])
ax[0,1].set_title("Removal and thinning",fontsize=16)

ax[1,0].pcolormesh(initialSurface.lsmlon,initialSurface.lsmlat,added,vmin=0,vmax=100,cmap="viridis")
ax[1,0].set_title("Adding",fontsize=16)


ax[1,1].pcolormesh(initialSurface.lsmlon,initialSurface.lsmlat,surface1920.PCT_NAT_PFT[8],vmin=0,vmax=100,cmap="viridis")
ax[1,1].set_yticklabels([])
ax[1,1].set_title("Normalising",fontsize=16)

fig.suptitle("Process for creating the surface datasets",fontsize=22)
fig.text(0.5, 0.03, 'Longitude', ha='center')
fig.text(0.06,.45, 'Latitude', ha='center',rotation='vertical')
fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.82, 0.15, 0.025, 0.7])
fig.colorbar(im, cax=cbar_ax,label="% of ground covered by boreal BDT")
plt.subplots_adjust(wspace=0.05)
plt.savefig("../figurer/surfaceProcess.pdf",format="pdf",dpi=300)
plt.show()

# Plot finished result: 

print(initialSurface.lsmlon.values.shape)
twoMapPlotter(initialSurface.lsmlon,initialSurface.lsmlat,surface1920.PCT_NAT_PFT[8],
              initialSurface.lsmlon,initialSurface.lsmlat,surface2020.PCT_NAT_PFT[8],
              "Final distribution of boreal BDT","1920","2020","../figurer/finalBDTDistribution.pdf",cbarlabel="% of ground covered by boreal BDT",minmax=[0,100])