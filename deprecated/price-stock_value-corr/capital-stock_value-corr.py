import pandas as pd
import numpy as np

market_capital = pd.read_csv('market-capital-2017-1.csv')
market_capital = market_capital.rename(columns={'stock_value': '2017_price'})

month_k_2021 = pd.read_csv('month-k-2021-7-30.csv')
month_k_2021 = month_k_2021.rename(columns={'close': 'now_price'})
stock_capital = pd.merge(month_k_2021, market_capital, how='inner', on='code')
value_diff = stock_capital.loc[:, ['code_name', 'liqaShare', 'now_price', '2017_price']]
value_diff['price_diff'] = stock_capital['now_price'] - stock_capital['2017_price']

mean_price_diff = value_diff.loc[:, ['price_diff']].mean()[0]
mean_total_capital = value_diff.loc[:, ['liqaShare']].mean()[0]
value_diff['cov_value'] = (value_diff['price_diff'] - mean_price_diff) * (value_diff['liqaShare'] - mean_total_capital)
print(value_diff['cov_value'])

var_price_diff = value_diff.loc[:, ['price_diff']].var()[0]
var_total_capital = value_diff.loc[:, ['liqaShare']].var()[0]

corr = value_diff['cov_value'].mean() / np.sqrt(var_price_diff * var_total_capital)

print(corr)