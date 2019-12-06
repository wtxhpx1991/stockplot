# __author:wtxhpx1991
# data:2019/12/6


import pandas as pd
from WindPy import *

w.start()


def get_wsd(*args):
    '''
    获取wind分钟级数据，并做数据清洗
    :param args: w.wsd参数
    :return: dataframe结构
    '''
    raw_data = w.wsd(*args)
    code, field, *rest = args
    raw_data_result = pd.DataFrame(raw_data.Data).T
    raw_data_result.index = raw_data.Times
    if len(code.split(',')) == 1:
        raw_data_result.columns = raw_data.Fields
        raw_data_result['wind_code'] = code
        raw_data_result = raw_data_result.reset_index()
    if len(field.split(',')) == 1:
        raw_data_result.columns = raw_data.Codes
        raw_data_result = pd.melt(raw_data_result.reset_index(), id_vars='index', var_name='wind_code',
                                  value_name=raw_data.Fields[0])
    raw_data_result.rename(columns={'index': 'date'}, inplace=True)
    return raw_data_result


def get_wset(*args):
    raw_data = w.wset(*args)
    raw_data_result = pd.DataFrame(raw_data.Data).T
    raw_data_result.columns = raw_data.Fields
    return raw_data_result


a = get_wsd("801890.SI", "close,amt,pct_chg,free_turn,mfd_netbuyamt,mfd_netbuyamt_a", "ED-6D", "2019-12-05",
            "unit=1;traderType=1;Fill=Previous;PriceAdj=F")

b = get_wsd("801880.SI,801890.SI", "close", "ED-6D", "2019-12-05",
            "unit=1;traderType=1;Fill=Previous;PriceAdj=F")

c = get_wset("sectorconstituent", "date=2019-12-06;sectorid=a39901011g000000")
