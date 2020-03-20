'''
    DarkMarbel
    
    developed by Mehdi Rezaie and Reza Katebi Katebi&Rezaie Co.
    based on https://cosmiccoding.com.au/tutorials/des_instituions
    by Samuel Hinton
'''


import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from mpl_toolkits.basemap import Basemap
from matplotlib.colors import LinearSegmentedColormap as LSC

class DarkMarble(object):
 
    def __init__(self, df, ouput_name, max_val, resolution='low'):
        # MR: different resolution is not implemented yet
        self.df = df
        self.ouput_name = ouput_name
        self.max_val = max_val
        
    def generatemap(self,
                    date,
                    scale=1e4,
                    fontsize_date=36,
                    fontsize_labels=22,
                    show_death=False,
                    addglow=True, 
                    **kwargs
                    ):
        
        df_date = self.df[self.df.Date == date]

        m = self.get_base_frame()
        m.scatter(df_date.Long, df_date.Lat, latlon=True, 
                  c='#d7ff1f', s=0.03*df_date.Confirmed, zorder=1,
                  alpha=0.3)
        
        
        if addglow:
            
            nmesh = 500
            x0, y0 = m(-170, -80)
            x1, y1 = m(190, 90)
            xs, ys = np.linspace(x0, x1, nmesh), np.linspace(y0, y1, nmesh)
            X, Y = np.meshgrid(xs, ys)
            zs = []
            scale = 1.2
            
            
            c = '#d7ff1f'
            cmap = LSC.from_list("fade", [c + "00", c,"#FFFFFF"], N=1000)
            vmax = min(2, 0.7 * df_date.shape[0]**0.7)

            z = np.zeros(X.shape)
            for row in df_date.itertuples(index=False):
                x, y = m(row.Long, row.Lat)
                dist = ((x - X)**2 + (y - Y)**2)**0.25
                z += (row.Confirmed/8.0e3)*np.exp(-dist * scale)

            m.imshow(z, origin="lower", extent=[x0,x1,y0,y1], 
                     cmap=cmap, vmax=vmax, zorder=2, rasterized=True)        
            
            m.scatter(df_date.Long, df_date.Lat, latlon=True, c="#FFFFFF", 
                     alpha=0.8, s=1.0e-4*df_date.Confirmed, zorder=3)

            
        plt.title("Covid-19 around the world", fontsize=14, 
                  color="#EEEEEE", fontname="serif")
        
        msg = '(c) Katebi&Rezaie\ngithub.com/RezaKatebi/Covid19-Animation'
        plt.text(*m(-165, -62), msg, color='yellow', fontsize=5)        


        t = pd.to_datetime(str(date))
        date = t.strftime('%b %d, %Y')

        date_x = 0
        date_y = -45
        plt.text(*m(date_x, date_y),
                f"{date}",
                color='white',
                fontsize=15)

        fig = plt.gcf()
        fig.patch.set_facecolor("#000000")

        # Add bar plot
        ax1 = plt.axes([0.45, 0.175, 0.15, 0.025])
        ax1.patch.set_facecolor('None')

        lcolors = ['white'] #'#4b34e2', '#a6a3ba']
        groups = ['Confirmed']#, 'Recovered', 'Death']
        numbers = [df_date.Confirmed.sum()] #,40, 20]
        y_pos = np.arange(len(numbers))

        for i, v in enumerate(numbers):
            ax1.text(v+3, i, str(v), color=lcolors[i], 
                     fontweight='bold', 
                     verticalalignment='center',
                     fontsize=10)

        ##ax1.set_title(f'{date}', fontsize=20, color='w')
        ax1.barh(y_pos, numbers, color=lcolors)
        ax1.set_yticks(y_pos)
        ax1.set_xlim(0, self.max_val)
        ax1.set_yticklabels(groups, color='white', fontsize=10)
        ax1.set_xticks([])
        for side in ['left', 'top', 'bottom', 'right']:
            ax1.spines[side].set_visible(False)

        #fig.tight_layout(pad=-0.5)
        fig.savefig(self.ouput_name, dpi=100, facecolor='black', bbox_inches='tight')
        return None


    
    def get_base_frame(self):
        
        # Lets define some colors
        bg_color = "#000000"
        coast_color = "#333333"
        country_color = "#222222"
        
        plt.figure(figsize=(12, 6))

        m = Basemap(projection='cyl', llcrnrlat=-80,urcrnrlat=90, 
                    llcrnrlon=-170, urcrnrlon=190, area_thresh=10000.)
        m.fillcontinents(color=bg_color, lake_color=bg_color, zorder=-2)
        m.drawcoastlines(color=coast_color, linewidth=1.0, zorder=-1)
        m.drawcountries(color=country_color, linewidth=1.0, zorder=-1)
        m.drawmapboundary(fill_color=bg_color, zorder=-2)
        
        return m        
