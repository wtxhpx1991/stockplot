# __author:wtxhpx1991
# data:2019/12/6


import pandas as pd
from WindPy import *

w.start()


def get_wsd(*args):
    raw_data = w.wsd(*args)
    code, field, *rest = args
    raw_data_result = pd.DataFrame(raw_data.Data).T
    raw_data_result.index = raw_data.Times
    if len(code.split(',')) == 1:
        raw_data_result.columns = raw_data.Fields
        raw_data_result['windcode'] = code
        # raw_data_result.index.name = 'index'
        raw_data_result = raw_data_result.reset_index()
    if len(field.split(',')) == 1:
        raw_data_result.columns = raw_data.Codes
        raw_data_result = pd.melt(raw_data_result.reset_index(), id_vars='index', var_name='windcode',
                                  value_name=raw_data.Fields[0])
        # raw_data_result = raw_data_result.set_index(['index'])
    raw_data_result.rename(columns={'index': 'datetime'}, inplace=True)
    return raw_data_result


a = get_wsd("801890.SI", "close,amt,pct_chg,free_turn,mfd_netbuyamt,mfd_netbuyamt_a", "ED-6D", "2019-12-05",
            "unit=1;traderType=1;Fill=Previous;PriceAdj=F")

b = get_wsd("801880.SI,801890.SI", "close", "ED-6D", "2019-12-05",
            "unit=1;traderType=1;Fill=Previous;PriceAdj=F")
