import pandas as pd


def match_ts(ts1: pd.DataFrame, ts2: pd.DataFrame, join_with: str = None):
    """ Match two Time Series data (DataFrames) by time"""
    init_shape = [ts.shape[0] for ts in [ts1, ts2]]
    ts1 = pd.merge(ts1, ts2['time'], on='time', how='inner')
    ts2 = pd.merge(ts2, ts1['time'], on='time', how='inner')
    res_shape = [ts.shape[0] for ts in [ts1, ts2]]
    pct = [100.0 * round(float(init_shape[i] - res_shape[i]) / init_shape[i], 3) for i in range(2)]
    for i in range(2):
        print(f'Time Series{i+1}:  {pct[i]}% is missing ({init_shape[i]} ==> {res_shape[i]})')
    if join_with is not None:
        res = pd.DataFrame()
        res['time'] = ts1['time']
        res['ts1'] = ts1[join_with]
        res['ts2'] = ts2[join_with]
        return res
    else:
        return ts1, ts2
