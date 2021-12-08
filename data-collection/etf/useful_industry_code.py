'''
====================
@author: Bian Zheng
@time: 2021/8/11 
@email: 1317257555@qq.com
====================
'''
import requests
from bs4 import BeautifulSoup

url_ = 'http://www.csindex.com.cn/zh-CN/indices/index-detail/930677'
# print(url_)
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
response_text = requests.get(url_, headers=headers).text
soup = BeautifulSoup(response_text, 'lxml')
# print(soup.prettify())
# print(soup.select('.js_txt_new')[0])
cpy = soup.select('.js_txt_new')[0]
for str in cpy.strings:
    if str.strip() == '为反映中证500指数成份中不同细分行业公司股票的整体表现，为投资者提供分析工具，将中证500指数样本股按行业分类标准分为10个一级行业、25个二级行业、60余个三级行业及100多个四级行业。再以进入各二、三级行业的全部股票作为样本编制指数，形成中证500细分行业指数，为投资者从行业角度考量中证500指数提供工具。':
        print("not have the corresponding imitation")
    # print(str.strip())
# print(response_text)
