import xarray as xr 
import matplotlib.pyplot as plt
import numpy as np
import time

t = time.localtime()
start_time = time.strftime("%H:%M:%S", t)
print("Start time: ", start_time)

Sites = ["BESS1","GROT2","ROND3","KNUT3","DOVR0"]

len_avg = 12

avg1920NoTreeOrShrub = np.zeros(len_avg)
avg1920NoTree = np.zeros(len_avg)
avg1920 = np.zeros(len_avg)
avg2000NoTreeOrShrub = np.zeros(len_avg)
avg2000NoTree = np.zeros(len_avg)
avg2000 = np.zeros(len_avg)


xticks = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

jump = 1 # 2 and uncomment after #day to split into nightly and daily
variable = "H2OSNO"#"TSOI_10CM" #H2OSNO - snø i vann mm #EFLX_LH_TOT latent varme

tidsintervall = "month"

location = "~/Documents/master/resultater/ctsm/riktige_singlesites30/"

for Site in Sites:
	site1920 = xr.concat([xr.open_dataset(location+Site+"_SDU/lnd/hist/"+Site+"_SDU.clm2.h0.1900-01-01-00000.nc")[variable],
						  xr.open_dataset(location+Site+"_SDU/lnd/hist/"+Site+"_SDU.clm2.h0.1910-01-01-00000.nc")[variable],
						  xr.open_dataset(location+Site+"_SDU/lnd/hist/"+Site+"_SDU.clm2.h0.1920-01-01-00000.nc")[variable]],dim="time")

	site2000 = xr.concat([xr.open_dataset(location+Site+"_SDU/lnd/hist/"+Site+"_SDU.clm2.h0.1985-01-01-00000.nc")[variable],
						  xr.open_dataset(location+Site+"_SDU/lnd/hist/"+Site+"_SDU.clm2.h0.1995-01-01-00000.nc")[variable],
						  xr.open_dataset(location+Site+"_SDU/lnd/hist/"+Site+"_SDU.clm2.h0.2005-01-01-00000.nc")[variable]],dim="time")

	site1920NoTree = xr.concat([xr.open_dataset(location+Site+"_no_trees_SDU/lnd/hist/"+Site+"_no_trees_SDU.clm2.h0.1900-01-01-00000.nc")[variable],
								xr.open_dataset(location+Site+"_no_trees_SDU/lnd/hist/"+Site+"_no_trees_SDU.clm2.h0.1910-01-01-00000.nc")[variable],
								xr.open_dataset(location+Site+"_no_trees_SDU/lnd/hist/"+Site+"_no_trees_SDU.clm2.h0.1920-01-01-00000.nc")[variable]],dim="time")

	site2000NoTree = xr.concat([xr.open_dataset(location+Site+"_no_trees_SDU/lnd/hist/"+Site+"_no_trees_SDU.clm2.h0.1985-01-01-00000.nc")[variable],
								xr.open_dataset(location+Site+"_no_trees_SDU/lnd/hist/"+Site+"_no_trees_SDU.clm2.h0.1995-01-01-00000.nc")[variable],
								xr.open_dataset(location+Site+"_no_trees_SDU/lnd/hist/"+Site+"_no_trees_SDU.clm2.h0.2005-01-01-00000.nc")[variable]],dim="time")

	site1920NoTreeOrShrub = xr.concat([xr.open_dataset(location+Site+"_no_trees_or_shrubs_SDU/lnd/hist/"+Site+"_no_trees_or_shrubs_SDU.clm2.h0.1900-01-01-00000.nc")[variable],
									   xr.open_dataset(location+Site+"_no_trees_or_shrubs_SDU/lnd/hist/"+Site+"_no_trees_or_shrubs_SDU.clm2.h0.1910-01-01-00000.nc")[variable],
									   xr.open_dataset(location+Site+"_no_trees_or_shrubs_SDU/lnd/hist/"+Site+"_no_trees_or_shrubs_SDU.clm2.h0.1920-01-01-00000.nc")[variable]],dim="time")

	site2000NoTreeOrShrub = xr.concat([xr.open_dataset(location+Site+"_no_trees_or_shrubs_SDU/lnd/hist/"+Site+"_no_trees_or_shrubs_SDU.clm2.h0.1985-01-01-00000.nc")[variable],
									   xr.open_dataset(location+Site+"_no_trees_or_shrubs_SDU/lnd/hist/"+Site+"_no_trees_or_shrubs_SDU.clm2.h0.1995-01-01-00000.nc")[variable],
									   xr.open_dataset(location+Site+"_no_trees_or_shrubs_SDU/lnd/hist/"+Site+"_no_trees_or_shrubs_SDU.clm2.h0.2005-01-01-00000.nc")[variable]],dim="time")

	baseline = site1920NoTreeOrShrub[::jump].groupby("time."+tidsintervall).mean()
	treeChange = site1920NoTree[::jump].groupby("time."+tidsintervall).mean()
	treeAndShrubChange = site1920[::jump].groupby("time."+tidsintervall).mean()
	climateChange = site2000NoTreeOrShrub[::jump].groupby("time."+tidsintervall).mean()
	treeAndClimateChange = site2000NoTree[::jump].groupby("time."+tidsintervall).mean()
	treeShrubAndClimateChange = site2000[::jump].groupby("time."+tidsintervall).mean()

	

	#print(site1920[variable][::jump].groupby("time.month").mean().values.squeeze())

	plt.figure(figsize=(10,5))
	plt.rcParams.update({'font.size': 12})
	#night
	#plt.plot(baseline,label="1920")
	plt.plot(treeChange-baseline,label="Shrub growth")
	plt.plot(treeAndShrubChange-baseline,label="Tree and shrub growth")
	plt.plot(climateChange-baseline,label="Change in climate forcing")
	plt.plot(treeShrubAndClimateChange-baseline,label="Trees shrubs and climate forcing")
	#plt.plot(treeAndShrubChange+climateChange-2*baseline, label="sum")
	plt.ylabel("$\Delta$ Energy Flux [W/$m^2$]")
	#plt.ylabel("Fraction of snow covered area")
	#plt.ylabel("Change in snow cover [mm H$_2$0]")
	#plt.ylabel("Change in top 10cm soil temperature [C$^o$]")
	plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11],xticks,rotation=20)

	avg1920NoTreeOrShrub += baseline.values.squeeze()
	avg1920NoTree += treeChange.values.squeeze()
	avg1920 += treeAndShrubChange.values.squeeze()
	avg2000NoTreeOrShrub += climateChange.values.squeeze()
	avg2000 += treeShrubAndClimateChange.values.squeeze()
	#plt.show()
	#plt.figure()
	#day
	#plt.plot(bess1920[variable][1::2].groupby("time."+tidsintervall).mean()-bess1920NoTreeOrShrub[variable][1::2].groupby("time."+tidsintervall).mean(),"--",label="Change in vegetation",color="tab:blue")
	#plt.plot(bess2000NoTreeOrShrub[variable][1::2].groupby("time."+tidsintervall).mean()-bess1920NoTreeOrShrub[variable][1::2].groupby("time."+tidsintervall).mean(),"--",label="Change in climate forsing",color="tab:orange")
	#plt.plot(bess2000[variable][1::2].groupby("time."+tidsintervall).mean()-bess1920NoTreeOrShrub[variable][1::2].groupby("time."+tidsintervall).mean(),"--",label="Change in both",color="tab:green")
	#plt.plot(bess2000NoTreeOrShrub.EFLX_LH_TOT.groupby("time.dayofyear").mean()-273.15)
	#plt.plot(bess1920NoTreeOrShrub.EFLX_LH_TOT.groupby("time.dayofyear").mean()-273.15,label="Vegetation change")
	plt.legend()
	plt.title("Change in " + variable +  " from 1920 climate with no trees with different pertubations "+Site)
	#plt.title("Fraction of snow covered area"+Site)
	plt.savefig("../figurer/monthlyChange"+variable+"-"+Site+".pdf",format="pdf",dpi=300)

