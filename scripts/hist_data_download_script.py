import creds
from portfolio_analytics.utils import *
from tqdm import tqdm
import time
from datetime import datetime, timedelta
from tinkoff.invest import CandleInterval

tok = creds.token_ro_all

tickers = ['SBER', 'TGKB', 'CNTL', 'KZOS', 'SNGS', 'RTKM', 'NKNC', 'LSNG', 'PMSB', 'MTLR', 'TATN', 'KAZT', 'BANE', 'LNZL']
# NB!!! MGTS, KRKN are not api avalable, but prefs are OK
# TODO: download 2 last shares
pref_tickers = list(map(lambda string: string + 'P', tickers))


figis = get_figi(tickers, ru=True, api_avalable=True)
print(figis, )
pref_figis = get_figi(pref_tickers, ru=True, api_avalable=True)
# print(figis)

end = datetime(year=2023, month=8, day=10)
for name in (figis[-2], figis[-1]):
    df_list = []
    for i in tqdm(range(1825)):
        df = get_candles(acc_token=tok,
                         figi=name,
                         from_=end - timedelta(days=1 + i),
                         to=end - timedelta(days=i),
                         interval=CandleInterval.CANDLE_INTERVAL_1_MIN)
        df_list.append(df)
        time.sleep(0.2)

    res = pd.concat(df_list, axis=0, ignore_index=True)
    res.to_csv(f'../data/shares_data/companies_pref/{name}.csv')
