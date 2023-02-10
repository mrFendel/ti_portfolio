from tinkoff.invest import Client, MoneyValue, Quotation, InstrumentIdType
import portfolio_analytics.keys as keys


def to_decimal(value, currency=False):
    """ Converts MoneyValue or Quantity class to decimal form and also returns currency """

    if currency:
        return value.units + value.nano * 10 ** -9, value.currency
    else:
        return value.units + value.nano * 10**-9


def conditional_to_decimals(obj, currency=False):
    """ Converts MoneyValue or Quantity class to decimal form and also returns currency """

    if isinstance(obj, MoneyValue):
        return to_decimal(obj, currency=currency)
    elif isinstance(obj, Quotation):
        return to_decimal(obj)
    else:
        return obj


# TODO: to dict to DF
def accs_info(acc_token: str):
    """ Gets info about Clients accounts """

    with Client(acc_token) as client:
        response = client.users.get_accounts()
    return response


def accs_id(acc_token: str):
    """ Gathers accounts ids to list """

    accounts_list = accs_info(acc_token).accounts
    return [getattr(acc, 'id') for acc in accounts_list]


def pos_data_to_dict(position_data, keys_list):
    """ Gathers position's information to dictionary """

    data = {key: conditional_to_decimals(getattr(position_data, key)) for key in keys_list}
    data['currency'] = position_data.current_price.currency
    return data


def instrument_info(acc_token: str, figi: str):
    """ Gathers instrument's information to dictionary """

    with Client(acc_token) as client:
        response = client.instruments.get_instrument_by(id_type=InstrumentIdType(1), id=figi)
        return {key: getattr(response.instrument, key) for key in keys.instrument}
