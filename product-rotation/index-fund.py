# coding=utf-8
'''
====================
@author: Bian Zheng
@time: 2021/8/12 
@email: 1317257555@qq.com
====================
'''
'''
策略一
收盘前计算金融产品A和B的n日涨跌幅(就是判断当天股价和n个交易日前的涨跌幅)
    如果A涨跌幅大于B, 就下日持有A
    否则, 下日持有B
策略二
收盘前计算金融产品A和B的n日涨跌幅(就是判断当天股价和n个交易日前的涨跌幅)
    如果涨跌幅都小于0, 就空仓
    否则
        如果A涨跌幅大于B, 就下日持有A
        否则, 下日持有B
'''

commission_rate = 2 / 10000  # 佣金税
stamp_duty_rate = 0 / 1000  # 印花税
momentum_days = 20  # 计算多少天的涨跌幅
start_date_time = '20180101'

# 计算每一个行业最可能成功的频率, 分析为什么这样的行业轮动会成功, 以及为什么这个轮动的曲线会比别人优秀
# 计算不同曲线之间的相关系数, 使用两个股票的股价作为相关系数
n_total_win = 0

import pandas as pd
import numpy as np
from function import *
import matplotlib.pyplot as plt
import json
import matplotlib as mpl
import copy

mpl.rcParams['font.sans-serif'] = ['KaiTi']
mpl.rcParams['font.serif'] = ['KaiTi']
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数


