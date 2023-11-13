import creds
from utils import *
from datetime import datetime
from keys import pref_tickers as tickers

tok = creds.token_ro_all
pref_tickers = list(map(lambda string: string + 'P', tickers))

tkrs = ['GAZP', 'PLZL']
figis = get_figi(tkrs, ru=True, api_avalable=True)
# pref_figis = get_figi(pref_tickers, ru=True, api_avalable=True)
print(figis)
end = datetime(year=2023, month=8, day=10)
for num in range(len(figis)):
    download_candles(acc_token=tok,
                     figi=figis[num],
                     from_=end - timedelta(days=900, minutes=3),
                     interval=Interval.m1,
                     alt_name=tkrs[num],
                     path='data/shares_data/companies/')


# for num in range(len(pref_figis)):
#     download_candles(acc_token=tok,
#                      figi=pref_figis[num],
#                      from_=end - timedelta(days=10, minutes=3),
#                      interval=Interval.m1,
#                      alt_name=pref_tickers[num],
#                      path='data/shares_data/companies_pref/')
