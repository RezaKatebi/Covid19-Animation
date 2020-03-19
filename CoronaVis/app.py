import MapVis
import argparse
import pandas as pd
import os
from tqdm import tqdm


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-mm", "--movie",
                    default=False,
                    action="store_true",
                    help="Use -m to activate!")
    ap.add_argument("-d", "--date",
                    default='2020-03-17',
                    type=str,
                    help="Enter date in format of Year-Month-Day!")
    ap.add_argument("-r", "--res",
                    default='low',
                    type=str,
                    help="Enter the resolution for your Image or Movie!")
    args = ap.parse_args()
    general_path = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/"
    url_list = {
        "Confirmed": f"{general_path}time_series_19-covid-Confirmed.csv",
        "Deaths": f"{general_path}time_series_19-covid-Deaths.csv",
        "Recovered": f"{general_path}time_series_19-covid-Recovered.csv"
    }

    DataLoader = MapVis.DFLoader(url_list)
    df_merged, max_last_day = DataLoader.load()

    if not args.movie:
        BM = MapVis.BlueMarble(df=df_merged, ouput_name=f"{args.date}.png",
                                max_val= max_last_day, resolution=args.res)
        BM.generatemap(args.date)
    else:
        alldates = df_merged.Date.unique()
        alldates = pd.to_datetime(alldates)
        # timestring = t.strftime('%Y-%m-%d')
        alldates = alldates.strftime('%Y-%m-%d')

        path = "frames"
        if not os.path.exists(path):
            os.makedirs(path)

        for i, date in tqdm(enumerate(alldates)):
            BM = MapVis.BlueMarble(df=df_merged, ouput_name=f"{path}/{i}_{date}.png",
                                    max_val= max_last_day, resolution=args.res)
            BM.generatemap(date)


if __name__ == "__main__":
    main()