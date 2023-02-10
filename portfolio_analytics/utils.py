import pandas as pd
from tinkoff.invest import Client, MoneyValue, Quotation, InstrumentIdType
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
