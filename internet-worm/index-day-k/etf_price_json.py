'''
====================
@author: Bian Zheng
@time: 2021/8/12 
@email: 1317257555@qq.com
====================
'''
import pandas as pd
import requests
from urllib.parse import quote
import json


def etf_price(index_code, index_name):
    # 给定指数代码, 从中证指数有限公司官网(http://www.csindex.com.cn/)爬取该指数5年的数据
    # 年至今, 1个月, 3个月, 5年
    # http://www.csindex.com.cn/zh-CN/indices/index-detail/H30015?earnings_performance=5%E5%B9%B4&data_type=json
    # %E5%B9%B4
    time_encode = quote('5年', encoding='utf-8')
    url_ = 'http://www.csindex.com.cn/zh-CN/indices/index-detail/{}?earnings_performance={}&data_type=json'.format(
        index_code, time_encode)
    headers = {
        "Host": "www.csindex.com.cn",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "acw_tc=2f624a6a16285094760041987e7129162536806b3676cb31104f4fbe69f30e; "
                  "Hm_lvt_12373533b632515a7c0ccd65e7fc5835=1628501622,1628509476; "
                  "Hm_lpvt_12373533b632515a7c0ccd65e7fc5835=1628510702; "
                  "XSRF-TOKEN"
                  "=eyJpdiI6IlJQQ1BSNFJCa0szVXFNMzA5Wkp3b0E9PSIsInZhbHVlIjoiUjd4aVlQQXdQVmpTejNYUGREMXhlaUV2THp1Wkx5STlXNW9LbHRcL1lJcnJ4ajVxXC9TUlVWaDQyOVl4M2J5SFJzXC9PbmNuZE5weFBqV0lBSlVIc1A3NlE9PSIsIm1hYyI6IjA0YjdjNmM5MTY4N2YwMmM5ZDFlMDNjMWQxYjY2NjZiMGI4NDNkMWM0MDVmZjlhOWUwMGM2ZjRmOGZhOGQ5YTAifQ%3D%3D; laravel_session=eyJpdiI6Ild1ajc2bmRcL3FHSVNcL0tcL2JNK05oaWc9PSIsInZhbHVlIjoiWll1S0dzblcxT0ltdlwvRE5uOWYrXC92YUJNRDV4T2NqSWc3ZUJ2RTVwQlpzSmJOSkpiNVVST0Y4T2lPNnRabXorNHNEWUFzaGFObXQyY2hYMFRnVEhsZz09IiwibWFjIjoiNzc3ODZhMjY4YzE0YzJmMzFiZGVmNzYyNTM0MWExMTg4ZmZlODYxYTZhNjNiYjRmZGMzY2UwYmE4MjU5MTFlNSJ9 "
    }
    trade_json = requests.get(url_, headers=headers).text
    trade_json = json.loads(trade_json)
    print(url_)
    with open('%s-%s.json' % (index_name, index_code), 'w', encoding='utf-8') as f:
        json.dump(trade_json, f)


data = pd.read_csv('自选股.txt', delimiter=" ")
for i in range(len(data)):
    tmp_data = data.loc[i]
    etf_price(tmp_data['指数代码'], tmp_data['指数名称'])
