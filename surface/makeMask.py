import xarray as xr
import numpy as np

DBT2020 = xr.open_dataset("surfdata_southNorway_pft8x50_2020_TL.nc").PCT_NAT_PFT[8]

DBT1920 = xr.open_dataset("surfdata_southNorway_pft8x50_1920_TL.nc").PCT_NAT_PFT[8]

change = DBT2020-DBT1920
changemask = change > 5
import matplotlib.pyplot as plt
changemask.plot()
plt.show()

print(changemask.values)

np.save("changemask5",changemask.values)
