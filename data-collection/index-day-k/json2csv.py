'''
====================
@author: Bian Zheng
@time: 2021/8/12 
@email: 1317257555@qq.com
====================
'''
import json
import pandas as pd

data = pd.read_csv('自选股.txt', delimiter=" ")
for i in range(len(data)):
    # for i in range(1):
    tmp_data = data.loc[i]
    tmp_index_code = tmp_data['指数代码']
    tmp_index_name = tmp_data['指数名称']
    df = pd.read_json('json-data/%s-%s.json' % (tmp_index_name, tmp_index_code))
    df.rename(columns={'lclose': 'open', 'tclose': 'close', 'tradedate': 'date'}, inplace=True)
    del df['indx_code'], df['changes']
    order = ['date', 'open', 'close']
    df = df[order]
    df.to_csv('csv-data/day-k-%s-%s.csv' % (tmp_index_name, tmp_index_code), encoding='utf-8', index=False)
    # print(df)
