# __author:wtxhpx1991
# data:2019/12/6

import getdata
import pandas as pd
import datetime

import matplotlib.pyplot as plt
from matplotlib import cm

plt.style.use('ggplot')

YESTERDAY = (datetime.datetime.today() - datetime.timedelta(1)).strftime("%Y-%m-%d")
SECTORID = "a39901011g000000"
fmt = "date={TODAY};sectorid={SECTORID}"
# 获取申万一级行业代码
swindex = getdata.get_wset("sectorconstituent", fmt.format(TODAY=YESTERDAY, SECTORID=SECTORID))
# 获取逐日交易数据
daily_rawdata = pd.DataFrame({})
for wind_code in swindex['wind_code']:
    daily_rawdata = daily_rawdata.append(
        getdata.get_wsd(wind_code, "close,amt,pct_chg,free_turn_n", "ED-6D", YESTERDAY,
                        "unit=1;traderType=1;Fill=Previous;PriceAdj=F"))
daily_data = daily_rawdata.reset_index(drop=True)
daily_data = pd.merge(daily_data, swindex[['wind_code', 'sec_name']], on='wind_code', how='left')

daily_data_last = daily_data.groupby('wind_code').last()
daily_data_first = daily_data.groupby('wind_code').first()
daily_data_first['PRE_CLOSE'] = daily_data_first['CLOSE'] / (1 + daily_data_first['PCT_CHG'] / 100)
daily_data_last['VOL_MUL'] = (daily_data_last['FREE_TURN_N'] / daily_data.groupby('wind_code')[
    'FREE_TURN_N'].mean() - 1) * 100
daily_data_last['PCT_CHANGE_5D'] = (daily_data_last['CLOSE'] / daily_data_first['PRE_CLOSE'] - 1) * 100
daily_data_cmp = daily_data_last[['date', 'sec_name', 'CLOSE', 'PCT_CHG', 'PCT_CHANGE_5D', 'FREE_TURN_N', 'VOL_MUL']]
daily_data_cmp['sec'] = daily_data_cmp['sec_name'].map(lambda x: x.split("(")[0])

s = daily_data_cmp['VOL_MUL'] * 5
c = daily_data_cmp['FREE_TURN_N']
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.scatter(daily_data_cmp['PCT_CHG'], daily_data_cmp['PCT_CHANGE_5D'], s=s, c=c, cmap=cm.Reds)
for i in range(len(daily_data_cmp)):
    plt.annotate(daily_data_cmp['sec'][i], xy=(daily_data_cmp['PCT_CHG'][i], daily_data_cmp['PCT_CHANGE_5D'][i]),
                 xytext=(daily_data_cmp['PCT_CHG'][i] + 0.01, daily_data_cmp['PCT_CHANGE_5D'][i] + 0.01))
