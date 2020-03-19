# Covid19-Animation
This repo creates animation to visualize the spread of the virus.

# Requirments 
- Pyhton >= 3
- Numpy, Matplotlib
- Pandas
- Cartopy (instruction on instalaion is provided)

# Cartopy Installation and Custom Map Guide
Cartopy is a package that is used to visualize maps on geological data. To install it first make a conda enviroment and then install cartopy ```conda install -c conda-forge cartopy```. 

To use custom background image, first use the following commands to find the path of the caratopy in the eniroment:
```
import cartopy 
mport os 
os.path.join(cartopy.__path__[0], "data", "raster", "natural_earth")

```

