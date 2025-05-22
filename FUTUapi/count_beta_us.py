import yfinance as yf
import pandas as pd
import numpy as np
import statsmodels.api as sm
from datetime import datetime
from dateutil.relativedelta import relativedelta


def get_today_close_price(stock_code_l:list[str]):
    """
    获取多个股票的最新日线收盘价（带错误重试）

    参数：
    - symbols: 股票代码列表 (如 ['AAPL', '0700.HK', '^HSI'])
    - max_retries: 最大重试次数
    - delay: 重试间隔(秒)

    返回：
    DataFrame[代码, 最新收盘价, 货币, 交易日期, 时区]
    """
    code2price_m = {}

    for code in stock_code_l:
        ticker = yf.Ticker(code)

        # 获取最近2天数据确保覆盖最新交易日
        hist = ticker.history(period="2d")

        if not hist.empty:
            # 获取市场时区信息
            market_tz = ticker.fast_info['timezone']  # 自动识别市场时区

            # 转换时区并获取最新收盘价
            last_close = hist['Close'].iloc[-1]
            trade_date = hist.index[-1].tz_convert(market_tz).date()

            # 获取货币信息
            currency = ticker.fast_info['currency']
            code2price_m[code] ={'time': trade_date, 'zone': market_tz, 'name': code, 'currency': currency, 'price': round(last_close, 4)}
        else:
            print(f"警告：{code} 无有效数据")

    return code2price_m


# ================== 数据获取模块 ==================
def get_historical_data(code_list, start_date, end_date, ktype):
    """获取并格式化数据"""
    dfs = []

    for code in code_list:
        # 下载日线数据（美东时区）
        data = yf.download(
            code,
            start=start_date,
            end=end_date,
            interval=ktype,
            progress=False,
            auto_adjust=True  # 自动调整价格
        )
        data.rename(columns={('Close', code): code}, inplace=True)

        dfs.append(data['Close'])

        # dfs.append(pd.Series(name=col_name, dtype='float64'))

    # 合并数据
    df = pd.concat(dfs, axis=1).ffill().dropna()
    return df


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
    # 需要VPN
    test_years = 3
    test_ktype = '1d'

    stock_list = [
        # {'code': 'MSFT', 'quantity': 1000},  # 微软
        # {'code': 'NVDA', 'quantity': 500},  # 英伟达
        # {'code': 'GOOG', 'quantity': 800},  # 谷歌
        {'code': 'EL', 'quantity': 36}  # 雅诗兰黛
    ]
    benchmark_code = '^SPX'  # 恒生指数作为市场基准
    current_datetime = datetime.now()
    start_date_time = current_datetime - relativedelta(years=test_years)

    start_date = start_date_time.strftime('%Y-%m-%d')
    end_date = current_datetime.strftime('%Y-%m-%d')

    # 获取历史数据
    codes = [s['code'] for s in stock_list] + [benchmark_code]
    price_data = get_historical_data(codes, start_date, end_date, test_ktype)

    # 计算收益率
    returns = calculate_returns(price_data)
    # print("returns", returns)
    market_returns = returns[benchmark_code]

    code2now_price_m = get_today_close_price([sl['code'] for sl in stock_list])

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
    print(f"投资组合当前市值: {total_value:.2f} 美金，需要对冲的市值: {portfolio_beta * total_value:.2f} 美金")
