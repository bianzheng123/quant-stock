import akshare as ak
import datetime


def get_day_k(stock_code, stock_name, start_date, end_date):
    # result = ak.stock_zh_a_daily(symbol="sz000002", start_date="20101103", end_date="20201116")
    result = ak.stock_zh_a_daily(symbol=stock_code, start_date=start_date, end_date=end_date)
    result.to_csv("data/akshare-day-k-%s.csv" % stock_name, index=False)
    return result


if __name__ == '__main__':
    stock_m = {
        '浦发银行': 'sh600000',
        # '东风汽车': 'sh600006',
        # '中国国贸': 'sh600007',
        # '上海机场': 'sh600009',
        # '包钢股份': 'sh600010'
    }
    now_string = datetime.datetime.now().strftime('%Y%m%d')
    for tmp in stock_m:
        get_day_k(stock_code=stock_m[tmp], stock_name=tmp, start_date='19990101', end_date=now_string)
