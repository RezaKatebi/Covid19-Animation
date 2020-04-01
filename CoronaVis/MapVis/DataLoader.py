import pandas as pd
import numpy as np
from functools import reduce


class DFLoader(object):
    def __init__(self, url_list):
        self.url_list = url_list

    def load(self):
        data_frames = []
        for key, value in self.url_list.items():
            df = pd.read_csv(value, error_bad_lines=False)
            df_long = df.melt(id_vars = ["Province/State", "Country/Region", "Lat", "Long"],\
                var_name="Date", value_name=key)
            df_long["Date"] = pd.to_datetime(df_long["Date"])
            data_frames.append(df_long)
        df_merged = reduce(lambda left,right: pd.merge(left, right, on=["Date","Province/State", "Country/Region", "Lat", "Long"],
                                            how='outer'), data_frames)
        min_val = df_merged["Confirmed"].min()
        max_val = df_merged["Confirmed"].max()
        df_merged["ConfNorm"] = (df_merged["Confirmed"]-min_val)/(max_val-min_val)
        df_merged["DeathNorm"] = (df_merged["Deaths"]-min_val)/(max_val-min_val)
        df_merged["RecoverNorm"] = (df_merged["Recovered"]-min_val)/(max_val-min_val)
        last_date = df_merged.Date.unique()[-1]
        max_last_day = df_merged.loc[df_merged["Date"]==last_date, "Confirmed"].sum()
        return df_merged, max_last_day



class DFLoaderNew:

    def __init__(self, url_list):
        self.df_global = pd.read_csv(url_list['world'])
        self.df_us = pd.read_csv(url_list['us'])
        self._fixUS() # fix US

    def load(self):
        df_all = pd.concat([self.df_us, self.df_global])

        #df_all.dropna(axis=1, inplace=True)
        df_long = df_all.melt(id_vars =["Province/State", "Country/Region", "Lat", "Long"],
                               var_name="Date", value_name='Confirmed')
        df_long["Date"] = pd.to_datetime(df_long["Date"])
        min_val = df_long["Confirmed"].min()
        max_val = df_long["Confirmed"].max()
        df_long["ConfNorm"] = (df_long["Confirmed"]-min_val)/(max_val-min_val)
        tot_confirmed = df_long.Confirmed[df_long.Date == df_long.Date.max()].sum(axis=0)
        return df_long, tot_confirmed

    def _fixUS(self):

        # ---  clean up US data
        self.df_us.drop(columns=['UID', 'iso2', 'iso3', 'code3',
                            'FIPS', 'Admin2', 'Combined_Key'], inplace=True)
        assert self.df_us['Country_Region'].unique()[0] == 'US'
        col_rename = {}
        for (a,b) in zip(['Province_State', 'Country_Region', 'Long_'],
                         ['Province/State', 'Country/Region', 'Long']):
            col_rename[a] = b
        self.df_us.rename(columns=col_rename, inplace=True)

        # --- fill NaN long Lat with NaNs
        states = np.unique(self.df_us['Province/State'])
        self.long_lat = {}

        long_glob = np.nanmean(self.df_us.Long)
        lat_glob  = np.nanmean(self.df_us.Lat)

        lat_nan = np.isnan(self.df_us.Lat)
        long_nan = np.isnan(self.df_us.Long)

        for state in states:
            mask_state = self.df_us['Province/State'] == state

            # --- compute the mean
            long_mean = np.nanmean(self.df_us.loc[mask_state, 'Long'])
            lat_mean = np.nanmean(self.df_us.loc[mask_state, 'Lat'])

            if np.isnan(long_mean): # if NaN, use global Mean
                #print(state)
                long_mean = long_glob*1

            if np.isnan(lat_mean):
                #print(state)
                lat_mean = lat_glob*1

            # --- fill
            mask_state_latnan = mask_state & lat_nan
            mask_state_longnan = mask_state & long_nan
            self.df_us.loc[mask_state_longnan, 'Long'] = long_mean
            self.df_us.loc[mask_state_latnan, 'Lat'] = lat_mean

            # --- backup
            self.long_lat[state] = {'Long':long_mean,
                                  'Lat':lat_mean}
