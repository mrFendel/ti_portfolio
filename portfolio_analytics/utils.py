from datetime import datetime

import pandas as pd
from tinkoff.invest import Client, MoneyValue, Quotation, InstrumentIdType, InstrumentStatus, CandleInterval
import portfolio_analytics.keys as keys


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
        return dictionary[tickers]
    else:
        return [dictionary[tick] for tick in tickers]


def create_candle_df(candles):
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
                figi: str, from_: datetime,
                to: datetime | None = None,
                interval=CandleInterval.CANDLE_INTERVAL_1_MIN
                ):

    with Client(acc_token) as client:
        response = client.market_data.get_candles(from_=from_, to=to, interval=interval, figi=figi)
        print(len(response.candles))

    return create_candle_df(response.candles)
