import baostock as bs
import pandas as pd

# 得到季度利润, 并保存
eval_year = 2017
eval_quarter = 1

# 登陆系统
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:' + lg.error_code)
print('login respond  error_msg:' + lg.error_msg)
pd_company_code = pd.read_csv('stock-code.csv')


def get_profit(code_l):
    # 查询季频估值指标盈利能力
    profit_list = []
    for code in code_l:
        print(code)
        rs_profit = bs.query_profit_data(code=code, year=eval_year, quarter=eval_quarter)
        profit_list.append(rs_profit.get_row_data())
    result_profit = pd.DataFrame(profit_list, columns=rs_profit.fields)
    return result_profit


# profit_total = pd.concat([get_profit(code) for code in pd_company_code['code']], ignore_index=True)
profit_total = get_profit(pd_company_code['code'])
profit_total = profit_total.dropna(how='all')
profit_total.to_csv("profit-quarter-%d-%d.csv" % (eval_year, eval_quarter), encoding="utf-8", index=False)
print(profit_total)

# 登出系统
bs.logout()
