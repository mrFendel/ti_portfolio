from portfolio_analytics.utils import *
import pandas as pd


# TODO: change of currency
def pflo_totals(acc_token: str, id: str, show=False):
    """ Gathers total portfolio statistics to DataFrame """

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


def agg_pflo_totals(acc_token: str, mode=''):
    """ Gathers positions statistics for all portfolios to DataFrame """

    acc_id_list = accs_id(acc_token)
    df_list = [pflo_totals(acc_token, acc_id)[0] for acc_id in acc_id_list]
    df_agg = df_list[0]
    if len(acc_id_list) > 1:
        for i in range(1, len(df_list)):
            df_add = df_list[i]
            df_agg['AMOUNT'] = df_agg['AMOUNT'] + df_add['AMOUNT']
    return df_agg


def pflo_positions(acc_token: str, id: str, mode=''):
    """ Gathers portfolio positions statistics to DataFrame """

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


def agg_pflo_positions(acc_token: str, mode=''):
    """ Gathers positions statistics for all portfolios to DataFrame """

    acc_id_list = accs_id(acc_token)
    df_list = [pflo_positions(acc_token, acc_id, mode) for acc_id in acc_id_list]
    return pd.concat(df_list, ignore_index=True)


# TODO: process positions request
def positions(acc_token: str, id: str):
    with Client(acc_token) as client:
        ops = client.operations
        response = ops.get_positions(account_id=id)
    return response
