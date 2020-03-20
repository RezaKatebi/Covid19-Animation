'''
    Test that you have correctly added the custom maps

    (c) Katebi Rezaie Co.
    March 19, 2020
'''

import matplotlib.pyplot as plt
import cartopy.crs as ccrs

fig = plt.figure(figsize=(19.2, 10.8))
ax = plt.axes(projection=ccrs.Mercator(central_longitude=0,  
                                       min_latitude=-65,
                                      max_latitude=70))
ax.background_img(name='BM', resolution='low')
ax.set_extent([-170, 179, -65, 70], crs=ccrs.PlateCarree())
plt.show()

