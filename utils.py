import time
from datetime import datetime, timedelta

import pandas as pd
from tinkoff.invest import Client, MoneyValue, Quotation, InstrumentIdType, InstrumentStatus, CandleInterval
from tqdm import tqdm

import keys as keys
import enum


class Interval(enum.Enum):
    m1 = CandleInterval.CANDLE_INTERVAL_1_MIN
    m2 = CandleInterval.CANDLE_INTERVAL_2_MIN
    m3 = CandleInterval.CANDLE_INTERVAL_3_MIN
    m5 = CandleInterval.CANDLE_INTERVAL_5_MIN
    m10 = CandleInterval.CANDLE_INTERVAL_10_MIN
    m15 = CandleInterval.CANDLE_INTERVAL_15_MIN
    m30 = CandleInterval.CANDLE_INTERVAL_30_MIN
    h1 = CandleInterval.CANDLE_INTERVAL_HOUR

def to_decimal(value, currency=False):
    """ Converts MoneyValue or Quantity class to decimal form and also returns currency """

    if currency:
        return value.units + value.nano * 10 ** -9, value.currency
    else:
        return value.units + value.nano * 10**-9


def conditional_to_decimals(obj, currency=False):
    """ Conditionally converts to decimal form and returns currency if value is MoneyValue or Quantity object """

    if isinstance(obj, MoneyValue):
        return to_decimal(obj, currency=currency)
    elif isinstance(obj, Quotation):
        return to_decimal(obj)
    else:
        return obj


def accs_info(acc_token: str, to_df=False):
    """ Gets info about Clients accounts and could convert it to DataFrame"""

    with Client(acc_token) as client:
        response = client.users.get_accounts()
    if not to_df:
        return response
    else:
        return pd.DataFrame([elem.__dict__ for elem in response.accounts])


def accs_id(acc_token: str):
    """ Gathers accounts ids to list """

    accounts_list = accs_info(acc_token).accounts
    return [getattr(acc, 'id') for acc in accounts_list]


def pos_data_to_dict(position_data, keys_list):
    """ Gathers position's information to dictionary """

    data = {key: conditional_to_decimals(getattr(position_data, key)) for key in keys_list}
    data['currency'] = position_data.current_price.currency
    return data


def instrument_info(acc_token: str, figi: str, short=False):
    """ Gathers instrument's information to Series """

    with Client(acc_token) as client:
        response = client.instruments.get_instrument_by(id_type=InstrumentIdType(1), id=figi)
        if short:
            return pd.Series({key: getattr(response.instrument, key) for key in keys.instrument})
        else:
            return pd.Series(response.instrument.__dict__)


def brand_info(acc_token: str, uid):
    """ Gathers brand's information to Series """

    with Client(acc_token) as client:
        response = client.instruments.get_brands_by(uid)
    return pd.Series(response.__dict__)


def all_shares_info(acc_token: str, short: bool = True):
    """ Gets information about all shares in a form of DataFrame"""
    with Client(acc_token) as cl:
        figi_df = pd.DataFrame(
            cl.instruments.shares(instrument_status=InstrumentStatus.INSTRUMENT_STATUS_ALL).instruments
        )

    if short:
        return figi_df[['figi', 'ticker', 'lot', 'currency', 'name', 'exchange', 'api_trade_available_flag']]
    else:
        return figi_df


def download_all_shares_info(acc_token: str,
                             short=True,
                             ru=False,
                             api_avalable=False):
    """ Saves information about specified shares to CSV """
    data = all_shares_info(acc_token=acc_token, short=True)

    file = '_shares_info'
    if short:
        file = file + '_short'
    if api_avalable:
        file = '_api' + file
        data = data.loc[data['api_trade_available_flag'] == True]

    if ru:
        file = 'ru' + file
        data = data.loc[data['currency'] == 'rub']
    else:
        file = 'all' + file

    data.to_csv(f'../data/{file}.csv')
    print(f'{file}.csv saved.')


def get_figi(tickers: list, ru=False, api_avalable=False, exchange=''):
    """
    Gets figi by ticker
    NB!! USE WITH LISTS FOR OPTIMAL WORK
    """
    file = '_shares_info_short.csv'
    if api_avalable:
        file = '_api' + file
    else:
        pass
    if ru:
        file = 'ru' + file
    else:
        file = 'all' + file

    df = pd.read_csv(f'data/{file}')
    if exchange == '':
        assert df.shape[0] == len(df['ticker'].unique()), 'Tickers are not unique. Specify exchange'
    else:
        df = df[df['exchange'] == exchange]
        assert df.shape[0] == len(df['ticker'].unique()), 'Tickers are not unique.'

    dictionary = dict(zip(df['ticker'].values, df['figi'].values))
    if not tickers:
        return dictionary
    elif len(tickers) == 1:
        return dictionary[tickers[0]]
    else:
        return [dictionary[tick] for tick in tickers]


def create_candle_df(candles):
    """ Makes candle dataframe from raw data """
    df = pd.DataFrame([{
        'time': c.time,
        'volume': c.volume,
        'open': to_decimal(c.open),
        'close': to_decimal(c.close),
        'high': to_decimal(c.high),
        'low': to_decimal(c.low),
    } for c in candles])

    return df


def get_candles(acc_token: str,
                figi: str,
                from_: datetime,
                to: datetime | None = None,
                interval=CandleInterval.CANDLE_INTERVAL_1_MIN
                ):
    """ Gets OHLC data by figi (overwriting of tinkoff lib method) """
    with Client(acc_token) as client:
        response = client.market_data.get_candles(from_=from_, to=to, interval=interval, figi=figi)

    return create_candle_df(response.candles)


def download_candles(acc_token: str,
                     figi: str,
                     from_: datetime,
                     to: datetime = datetime.utcnow(),
                     interval: Interval = Interval.m1,
                     alt_name: str = None,
                     path=''):
    """ Gets & Saves OHLC data by figi to CSV """

    period = to - from_
    iter_num = int(period / timedelta(days=1))
    time_appendix = period - iter_num*timedelta(days=1)

    df_list = []
    if time_appendix > timedelta(minutes=1):
        new_to = to - time_appendix
        df = get_candles(acc_token=acc_token,
                         figi=figi,
                         from_=new_to,
                         to=to,
                         interval=interval)
        df_list.append(df)
        time.sleep(0.5)

    for i in tqdm(range(iter_num)):
        df = get_candles(acc_token=acc_token,
                         figi=figi,
                         from_=new_to - timedelta(days=1 + i),
                         to=new_to - timedelta(days=i),
                         interval=interval)
        df_list.append(df)
        time.sleep(0.5)

    if alt_name is not None:
        filepath = path + alt_name
    else:
        filepath = path + figi

    res = pd.concat(df_list, axis=0, ignore_index=True)
    res.to_csv(f'{filepath}.csv')
    print(f'{figi} i.e. {alt_name} saved successfully.')
