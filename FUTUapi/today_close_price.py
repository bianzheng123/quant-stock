import __init__
from futu import *
import pandas as pd
from datetime import datetime


def get_today_close_price(stock_code):
    """
    获取港股最新收盘价
    :param stock_code: 港股代码（如'00700'）
    :return: float类型收盘价
    """
    quote_ctx = None
    try:
        # 连接行情服务
        quote_ctx = OpenQuoteContext(host='172.18.64.1', port=11111)

        # 代码格式转换（添加.HK后缀）
        futu_code = f"HK.{stock_code}"

        # 获取市场快照（含最新价）
        ret, snapshot = quote_ctx.get_market_snapshot([futu_code])
        if ret == RET_OK:
            print(snapshot)
            latest_close = snapshot.iloc[0]['last_price']
            return round(latest_close, 2)
        else:
            print(f"获取{stock_code}数据失败：{snapshot}")
            return None

    except Exception as e:
        print(f"API异常：{str(e)}")
        return None
    finally:
        if quote_ctx:
            quote_ctx.close()


# 测试案例
if __name__ == "__main__":
    test_cases = [
        ('00700', '腾讯控股'),
        ('09988', '阿里巴巴'),
        ('03690', '美团-W'),
        ('00005', '汇丰控股')
    ]

    print("=== 港股收盘价测试 ===")
    for code, name in test_cases:
        price = get_today_close_price(code)
        if price:
            print(f"{name}({code}) 最新收盘价：{price} 港币")
        else:
            print(f"{name}({code}) 数据获取失败")
