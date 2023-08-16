totals = ['total_amount_portfolio', 'total_amount_currencies', 'total_amount_etf', 'total_amount_shares',
          'total_amount_bonds', 'total_amount_futures', 'total_amount_options', 'total_amount_sp']

pflo_pos_full = ['figi', 'instrument_type', 'quantity', 'average_position_price', 'expected_yield', 'current_nkd',
                 'average_position_price_pt', 'current_price', 'average_position_price_fifo', 'quantity_lots',
                 'blocked', 'position_uid', 'instrument_uid', 'var_margin', 'expected_yield_fifo']

pflo_pos = ['figi', 'instrument_type', 'quantity', 'average_position_price',
            'expected_yield', 'current_price', 'quantity_lots']

pflo_pos_short = ['figi', 'quantity', 'average_position_price', 'current_price']


instrument = ['ticker', 'name', 'exchange', 'country_of_risk', 'country_of_risk_name', 'instrument_type']

pref_tickers = ['SBER', 'TGKB', 'CNTL', 'KZOS', 'SNGS', 'RTKM', 'NKNC', 'LSNG', 'PMSB',
                'MTLR', 'TATN', 'KAZT', 'BANE', 'LNZL']