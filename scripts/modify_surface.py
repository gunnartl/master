import xarray as xr
import glob 


path = "/home/gunnartl/Documents/master/resultater/ctsm/singleSites/archive/**/lnd/hist/*.nc"

path = "testbakke_no_trees_or_shrubs.nc"

files = sorted(glob.glob(path,recursive=True))

relevant_plants = [2,3,8,11]

print(xr.open_dataset(files[0]))

#for file in files:
#	loaded = xr.open_dataset(file)
#	loaded.PCT_NAT_PFT[relevant_plants] = 0 # setting all trees and shrubs to zero
#	loaded.PCT_NAT_PFT[:] = loaded.PCT_NAT_PFT[:]/loaded.PCT_NAT_PFT.sum() * 100
#	loaded.to_netcdf(file[:-3]+"_no_trees_or_shrubs.nc")
