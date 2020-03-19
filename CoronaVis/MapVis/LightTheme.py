import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np
import pandas as pd


class BlueMarble(object):
    def __init__(self, df, ouput_name, max_val, resolution='low'):
        self.df = df
        self.ouput_name = ouput_name
        self.fig, self.ax = self.loadmap(resolution)
        self.max_val = max_val

    def loadmap(self,
                resolution):
        fig = plt.figure(figsize=(19.2, 10.8))
        ax = plt.axes(projection=ccrs.Mercator(central_longitude=0,\
                                       min_latitude=-65,
                                       max_latitude=70))
        ax.background_img(name='BM', resolution=resolution)
        ax.set_extent([-170, 179, -65, 70], crs=ccrs.PlateCarree())
        return fig, ax

    def generatemap(self,
                    date,
                    scale=1e4,
                    fontsize_date=36,
                    fontsize_labels=22,
                    show_death=False
                    ):
        df_date = self.df[self.df.Date == date]
        self.ax.scatter(df_date.Long.values, df_date.Lat.values,
                   s=scale * df_date.ConfNorm.values,
                   transform=ccrs.PlateCarree(),
                   color = "#ffee00",
                   alpha=0.6
                  )
        self.ax.scatter(df_date.Long.values, df_date.Lat.values,
                   s = scale * df_date.RecoverNorm.values,
                   transform=ccrs.PlateCarree(),
                   color = '#00a6f9',
                   alpha = 0.6
                  )
        if show_death:

            self.ax.scatter(df_date.Long.values, df_date.Lat.values,
                       s = scale * df_date.DeathNorm.values,
                       transform=ccrs.PlateCarree(),
                       color = '#ff5483',
                       alpha = 0.6
                      )

        t = pd.to_datetime(str(date))
        date = t.strftime('%b %d, %Y')

        date_x = 0
        date_y = -45

        self.ax.text(date_x, date_y,
                f"{date}",
                color='white',
                fontsize=fontsize_date,
                transform=ccrs.PlateCarree())


        ax1 = self.fig.add_axes([0.4, 0.04, 0.3, 0.15])
        ax1.patch.set_facecolor('None')
        
        colors = ["#ffee00", '#00a6f9']
        groups = ['Confirmed', 'Recovered']
        numbers = [df_date.Confirmed.sum(), df_date.Recovered.sum()]
        
        if show_death:
            colors.append('#ff5483')
            groups.append('Death')
            numbers.append(df_date.Deaths.sum())

        y_pos = np.arange(len(numbers))
        for i, v in enumerate(numbers):
            ax1.text(v, i, str(v), color=colors[i], fontweight='bold', fontsize=fontsize_labels, verticalalignment='center')

        ax1.barh(y_pos, numbers, color=colors)
        ax1.set_xlim(0, self.max_val)
        ax1.set_yticks(y_pos)
        ax1.set_yticklabels(groups, color="white", fontsize=fontsize_labels)
        ax1.set_xticks([])
        for side in ["left", "top", "bottom", "right"]:
            ax1.spines[side].set_visible(False)

        self.fig.tight_layout(pad=-0.5)
        self.fig.savefig(self.ouput_name, dpi=100, facecolor='black')
