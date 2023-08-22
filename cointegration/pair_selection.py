import matplotlib.pyplot as plt
from cointegration.funcs import *
import pandas as pd
import numpy as np
from keys import pref_tickers as tickers
from tqdm import tqdm
import datetime as dt
from statsmodels.tsa.stattools import adfuller as adf


# columns = ['name', 'a', 'b', 't', 'stat', 'ds_ratio']
# stats = [[] for el in columns]
# stats = dict(zip(columns, stats))
# print(stats)
for ticker in tqdm(tickers):
    print('=======================' + ticker + '=======================')
    share_df = pd.read_csv(f'../data/shares_data/companies/{ticker}.csv')  # downloading
    pref_df = pd.read_csv(f'../data/shares_data/companies_pref/{ticker}P.csv')

    pair_df = match_ts(share_df, pref_df, join_with='close')  # matching and joining
    T = (dt.datetime.strptime(pair_df['time'].iloc[0][:10], '%Y-%m-%d') - dt.datetime.strptime(pair_df['time'].iloc[-1][:10],'%Y-%m-%d')) / dt.timedelta(days=365)
    pair_df['T'] = np.linspace(0, T, pair_df.shape[0])  # adding time in years
    print(f'time period = {T}')

    cut = int(2 * pair_df.shape[0] / 3)  # making sample
    pair_df = pair_df.iloc[:cut]

    # regression with trend and stats
    A = np.array((np.ones_like(pair_df['T'].values), pair_df['T'].values, pair_df['ts2'].values))
    y = pair_df['ts1'].values

    res = np.linalg.lstsq(A.T, y, rcond=None)
    print(f'Regression coefs: {res[0]}')
    a, t, b = res[0]
    pair_df['spread'] = pair_df['ts1'] - b * pair_df['ts2'] - a  # error with trend
    pair_df['err'] = pair_df['ts1'] - b * pair_df['ts2'] - t * pair_df['T'] - a  # residual series
    ds_ratio = t / pair_df.err.std()
    # df_test = adf(pair_df.err.values[::3])
    # stats_list = [ticker, a, b, t, df_test, ds_ratio]
    # for i in range(len(stats_list)):
    #     stats[columns[i]].append(stats_list[i])

    print(f'Drift / Sigma ~ {ds_ratio*100} %')
    # print(f' DF Test statistic = {df_test}')

    plt.style.use('dark_background')
    fig, ax = plt.subplots(3, 1, figsize=(18, 15), gridspec_kw={'height_ratios': [3, 2, 2]})
    fig.suptitle(f'{ticker}', fontsize=16)
    ax[0].plot(pair_df['T'].values, pair_df['ts1'].values, label='share')
    ax[0].plot(pair_df['T'].values, pair_df['ts2'].values, label='pref')
    ax[0].legend()
    ax[1].plot(pair_df['T'].values, pair_df['spread'].values,
               label='spread')
    ax[1].plot(pair_df['T'].values, t*pair_df['T'].values, label='trend')
    ax[1].legend()
    ax[2].plot(pair_df['T'].values, pair_df['err'], label=f'a = {a}, t = {t}, b = {b}')
    ax[2].legend()
    plt.show()

# stats_df = pd.DataFrame.from_dict(stats)
# stats_df.to_csv('../cointegration/data/sample_stats.csv')
