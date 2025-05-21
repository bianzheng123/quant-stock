import __init__
import futu
import pandas as pd
import numpy as np
import statsmodels.api as sm

# ================== 配置区 ==================
stock_list = [
    # {'code': 'HK.00700', 'quantity': 1000},  # 腾讯控股
    # {'code': 'HK.09988', 'quantity': 500},  # 阿里巴巴
    {'code': 'HK.03690', 'quantity': 800}  # 美团
]
benchmark_code = 'HK.800000'  # 恒生指数作为市场基准
start_date = '2024-01-01'
end_date = '2025-05-20'


# ================== 数据获取模块 ==================
def get_historical_data(code_list, start, end):
    """获取历史行情数据"""
    quote_ctx = futu.OpenQuoteContext(host='172.18.64.1', port=11111)
    dfs = []

    for code in code_list:
        ret, data, page_req_key = quote_ctx.request_history_kline(code, start=start, end=end, ktype=futu.KLType.K_DAY)
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
    return model.params[1]


# ================== 主程序 ==================
if __name__ == '__main__':
    # 获取历史数据
    codes = [s['code'] for s in stock_list] + [benchmark_code]
    price_data = get_historical_data(codes, start_date, end_date)
    print("price_data", price_data)

    # 计算收益率
    returns = calculate_returns(price_data)
    print("returns", returns)
    market_returns = returns[benchmark_code]

    # 计算组合权重
    total_value = sum(s['quantity'] * price_data[s['code']].iloc[-1] for s in stock_list)
    weights = [s['quantity'] * price_data[s['code']].iloc[-1] / total_value for s in stock_list]

    # 计算个股β
    stock_betas = []
    for s in stock_list:
        beta = calculate_beta(returns[s['code']], market_returns)
        stock_betas.append(beta)
        print(f"{s['code']} 的β系数: {beta:.2f}")

    # 计算组合β
    portfolio_beta = sum(w * b for w, b in zip(weights, stock_betas))
    print(f"\n投资组合整体β系数: {portfolio_beta:.2f}")