import baostock as bs
import pandas as pd
import akshare as ak
import datetime


def baostock_day_k(stock_code, start_date_obj, end_date_obj):
    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)

    start_str = start_date_obj.strftime('%Y-%m-%d')
    end_str = end_date_obj.strftime('%Y-%m-%d')

    rs = bs.query_history_k_data_plus(stock_code,
                                      # "date,open,high,low,close,volume",
                                      "date,open,high,low,close,volume, peTTM, pbMRQ",
                                      start_date=start_str,
                                      end_date=end_str,
                                      frequency="d", adjustflag="3")
    print('query_history_k_data_plus respond error_code:' + rs.error_code)
    print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)

    #### 打印结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)

    #### 登出系统 ####
    bs.logout()
    result['open'] = result['open'].astype('float64')
    result['high'] = result['high'].astype('float64')
    result['low'] = result['low'].astype('float64')
    result['close'] = result['close'].astype('float64')
    result['volume'] = result['volume'].astype('float64')
    result['peTTM'] = result['peTTM'].astype('float64')
    result['pbMRQ'] = result['pbMRQ'].astype('float64')
    return result


def akshare_day_k(stock_code, start_date_obj, end_date_obj):
    # result = ak.stock_zh_a_daily(symbol="sz000002", start_date="20101103", end_date="20201116")
    result = ak.stock_zh_a_daily(symbol=stock_code, start_date=start_date_obj.strftime('%Y%m%d'),
                                 end_date=end_date_obj.strftime('%Y%m%d'))
    result['date'] = result.apply(lambda x: x['date'].strftime("%Y-%m-%d"), axis=1)
    return result


def get_data(akcsv, baocsv, stock_name):
    akcsv['volume'] = akcsv.apply(lambda x: int(x['volume']), axis=1)
    akcsv['outstanding_share'] = akcsv.apply(lambda x: int(x['outstanding_share']), axis=1)
    akcsv['mkt_capital'] = akcsv['close'] * akcsv['outstanding_share']
    akcsv.drop(columns=['open', 'high', 'low', 'volume', 'close', 'turnover', 'outstanding_share'], inplace=True)

    baocsv.drop(columns=['open', 'high', 'low'], inplace=True)
    baocsv.rename(columns={'close': 'price', 'peTTM': 'price_earning_ratio', 'pbMRQ': 'price_book_ratio'}, inplace=True)

    daykcsv = pd.merge(left=akcsv, left_on=['date'],
                       right=baocsv, right_on=['date'], how='inner')
    daykcsv = daykcsv.reindex(
        columns=['date', 'price', 'volume', 'price_earning_ratio', 'price_book_ratio', 'mkt_capital'])

    def get_dateid(x):
        # print(x)
        date = datetime.datetime.strptime(x['date'], '%Y-%m-%d')
        # date = x['date']
        return date.strftime("%Y-%m")

    daykcsv['dateid'] = daykcsv.apply(get_dateid, axis=1)

    mongbobj = daykcsv.groupby(['dateid'], as_index=False)
    month_last = mongbobj[['price', 'price_book_ratio', 'mkt_capital', 'price_earning_ratio']].last()
    month_sum = mongbobj['volume'].sum()
    month_std = mongbobj['price'].std()
    month_std.rename(columns={'price': 'day_price_std'}, inplace=True)

    monthkcsv = pd.merge(left=month_last, left_on=['dateid'], left_index=False, right=month_sum, right_on=['dateid'],
                         right_index=False)
    monthkcsv = pd.merge(left=monthkcsv, left_on=['dateid'], left_index=False, right=month_std, right_on=['dateid'],
                         right_index=False)
    monthkcsv['price_pct'] = monthkcsv['price'].pct_change(periods=1)
    monthkcsv.rename(columns={'price_pct': 'price_rise_rate', 'dateid': 'date'}, inplace=True)

    monthkcsv['price'] = monthkcsv['price'] / monthkcsv['price'].max()
    monthkcsv['price_book_ratio'] = monthkcsv['price_book_ratio'] / monthkcsv['price_book_ratio'].max()
    monthkcsv['mkt_capital'] = monthkcsv['mkt_capital'] / monthkcsv['mkt_capital'].max()
    monthkcsv['price_earning_ratio'] = monthkcsv['price_earning_ratio'] / monthkcsv['price_earning_ratio'].max()
    monthkcsv['volume'] = monthkcsv['volume'] / monthkcsv['volume'].max()

    monthkcsv.to_csv("data/feature-%s.csv" % stock_name, index=False)
    print(monthkcsv)


if __name__ == '__main__':
    stock_m = {
        '浦发银行': 'sh.600000',
        '东风汽车': 'sh.600006',
        '中国国贸': 'sh.600007',
        '上海机场': 'sh.600009',
        '包钢股份': 'sh.600010'
    }
    start_date = datetime.datetime(year=2005, month=1, day=1)
    end_date = datetime.datetime.now()
    for name in stock_m:
        code = stock_m[name]
        baocsv = baostock_day_k(code, start_date, end_date)
        akcode = code.split('.')[0] + code.split('.')[1]
        akcsv = akshare_day_k(akcode, start_date, end_date)
        get_data(akcsv, baocsv, name)
