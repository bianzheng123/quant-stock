import __init__
import futu
import pandas as pd
import numpy as np
import statsmodels.api as sm
from datetime import datetime
from dateutil.relativedelta import relativedelta


def get_today_close_price(stock_code_l: list[str]):
    """
    获取港股最新收盘价
    :param stock_code: 港股代码（如'00700'）
    :return: float类型收盘价
    """
    quote_ctx = None
    try:
        # 连接行情服务
        quote_ctx = futu.OpenQuoteContext(host='172.18.64.1', port=11111)
        stock_price_m = {}  # code: price

        # 获取市场快照（含最新价）
        ret, snapshot = quote_ctx.get_market_snapshot(stock_code_l)
        if ret == futu.RET_OK:
            price_m = snapshot[['code', 'name', 'update_time', 'last_price']].to_dict(orient='records')
            code2price_m = {item['code']: {'time': item['update_time'],
                                           'name': item['name'],
                                           'price': item['last_price']} for item in price_m}
            return code2price_m
        else:
            print(f"获取{stock_code_l}数据失败：{snapshot}")
            return None

    except Exception as e:
        print(f"API异常：{str(e)}")
        return None
    finally:
        if quote_ctx:
            quote_ctx.close()


# ================== 数据获取模块 ==================
def get_historical_data(code_list, start, end, ktype):
    """获取历史行情数据"""
    quote_ctx = futu.OpenQuoteContext(host='172.18.64.1', port=11111)
    dfs = []

    for code in code_list:
        ret, data, page_req_key = quote_ctx.request_history_kline(code, start=start, end=end, ktype=ktype)
        if ret == futu.RET_OK:
            df = data.set_index('time_key')[['close']]
            df.columns = [code]
            dfs.append(df)
        else:
            print(f"获取{code}数据失败：{data}")

    quote_ctx.close()
    return pd.concat(dfs, axis=1).ffill().dropna()


# ================== 收益率计算 ==================
def calculate_returns(data):
    """计算对数收益率"""
    return np.log(data / data.shift(1)).dropna()


# ================== β系数计算 ==================
def calculate_beta(stock_returns, market_returns):
    """使用回归法计算β系数"""
    X = sm.add_constant(market_returns)
    model = sm.OLS(stock_returns, X).fit()
    return model.params.iloc[1]


if __name__ == '__main__':
    # 如果是成长股，股性可能会变化，就采用3年，测试日线。这种测试使得更加能贴近当前的收益率分布，排除过时的信息
    # 如果是价值股，股性不太可能变化，就采用5年，测试月线。这个使得估计更加准确，消除短期波动
    test_years = 3
    test_ktype = futu.KLType.K_DAY

    stock_list = [
        # {'code': 'HK.00700', 'quantity': 1000},  # 腾讯控股
        # {'code': 'HK.09988', 'quantity': 500},  # 阿里巴巴
        # {'code': 'HK.03690', 'quantity': 800},  # 美团
        {'code': 'HK.09961', 'quantity': 100}  # 携程
    ]
    benchmark_code = 'HK.800000'  # 恒生指数作为市场基准
    current_datetime = datetime.now()
    start_date_time = current_datetime - relativedelta(years=test_years)

    start_date = start_date_time.strftime('%Y-%m-%d')
    end_date = current_datetime.strftime('%Y-%m-%d')

    # 获取历史数据
    codes = [s['code'] for s in stock_list] + [benchmark_code]
    price_data = get_historical_data(codes, start_date, end_date, test_ktype)
    # print("price_data", price_data)

    # 计算收益率
    returns = calculate_returns(price_data)
    # print("returns", returns)
    market_returns = returns[benchmark_code]

    code2now_price_m = get_today_close_price([sl['code'] for sl in stock_list])
    print(code2now_price_m)

    # 计算组合权重
    total_value = sum(s['quantity'] * code2now_price_m[s['code']]['price'] for s in stock_list)
    weights = [s['quantity'] * code2now_price_m[s['code']]['price'] / total_value for s in stock_list]

    # 计算个股β
    stock_betas = []
    for s in stock_list:
        beta = calculate_beta(returns[s['code']], market_returns)
        stock_betas.append(beta)
        print(f"{s['code']} {code2now_price_m[s['code']]['name']} 的β系数: {beta:.2f}")

    # 计算组合β
    portfolio_beta = sum(w * b for w, b in zip(weights, stock_betas))
    print(f"你目前持有: " + ', '.join(
        [f"{code2now_price_m[stock_info['code']]['name']} {stock_info['quantity']}股" for stock_info in stock_list]))
    print(f"\n投资组合整体β系数: {portfolio_beta:.2f}")
    print(f"投资组合当前市值: {total_value:.2f} 港币，需要对冲的市值: {portfolio_beta * total_value:.2f} 港币")
