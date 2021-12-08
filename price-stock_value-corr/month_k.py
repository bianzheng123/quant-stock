import baostock as bs
import pandas as pd

# 登陆系统
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:' + lg.error_code)
print('login respond  error_msg:' + lg.error_msg)

stock_code = pd.read_csv('stock-code.csv')

#### 打印结果集 ####
data_list = []
for i, code in enumerate(stock_code['code'], 0):
    #### 获取沪深A股历史K线数据 ####
    # 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
    # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
    # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
    rs = bs.query_history_k_data_plus(code,
                                      "code, date, close",
                                      start_date='2021-7-30', end_date='2021-7-30',
                                      frequency="m", adjustflag="3")
    print(code)
    assert rs.error_code != 0
    data_list.append(rs.get_row_data())
result = pd.DataFrame(data_list, columns=rs.fields)
result = result.dropna(how='all')
result.to_csv('month-k-2021-7-30.csv', index=False)

# 登出系统
bs.logout()
