import __init__
from futu import *
quote_ctx = OpenQuoteContext(host='172.18.64.1', port=11111)

ret, data = quote_ctx.get_market_state(['HK.800000', 'HK.00700'])
if ret == RET_OK:
    print(data)
else:
    print('error:', data)
quote_ctx.close() # 结束后记得关闭当条连接，防止连接条数用尽