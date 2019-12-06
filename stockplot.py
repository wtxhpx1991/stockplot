# __author:wtxhpx1991
# data:2019/12/6

import getdata
import pandas as pd
import datetime

YESTERDAY = (datetime.datetime.today() - datetime.timedelta(1)).strftime("%Y-%m-%d")
SECTORID = "a39901011g000000"
fmt = "date={TODAY};sectorid={SECTORID}"
# 获取申万一级行业代码
swindex = getdata.get_wset("sectorconstituent", fmt.format(TODAY=YESTERDAY, SECTORID=SECTORID))
# 获取逐日交易数据
daily_data = pd.DataFrame({})
for wind_code in swindex['wind_code']:
    daily_data = daily_data.append(
        getdata.get_wsd(wind_code, "close,amt,pct_chg,free_turn,mfd_netbuyamt,mfd_netbuyamt_a", "ED-6D", YESTERDAY,
                        "unit=1;traderType=1;Fill=Previous;PriceAdj=F"))
