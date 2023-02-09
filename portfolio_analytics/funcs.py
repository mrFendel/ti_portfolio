from tinkoff.invest import Client, MoneyValue, Quotation, InstrumentIdType
import pandas as pd
import portfolio_analytics.keys as keys
# TODO: aggregate data by all accounts


def to_decimal(value, currency=False):
    if currency:
        return value.units + value.nano * 10 ** -9, value.currency
    else:
        return value.units + value.nano * 10**-9


def accs_info(acc_token: str):
    with Client(acc_token) as client:
        response = client.users.get_accounts()
    return response


def conditional_to_decimals(obj, currency=False):
    if isinstance(obj, MoneyValue):
        return to_decimal(obj, currency=currency)
    elif isinstance(obj, Quotation):
        return to_decimal(obj)
    else:
        return obj


# TODO: change of currency
def pflo_totals(acc_token: str, id: str, show=False):
    with Client(acc_token) as client:
        response = client.operations.get_portfolio(account_id=id)
        totals_df = pd.DataFrame([(to_decimal(getattr(response, key), currency=True)) for key in keys.totals],
                                 index=keys.totals,
                                 columns=['AMOUNT', 'CURRENCY'])
        pct_profit = to_decimal(response.expected_yield)
    if show:
        print('TOTALS:')
        print(totals_df)
        print(f'PROFIT:  {pct_profit} %')
    return totals_df, pct_profit


def pos_data_to_dict(position_data, keys_list):
    data = {key: conditional_to_decimals(getattr(position_data, key)) for key in keys_list}
    data['currency'] = position_data.current_price.currency
    return data


def instrument_info(acc_token: str, figi: str):
    with Client(acc_token) as client:
        response = client.instruments.get_instrument_by(id_type=InstrumentIdType(1), id=figi)
        return {key: getattr(response.instrument, key) for key in keys.instrument}


def pflo_positions(acc_token: str, id: str, mode=''):
    if mode == 'short':
        keys_list = keys.pflo_pos_short
    elif mode == 'long':
        keys_list = keys.pflo_pos_full
    else:
        keys_list = keys.pflo_pos

    with Client(acc_token) as client:
        positions_list = client.operations.get_portfolio(account_id=id).positions
        positions_df = pd.DataFrame([pos_data_to_dict(position, keys_list) for position in positions_list],
                                    columns=keys_list.copy().append('currency'))

        names_list = list()
        for position in positions_list:
            res = client.instruments.get_instrument_by(id_type=InstrumentIdType(1), id=position.figi)
            names_list.append({'ticker': res.instrument.ticker, 'name': res.instrument.name})
        names_df = pd.DataFrame(names_list, columns=['ticker', 'name'])

        positions_df = pd.concat([names_df, positions_df], axis=1)
    return positions_df


# TODO: process positions request
def positions(acc_token: str, id: str):
    with Client(acc_token) as client:
        ops = client.operations
        response = ops.get_positions(account_id=id)
    return response
