import baostock as bs
import pandas as pd

# 得到季度利润, 并保存
eval_year = 2017
eval_quarter = 1
pd.set_option("display.max_rows", 10)
month_k = pd.read_csv('month-k-%d-%d.csv' % (eval_year, eval_quarter))
profit_quarter = pd.read_csv('profit-quarter-%d-%d.csv' % (eval_year, eval_quarter))
stock_code = pd.read_csv('stock-code.csv')

stock_capital = pd.merge(month_k, profit_quarter, how='inner', on='code')
stock_capital = pd.merge(stock_capital, stock_code, how='inner', on='code')
stock_capital['total_capital'] = stock_capital['liqaShare'] * stock_capital['close']
stock_capital.sort_values(by='total_capital', ascending=False)
stock_capital = stock_capital.rename(columns={'close': 'stock_value'})
stock_capital = stock_capital.loc[:, ['code', 'total_capital', 'code_name', 'liqaShare', 'stock_value']]
print(stock_capital)
stock_capital.to_csv('market-capital-2017-1.csv', index=False)
