import pandas as pd


def match_ts(ts1: pd.DataFrame, ts2: pd.DataFrame):
    """ Match two Time Series data (DataFrames) by time"""
    init_shape = [ts.shape[0] for ts in [ts1, ts2]]
    ts1 = pd.merge(ts1, ts2['time'], on='time', how='inner')
    ts2 = pd.merge(ts2, ts1['time'], on='time', how='inner')
    res_shape = [ts.shape[0] for ts in [ts1, ts2]]
    pct = [100.0 * round(float(init_shape[i] - res_shape[i]) / init_shape[i], 3) for i in range(2)]
    for i in range(2):
        print(f'Time Series{i+1}:  {pct[i]}% is missing ({init_shape[i]} ==> {res_shape[i]})')
    return ts1, ts2
