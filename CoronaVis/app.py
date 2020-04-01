import MapVis
import argparse
import pandas as pd
import os
from tqdm import tqdm


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--movie",
                    default=False,
                    action="store_true",
                    help="Use -m to activate!")
    ap.add_argument("-d", "--date",
                    default='2020-03-18',
                    type=str,
                    help="Enter date in format of Year-Month-Day!")
    ap.add_argument("-r", "--res",
                    default='low',
                    type=str,
                    help="Enter the resolution for your Image or Movie!")
    ap.add_argument("-t", "--theme",
                    default='light',
                    help="Enter the theme Light or Dark")
    args = ap.parse_args()
    general_path = ("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/"
                   "master/csse_covid_19_data/csse_covid_19_time_series/")
    #url_list = {
    #    "Confirmed": f"{general_path}time_series_19-covid-Confirmed.csv",
    #    "Deaths": f"{general_path}time_series_19-covid-Deaths.csv",
    #    "Recovered": f"{general_path}time_series_19-covid-Recovered.csv"
    #}
    print('new data has a different format. It has confirmed cases only!')
    url_list = {'world':f'{general_path}time_series_covid19_confirmed_global.csv',
                'us':f'{general_path}time_series_covid19_confirmed_US.csv'}


    DataLoader = MapVis.DFLoaderNew(url_list) # MR: Mar 31, new data
    df_merged, max_last_day = DataLoader.load()

    if args.theme == 'light':
        # msg = 'new data does not have the number recovered cases!'
        # msg += 'https://github.com/CSSEGISandData/COVID-19/issues/1250'
        # raise RuntimeError(msg)
        MarbleMaker = MapVis.BlueMarble

    elif args.theme == 'dark':
        MarbleMaker = MapVis.DarkMarble

    else:
        raise RuntimeError(f'{args.theme} must be light or dark')

    if not args.movie:
        BM = MarbleMaker(df=df_merged, ouput_name=f"{args.theme}_{args.date}.png",
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

        for date in tqdm(alldates):
            BM = MarbleMaker(df=df_merged, ouput_name=f"{path}/{args.theme}_{date}.png",
                             max_val= max_last_day, resolution=args.res)
            BM.generatemap(date)


if __name__ == "__main__":
    main()
