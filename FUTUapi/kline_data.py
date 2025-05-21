import __init__
from futu import *
import pandas as pd

quote_ctx = OpenQuoteContext(host='172.18.64.1', port=11111)
ret, data, page_req_key = quote_ctx.request_history_kline('HK.800000', ktype=KLType.K_3M, start='2024-02-24',
                                                          end='2024-03-21',
                                                          max_count=None)  # 每页5个，请求第一页
if ret == RET_OK:
    print(data)
    print(data['code'][0])  # 取第一条的股票代码
    print(data['close'].values.tolist())  # 第一页收盘价转为 list
else:
    print('error:', data)
while page_req_key != None:  # 请求后面的所有结果
    print('*************************************')
    ret, data, page_req_key = quote_ctx.request_history_kline('HK.800000', start='2024-02-24', end='2024-03-21',
                                                              max_count=None, page_req_key=page_req_key)  # 请求翻页后的数据
    if ret == RET_OK:
        print(data)
    else:
        print('error:', data)
print('All pages are finished!')
data.to_csv('3Min_k-hang_seng-2024_02_24-2024_03_21.csv', encoding='utf-8', index=False)
quote_ctx.close()  # 结束后记得关闭当条连接，防止连接条数用尽
