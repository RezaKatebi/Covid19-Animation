# Covid19-Animation
This repo creates animation to visualize the spread of the virus.

# Installation
## Requirments 
We provide the [corviz.yml](https://github.com/RezaKatebi/Covid19-Animation/blob/master/corviz.yml) file that you can use to set up the environment: `conda env create -f corviz.yml` 

The software depends on
- Pyhton >= 3
- Numpy, Matplotlib
- Pandas
- Cartopy >= 0.17 (instruction on instalaion is provided)
- Basemap
- ffmpeg (for making .mp4 animation)

## Cartopy Installation and Custom Map Guide
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
Now if you import the packages and use the following commands (or run the script [test_custom_map.py](https://github.com/RezaKatebi/Covid19-Animation/blob/master/CoronaVis/test/test_custom_map.py)) you will see earth map:
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
![alt text](https://eoimages.gsfc.nasa.gov/images/imagerecords/73000/73726/world.topo.bathy.200406.3x5400x2700.jpg "Sample Map")

## Make Movie
We provide a Shell script [makemovie.bash](https://github.com/RezaKatebi/Covid19-Animation/blob/master/CoronaVis/makemovie.bash) that can be used to create the frames in .png format and to combine them into a .mp4 clip.
```Shell
#------------------------------------------------------
#   
#   Shell script to make a movie
#   (c) Katebi&Rezaie Co.
#   
#   Steps
#           1. make frames in png
#           2. use ffmpeg to combine them into mp4
#
#------------------------------------------------------

# Choose the theme: options are `dark` or `light`
theme=dark
echo "theme: "${theme}

# Run app.py
python app.py -m -t ${theme} 

# Run ffmpeg
dir=${PWD}/frames
output_name=Covid19_${theme}.mp4
echo "movie : "${output_name}

echo "change to "${dir}
cd ${dir}
ffmpeg -pattern_type glob -framerate 6 -i ${theme}_"**.png" -c:v h264 -r 10 -s 1920x1080 -pix_fmt yuv420p ${output_name}
```
