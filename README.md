# Covid19-Animation
This repo creates animation to visualize the spread of the virus.

# Requirments 
- Pyhton >= 3
- Numpy, Matplotlib
- Pandas
- Cartopy (instruction on instalaion is provided)

# Cartopy Installation and Custom Map Guide
Cartopy is a package that is used to visualize maps on geological data. To install it first make a conda enviroment and then install cartopy using ```conda install -c conda-forge cartopy```. 

To use custom background image, first use the following commands to find the path of the caratopy in the eniroment:
```python
import cartopy 
import os 
os.path.join(cartopy.__path__[0], "data", "raster", "natural_earth")
```
Next, from [NASA Blue Marble](https://visibleearth.nasa.gov/collection/1484/blue-marble) download both low (.jpg) and high resolution (.png) version of your favorite map to prjoect into the background and move then to ```natural_earth``` folder. Next, edit ```images.json``` file in the same folder and add something like the following the the json dict:
```python 
"BM": {
      "__comment__": "June, Blue Marble Next Generation w/ Topography and Bathymetry",
      "__source__": "https://neo.sci.gsfc.nasa.gov/view.php?datasetId=BlueMarbleNG-TB",
      "__projection__": "PlateCarree",
      "low": "BM.jpg",
      "high": "BM_highres.png"}
```
Now if you import the packages and use the following commands you will see earth map:
```python
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

fig = plt.figure(figsize=(19.2, 10.8))
ax = plt.axes(projection=ccrs.Mercator(central_longitude=0,  
                                       min_latitude=-65,
                                       max_latitude=70))
ax.background_img(name='BM', resolution='low')
ax.set_extent([-170, 179, -65, 70], crs=ccrs.PlateCarree())
```
![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")

