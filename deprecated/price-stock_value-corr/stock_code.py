import baostock as bs
import pandas as pd
import numpy as np

# 获得上市流通的股票信息
# 登陆系统
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:' + lg.error_code)
print('login respond  error_msg:' + lg.error_msg)

# 获取证券基本资料
rs = bs.query_stock_basic()
print('query_stock_basic respond error_code:' + rs.error_code)
print('query_stock_basic respond  error_msg:' + rs.error_msg)

# 打印结果集
data_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    data_list.append(rs.get_row_data())
result = pd.DataFrame(data_list, columns=rs.fields)
result["type"] = result["type"].astype(np.int)
result["status"] = result["status"].astype(np.int)
result = result[result["type"] == 1]
result = result[result["outDate"] == ""]
result = result[result['status'] == 1]
del result["type"], result["outDate"], result['status']
result.reset_index(drop=True, inplace=True)
print(result)
# 结果集输出到csv文件
result.to_csv("stock-code.csv", encoding="utf-8", index=False)
# print(result)

# 登出系统
bs.logout()
