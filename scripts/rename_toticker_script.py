from portfolio_analytics.utils import *
import os


tickers = ['SBER', 'TGKB', 'CNTL', 'KZOS', 'SNGS', 'RTKM', 'NKNC',
           'LSNG', 'PMSB', 'MTLR', 'TATN', 'KAZT', 'BANE', 'LNZL']
# NB!!! MGTS, KRKN are not api avalable, but prefs are OK
# TODO: download 2 last shares
pref_tickers = list(map(lambda string: string + 'P', tickers))
figis = get_figi(tickers, ru=True, api_avalable=True)

pref_figis = get_figi(pref_tickers, ru=True, api_avalable=True)

for i in range(len(tickers)):
    name0 = pref_figis[i]
    name1 = pref_tickers[i]
    path0 = f'../data/shares_data/companies_pref/{name0}.csv'
    path1 = f'../data/shares_data/companies_pref/{name1}.csv'
    os.rename(path0, path1)
