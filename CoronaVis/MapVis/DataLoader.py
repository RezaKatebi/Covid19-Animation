import pandas as pd
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
