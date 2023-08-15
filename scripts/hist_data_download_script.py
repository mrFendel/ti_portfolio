import creds
from utils import *
from tqdm import tqdm
import time
from datetime import datetime, timedelta
from tinkoff.invest import CandleInterval
from keys import pref_tickers as tickers

tok = creds.token_ro_all
pref_tickers = list(map(lambda string: string + 'P', tickers))
# TODO: refactor to function in utils

figis = get_figi(tickers, ru=True, api_avalable=True)
pref_figis = get_figi(pref_tickers, ru=True, api_avalable=True)


end = datetime(year=2023, month=8, day=10)
for num in range(len(figis)):
    df_list = []
    for i in tqdm(range(1825)):
        df = get_candles(acc_token=tok,
                         figi=figis[num],
                         from_=end - timedelta(days=1 + i),
                         to=end - timedelta(days=i),
                         interval=CandleInterval.CANDLE_INTERVAL_1_MIN)
        df_list.append(df)
        time.sleep(0.2)

    res = pd.concat(df_list, axis=0, ignore_index=True)
    res.to_csv(f'data/shares_data/companies_pref/{tickers[num]}.csv')
