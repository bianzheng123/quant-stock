import __init__
from futu import *

# SysConfig.enable_proto_encrypt(is_encrypt=True)
# SysConfig.set_init_rsa_file("/home/bianzheng/software/FUTUapi/private_key.txt")  # rsa 私钥文件路径

quote_ctx = OpenQuoteContext(host='172.18.64.1', port=11111)

ret, data = quote_ctx.get_market_snapshot(['SH.600000', 'HK.00700'])
if ret == RET_OK:
    print(data)
    print(data['code'][0])  # 取第一条的股票代码
    print(data['code'].values.tolist())  # 转为 list
else:
    print('error:', data)
quote_ctx.close()  # 结束后记得关闭当条连接，防止连接条数用尽
