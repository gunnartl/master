import xarray as xr 
import matplotlib.pyplot as plt
import numpy as np


sites = ["GROT2"]#["BESS1","GROT2","ROND3","KNUT3","DOVR0"]
variables = ["FGR","FIRA","FSH","EFLX_LH_TOT","FSR","FSA"]
names = ["G","NLW","SH","LH","SR$_{R}$","SR$_{A}$"]


change_TS = np.zeros((len(variables),4))
day_change_TS = np.zeros((len(variables),4))

change_S = np.zeros((len(variables),4))
day_change_S = np.zeros((len(variables),4))

location = "~/Documents/master/resultater/ctsm/singleSites30/"

for site in sites:
	#site1920 = xr.open_dataset("~/Documents/master/resultater/ctsm/singlesites/"+site+"_SDU/lnd/hist/"+site+"_SDU.clm2.h0.1920-01-01-00000.nc")[variables]
	#site1920NoTreeOrShrub = xr.open_dataset("~/Documents/master/resultater/ctsm/singlesites/"+site+"_no_trees_or_shrubs_SDU/lnd/hist/"+site+"_no_trees_or_shrubs_SDU.clm2.h0.1920-01-01-00000.nc")[variables]
	#site1920NoTree = xr.open_dataset("~/Documents/master/resultater/ctsm/singlesites/"+site+"_no_trees_SDU/lnd/hist/"+site+"_no_trees_SDU.clm2.h0.1920-01-01-00000.nc")[variables]

	site1920 = xr.concat([xr.open_dataset(location+site+"_SDU/lnd/hist/"+site+"_SDU.clm2.h0.1900-01-01-00000.nc"),
						  xr.open_dataset(location+site+"_SDU/lnd/hist/"+site+"_SDU.clm2.h0.1910-01-01-00000.nc"),
						  xr.open_dataset(location+site+"_SDU/lnd/hist/"+site+"_SDU.clm2.h0.1920-01-01-00000.nc")],dim="time")


	site1920NoTree = xr.concat([xr.open_dataset(location+site+"_no_trees_SDU/lnd/hist/"+site+"_no_trees_SDU.clm2.h0.1900-01-01-00000.nc"),
								xr.open_dataset(location+site+"_no_trees_SDU/lnd/hist/"+site+"_no_trees_SDU.clm2.h0.1910-01-01-00000.nc"),
								xr.open_dataset(location+site+"_no_trees_SDU/lnd/hist/"+site+"_no_trees_SDU.clm2.h0.1920-01-01-00000.nc")],dim="time")

	site1920NoTreeOrShrub = xr.concat([xr.open_dataset(location+site+"_no_trees_or_shrubs_SDU/lnd/hist/"+site+"_no_trees_or_shrubs_SDU.clm2.h0.1900-01-01-00000.nc"),
									   xr.open_dataset(location+site+"_no_trees_or_shrubs_SDU/lnd/hist/"+site+"_no_trees_or_shrubs_SDU.clm2.h0.1910-01-01-00000.nc"),
									   xr.open_dataset(location+site+"_no_trees_or_shrubs_SDU/lnd/hist/"+site+"_no_trees_or_shrubs_SDU.clm2.h0.1920-01-01-00000.nc")],dim="time")


	for i, variable in enumerate(variables):
		baseline = site1920NoTreeOrShrub[variable].resample(time="QS-DEC").mean().groupby("time.month").mean().values.squeeze()
		change_TS[i] += site1920[variable].resample(time="QS-DEC").mean().groupby("time.month").mean().values.squeeze()-baseline
		change_S[i] += site1920NoTree[variable].resample(time="QS-DEC").mean().groupby("time.month").mean().values.squeeze()-baseline
		
		#day_baseline = site1920NoTreeOrShrub[variable][1::2].resample(time="QS-DEC").mean().groupby("time.month").mean().values.squeeze()
		#day_change_TS[i] += site1920[variable][1::2].resample(time="QS-DEC").mean().groupby("time.month").mean().values.squeeze()-day_baseline
		#day_change_S[i] += site1920NoTree[variable][1::2].resample(time="QS-DEC").mean().groupby("time.month").mean().values.squeeze()-day_baseline
		#print(site1920[variable][1::2].resample(time="QS-DEC").mean().groupby("time.month").mean()["month"])


day_change_TS /= len(sites)
change_TS /= len(sites)

day_change_S /= len(sites)
change_S /= len(sites)

y_pos = np.arange(len(variables))*2 # placement for barplots

fig, ax = plt.subplots(1,4,figsize=(17,6.3))

seasons = ["Spring", "Summer", "Autumn","Winter"]
plt.rcParams.update({'font.size': 12})
for i in range(4):
	ax[i].barh(y_pos+.8, change_S[:,i], align='center',label="Shrubs")
	ax[i].barh(y_pos, change_TS[:,i], align='center',label="Trees and shrubs")
	ax[i].set_yticks(y_pos+.4)
	ax[i].set_yticklabels(names if i == 0 else [],fontsize=12)
	#ax[i].set_xlabel('Energy flux')
	ax[i].set_title(seasons[i])
	ax[i].grid("on")
	#ax[i].set_xlim([-7.5,7.5])
	#ax[i].set_xticks([-5,-2.5,0,2.5,5])
	#ax[i].set_xticklabels([-5,-2.5,0,2.5,5],fontsize=12)
	#ax[i].set_xlim([-20,20])
	#ax[i].set_xticks([-15,-7.5,0,7.5,15])
	#ax[i].set_xticklabels([-15,-7.5,0,7.5,15],fontsize=12)
	ax[i].set_xlim([-6,6])
	ax[i].set_xticks([-4,-2,0,2,4])
	ax[i].set_xticklabels([-4,-2,0,2,4],fontsize=12)

	#ax[1,i].barh(y_pos, change_TS[:,i], align='center')
	#ax[1,i].barh(y_pos+.8, change_S[:,i], align='center')
	#ax[1,i].set_yticks(y_pos+.4)
	#ax[1,i].set_yticklabels(variables if i == 0 else [])
	#ax[1,i].set_xlabel('$\Delta$ Energy flux [W/m$^2$]')
	#ax[1,i].grid("on")
	#ax[1,i].set_xlim([-7.5,7.5])
ax[3].legend(bbox_to_anchor=(0.1,0), loc="lower left", 
                bbox_transform=fig.transFigure, ncol=2)
fig.text(0.5, 0.03, '$\Delta$ Energy flux [W/m$^2$]', ha='center',fontsize = 14)
fig.suptitle("Energy balance response to new vegetation at Grotli",fontsize=20)
fig.savefig("../figurer/energyBalanceBarplot-"+site[:-1]+"1920.pdf",format="pdf",dpi=300)
plt.show()