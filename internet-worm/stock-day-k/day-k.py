'''
====================
@author: Bian Zheng
@time: 2021/8/9 
@email: 1317257555@qq.com
====================
'''

import baostock as bs
import pandas as pd
import datetime


def get_day_k(stock_code, stock_name, start_date, end_date):
    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)

    #### 获取沪深A股历史K线数据 ####
    # 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
    # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
    # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
    rs = bs.query_history_k_data_plus(stock_code,
                                      "date,open,high,low,close,volume",
                                      start_date=start_date, end_date=end_date,
                                      frequency="d", adjustflag="3")
    print('query_history_k_data_plus respond error_code:' + rs.error_code)
    print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)

    #### 打印结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)

    #### 结果集输出到csv文件 ####
    result.to_csv("day-k-%s.csv" % stock_name, index=False)
    print(result)

    #### 登出系统 ####
    bs.logout()
    return result


if __name__ == '__main__':
    stock_m =  {
        '东风汽车': 'sh.600006',
        '包钢股份': 'sh.600010',
        '沪深300': 'sz.399300',
        '创业板指': 'sz.399006',
        '中证500': 'sz.399905'
    }
    now_string = datetime.datetime.now().strftime('%Y-%m-%d')
    for tmp in stock_m:
        get_day_k(stock_code=stock_m[tmp], stock_name=tmp, start_date='2013-01-01', end_date=now_string)
