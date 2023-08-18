import numpy as np
from keys import pref_tickers as tickers
from tqdm import tqdm
from cointegration.funcs import *


for ticker in tqdm(tickers):
    print(f'{ticker}')
    share_df = pd.read_csv(f'../data/shares_data/companies/{ticker}.csv')  # downloading
    pref_df = pd.read_csv(f'../data/shares_data/companies_pref/{ticker}P.csv')

    share_df, pref_df = match_ts(share_df, pref_df)  # matching

    pref_df['T'] = np.linspace(0, 5, pref_df.shape[0])  # adding time in years
    share_df['T'] = np.linspace(0, 5, pref_df.shape[0])

    cut = int(2 * share_df.shape[0] / 3)  # making sample and validation
    share_df.iloc[cut:].to_csv(f'../cointegration/data/sample/{ticker}.csv')
    pref_df.iloc[cut:].to_csv(f'../cointegration/data/sample/{ticker}P.csv')

    share_df.iloc[:cut].to_csv(f'../cointegration/data/validation/{ticker}.csv')
    pref_df.iloc[:cut].to_csv(f'../cointegration/data/validation/{ticker}P.csv')