plt.figure(figsize=(10,5))
plt.rcParams.update({'font.size': 12})
plt.plot((avg1920NoTree-avg1920NoTreeOrShrub)/len(Sites),label="Shrub growth")
plt.plot((avg1920 - avg1920NoTreeOrShrub )/len(Sites),label="Tree and shrub growth")
plt.plot((avg2000NoTreeOrShrub - avg1920NoTreeOrShrub)/len(Sites),label="Change in climate forcing")
plt.plot((avg2000 - avg1920NoTreeOrShrub)/len(Sites),label="Climate forcing, trees and shrubs")
plt.legend()
plt.ylabel("Change in snow cover [mm H$_2$0]")
plt.ylabel("Change in top 10cm soil temperature [C$^o$]")
plt.ylabel("$\Delta$ Energy Flux [W/$m^2$]")
#plt.ylabel("Fraction of snow covered area")
#plt.ylabel("Change in snow cover [mm H$_2$0]")
plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11],xticks,rotation=20)
plt.title("Change in " + variable +  " from 1900-29 climate with no trees with different pertubations average")
#plt.title("Fraction of snow covered area average")
plt.savefig("../figurer/monthlyChange"+variable+"-"+"average.pdf",format="pdf",dpi=300)

t = time.localtime()
end_time = time.strftime("%H:%M:%S", t)
print("End time: ", end_time)

plt.show()

### BARPLOTS showing change in energybalance
#EFLX_LH_TOT - total latent energiflux
#TSA - 2m temp
#FSNO - brøkdel som er snødekt
#SNOW_PERSITENACE -  
#FSA - absoberd solar radiation
#FSR - reflected solar radiation
#FIRA - net long wave 
# FSH_V sensible heat fom veg
# FCEV - canopy evaporation
# DHSDT_CANOPY caopy heat storage
# TSOI_10CM - soil temp top 10 cm