def run_model(coin1_fname, coin2_fname, coin1_name, coin2_name):
    # 读取数据
    # coin1_df = pd.read_csv('data/index-fund/%s.csv' % coin1_name, encoding='utf-8', parse_dates=['date'])
    # coin2_df = pd.read_csv('data/index-fund/%s.csv' % coin2_name, encoding='utf-8', parse_dates=['date'])
    coin1_df = pd.read_csv(coin1_fname, encoding='utf-8', parse_dates=['date'])
    coin2_df = pd.read_csv(coin2_fname, encoding='utf-8', parse_dates=['date'])

    def strategy1(cpy_coin1, cpy_coin2):
        df_coin1 = copy.deepcopy(cpy_coin1)
        df_coin2 = copy.deepcopy(cpy_coin2)

        # 计算两种币每天的涨跌幅pct
        df_coin1['coin1_pct'] = df_coin1['close'].pct_change(1)
        df_coin2['coin2_pct'] = df_coin2['close'].pct_change(1)
        # 重命名行
        df_coin1.rename(columns={'open': 'coin1_open', 'close': 'coin1_close'}, inplace=True)
        df_coin2.rename(columns={'open': 'coin2_open', 'close': 'coin2_close'}, inplace=True)
        # 合并数据
        df = pd.merge(left=df_coin1[['date', 'coin1_open', 'coin1_close', 'coin1_pct']], left_on=['date'],
                      right=df_coin2[['date', 'coin2_open', 'coin2_close', 'coin2_pct']],
                      right_on=['date'], how='left')
        # 计算N日的涨跌幅momentum
        df['coin1_mom'] = df['coin1_close'].pct_change(periods=momentum_days)
        df['coin2_mom'] = df['coin2_close'].pct_change(periods=momentum_days)
        # 轮动条件
        df.loc[df['coin1_mom'] > df['coin2_mom'], 'style'] = 'coin1'
        df.loc[df['coin1_mom'] < df['coin2_mom'], 'style'] = 'coin2'
        # 相等时维持原来的仓位。
        df['style'].fillna(method='ffill', inplace=True)
        # 收盘才能确定风格，实际的持仓pos要晚一天。
        df['pos'] = df['style'].shift(1)
        # 删除持仓为nan的天数
        df.dropna(subset=['pos'], inplace=True)
        # 数字货币从17年开始回测
        df = df[df['date'] >= pd.to_datetime(start_date_time)]
        # 计算策略的整体涨跌幅strategy_pct
        df.loc[df['pos'] == 'coin1', 'strategy_pct'] = df['coin1_pct']
        df.loc[df['pos'] == 'coin2', 'strategy_pct'] = df['coin2_pct']

        # 调仓时间
        df.loc[df['pos'] != df['pos'].shift(1), 'trade_time'] = df['date']
        # 将调仓日的涨跌幅修正为开盘价买入涨跌幅
        df.loc[(df['trade_time'].notnull()) & (df['pos'] == 'coin1'), 'strategy_pct_adjust'] = df['coin1_close'] / (
                df['coin1_open'] * (1 + commission_rate)) - 1
        df.loc[(df['trade_time'].notnull()) & (df['pos'] == 'coin2'), 'strategy_pct_adjust'] = df['coin2_close'] / (
                df['coin2_open'] * (1 + commission_rate)) - 1
        df.loc[df['trade_time'].isnull(), 'strategy_pct_adjust'] = df['strategy_pct']
        # 扣除卖出手续费
        df.loc[(df['trade_time'].shift(-1).notnull()), 'strategy_pct_adjust'] = (1 + df[
            'strategy_pct']) * (1 - stamp_duty_rate) - 1
        del df['strategy_pct'], df['style']

        df.reset_index(drop=True, inplace=True)
        # 计算净值
        df['coin1_net'] = df['coin1_close'] / df['coin1_close'][0]
        df['coin2_net'] = df['coin2_close'] / df['coin2_close'][0]
        df['strategy_net'] = (1 + df['strategy_pct_adjust']).cumprod()
        return df

    def strategy2(cpy_coin1, cpy_coin2):
        df_coin1 = copy.deepcopy(cpy_coin1)
        df_coin2 = copy.deepcopy(cpy_coin2)
        # 计算两种币每天的涨跌幅pct
        df_coin1['coin1_pct'] = df_coin1['close'].pct_change(1)
        df_coin2['coin2_pct'] = df_coin2['close'].pct_change(1)
        # 重命名行
        df_coin1.rename(columns={'open': 'coin1_open', 'close': 'coin1_close'}, inplace=True)
        df_coin2.rename(columns={'open': 'coin2_open', 'close': 'coin2_close'}, inplace=True)
        # 合并数据
        df = pd.merge(left=df_coin1[['date', 'coin1_open', 'coin1_close', 'coin1_pct']], left_on=['date'],
                      right=df_coin2[['date', 'coin2_open', 'coin2_close', 'coin2_pct']],
                      right_on=['date'], how='left')
        # 计算N日的涨跌幅momentum
        df['coin1_mom'] = df['coin1_close'].pct_change(periods=momentum_days)
        df['coin2_mom'] = df['coin2_close'].pct_change(periods=momentum_days)
        # 轮动条件
        df.loc[df['coin1_mom'] > df['coin2_mom'], 'style'] = 'coin1'
        df.loc[df['coin1_mom'] < df['coin2_mom'], 'style'] = 'coin2'
        df.loc[(df['coin1_mom'] < 0) & (df['coin2_mom'] < 0), 'style'] = 'empty'
        # 相等时维持原来的仓位。
        df['style'].fillna(method='ffill', inplace=True)
        # 收盘才能确定风格，实际的持仓pos要晚一天。
        df['pos'] = df['style'].shift(1)
        # 删除持仓为nan的天数
        df.dropna(subset=['pos'], inplace=True)
        # 数字货币从17年开始回测
        df = df[df['date'] >= pd.to_datetime(start_date_time)]
        # 计算策略的整体涨跌幅strategy_pct
        df.loc[df['pos'] == 'coin1', 'strategy_pct'] = df['coin1_pct']
        df.loc[df['pos'] == 'coin2', 'strategy_pct'] = df['coin2_pct']
        df.loc[df['pos'] == 'empty', 'strategy_pct'] = 0

        # 调仓时间
        df.loc[df['pos'] != df['pos'].shift(1), 'trade_time'] = df['date']
        # 将调仓日的涨跌幅修正为开盘价买入涨跌幅
        df.loc[(df['trade_time'].notnull()) & (df['pos'] == 'coin1'), 'strategy_pct_adjust'] = df['coin1_close'] / (
                df['coin1_open'] * (1 + commission_rate)) - 1
        df.loc[(df['trade_time'].notnull()) & (df['pos'] == 'coin2'), 'strategy_pct_adjust'] = df['coin2_close'] / (
                df['coin2_open'] * (1 + commission_rate)) - 1
        df.loc[df['trade_time'].isnull(), 'strategy_pct_adjust'] = df['strategy_pct']
        # 扣除卖出手续费
        df.loc[(df['trade_time'].shift(-1).notnull()) & (df['pos'] != 'empty'), 'strategy_pct_adjust'] = (1 + df[
            'strategy_pct']) * (1 - stamp_duty_rate) - 1
        # 空仓的日子，涨跌幅用0填充
        df['strategy_pct_adjust'].fillna(value=0.0, inplace=True)
        del df['strategy_pct'], df['style']

        df.reset_index(drop=True, inplace=True)
        # 计算净值
        df['coin1_net'] = df['coin1_close'] / df['coin1_close'][0]
        df['coin2_net'] = df['coin2_close'] / df['coin2_close'][0]
        df['strategy_net'] = (1 + df['strategy_pct_adjust']).cumprod()
        return df

    df1 = strategy1(coin1_df, coin2_df)
    df2 = strategy2(coin1_df, coin2_df)

    # 评估策略的好坏
    res = evaluate_investment(df1, 'strategy_net', 'strategy1', time='date')
    tmp_res = evaluate_investment(df2, 'strategy_net', 'strategy2', time='date')
    res[1] = tmp_res
    tmp_res = evaluate_investment(df1, 'coin1_net', coin1_name, time='date')
    res[2] = tmp_res
    tmp_res = evaluate_investment(df1, 'coin2_net', coin2_name, time='date')
    res[3] = tmp_res
    rev_res = res.T['累积净值']
    # if (rev_res[0] > rev_res[2] and rev_res[0] > rev_res[3]) or (rev_res[1] > rev_res[2] and rev_res[1] > rev_res[3]):
    if rev_res[1] > rev_res[2] and rev_res[1] > rev_res[3]:
        if rev_res[0] > rev_res[2] and rev_res[0] > rev_res[3]:
            print("strategy1 success %s %s" % (coin1_name, coin2_name))
        elif rev_res[1] > rev_res[2] and rev_res[1] > rev_res[3]:
            print("strategy2 success %s %s" % (coin1_name, coin2_name))
        print(res)
        global n_total_win
        n_total_win += 1
        res_json = res.to_dict()
        with open('result/label-%s-%s.json' % (coin1_name, coin2_name), 'w', encoding='utf-8') as f:
            json.dump(res_json, f, ensure_ascii=False)

        plt.plot(df1['date'], df1['strategy_net'], label='strategy1')
        plt.plot(df2['date'], df2['strategy_net'], label='strategy2')
        plt.plot(df1['date'], df1['coin1_net'], label=coin1_name)
        plt.plot(df1['date'], df1['coin2_net'], label=coin2_name)
        plt.legend(loc='upper left', title="%s与%s回测比较" % (coin1_name, coin2_name))
        plt.savefig('result/performance-%s-%s.jpg' % (coin1_name, coin2_name))
        plt.close()
        # plt.show()
    # print(res)
    # res_json = res.to_dict()
    # with open('result/label-%s-%s.json' % (coin1_name, coin2_name), 'w', encoding='utf-8') as f:
    #     json.dump(res_json, f, ensure_ascii=False)

    '''
    # 绘制图形
    plt.plot(df1['date'], df1['strategy_net'], label='strategy1')
    plt.plot(df2['date'], df2['strategy_net'], label='strategy2')
    plt.plot(df1['date'], df1['coin1_net'], label=coin1_name)
    plt.plot(df1['date'], df1['coin2_net'], label=coin2_name)
    plt.legend(loc='upper left', title="%s与%s回测比较" % (coin1_name, coin2_name))
    plt.savefig('result/performance-%s-%s.jpg' % (coin1_name, coin2_name))
    plt.close()
    # plt.show()
    '''


if __name__ == "__main__":
    info = pd.read_csv("data/index-fund-info.txt", delimiter=" ")
    for i in range(1, len(info), 1):
        for j in range(0, i, 1):
            print(i, j)
            name1 = 'day-k-%s-%s' % (info.loc[i, '指数名称'], info.loc[i, '指数代码'])
            name2 = 'day-k-%s-%s' % (info.loc[j, '指数名称'], info.loc[j, '指数代码'])
            fname1 = 'data/index-fund/%s.csv' % (name1)
            fname2 = 'data/index-fund/%s.csv' % (name2)
            run_model(fname1, fname2, name1, name2)
    print("n_total_win", n_total_win)
