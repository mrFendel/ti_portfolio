import creds
from utils import all_shares_info

tok = creds.token_ro_all

data = all_shares_info(acc_token=tok, short=True)

data = data.loc[data['api_trade_available_flag'] == True]
# data = data.loc[(data['currency'] == 'rub') & (data['api_trade_available_flag'] == True)]
data.to_csv('../data/all_shares_info_short.csv')
