import requests
import datetime
import chinese_calendar
import numpy as np
import pandas as pd
import locale
import smtplib
from email.mime.text import MIMEText
import socket

locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')


def send(title):
    # 设置服务器所需信息
    # 163邮箱服务器地址
    mail_host = 'smtp.163.com'
    # 163用户名
    mail_user = '13352984589'
    # 密码(部分邮箱为授权码)
    mail_pass = 'ZKCBEYHRGNRHPDPY'
    # 邮件发送方邮箱地址
    sender = '13352984589@163.com'
    # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
    receivers = ['1317257555@qq.com']

    # 设置email信息
    # 邮件内容设置
    message = MIMEText('ceshiyoujian', 'plain', 'utf-8')
    # 邮件主题
    message['Subject'] = title
    # 发送方信息
    message['From'] = sender
    # 接受方信息
    message['To'] = receivers[0]

    # 登录并发送邮件
    try:
        smtpObj = smtplib.SMTP()
        # 连接到服务器
        smtpObj.connect(mail_host, 25)
        # 登录到服务器
        smtpObj.login(mail_user, mail_pass)
        # 发送
        smtpObj.sendmail(
            sender, receivers, message.as_string())
        # 退出
        smtpObj.quit()
        print('success')
    except smtplib.SMTPException as e:
        print('error', e)  # 打印错误


def get_host_name():
    return socket.gethostname()


def trim(stock_name: str):
    # print(d)
    return stock_name.strip('\r\n').replace(u'\u3000', u'').replace(u'\xa0', u'')


def get_today_trade_info(day_info):
    if chinese_calendar.is_holiday(day_info):
        raise Exception("is holiday, not in trade")
    day_format = "%s%s%s" % (day_info.strftime("%Y"), day_info.strftime("%m"), day_info.strftime("%d"))
    # print(day_format)
    url_ = 'https://sc.hkex.com.hk/TuniS/www.hkex.com.hk/chi/csm/DailyStat/data_tab_daily_%sc.js' % day_format
    trade_json = eval(requests.get(url_).text.split("=")[1])
    sh_trade = trade_json[0]
    sz_trade = trade_json[2]
    assert sh_trade['market'] == 'SSE Northbound' and sh_trade['id'] == 0
    assert sz_trade['market'] == 'SZSE Northbound' and sz_trade['id'] == 2
    # 总的交易额, 买入额, 卖出额
    sh_turnover_l = np.array([locale.atof(sh_trade["content"][0]["table"]["tr"][i]['td'][0][0]) for i in range(3)],
                             dtype=np.float)
    sz_turnover_l = np.array([locale.atof(sz_trade["content"][0]["table"]["tr"][i]['td'][0][0]) for i in range(3)],
                             dtype=np.float)
    total_turnover_l = np.add(sh_turnover_l, sz_turnover_l)
    print("买入额占总交易额比例", total_turnover_l[1] / total_turnover_l[0])

    n_show_item = len(sh_trade["content"][1]['table']['tr'])
    sh_item_l = [sh_trade["content"][1]["table"]["tr"][i]['td'][0] for i in range(n_show_item)]
    sh_data = pd.DataFrame(sh_item_l,
                           columns=['id', 'stock_code', 'stock_name', 'buy_turnover', 'sell_turnover',
                                    'total_turnover'])

    n_show_item = len(sz_trade["content"][1]['table']['tr'])
    sz_item_l = [sz_trade["content"][1]["table"]["tr"][i]['td'][0] for i in range(n_show_item)]
    sz_data = pd.DataFrame(sz_item_l,
                           columns=['id', 'stock_code', 'stock_name', 'buy_turnover', 'sell_turnover',
                                    'total_turnover'])
    merge_data = sh_data.append(sz_data, ignore_index=True)
    del merge_data['id']
    merge_data['stock_name'] = merge_data.apply(lambda x: trim(x['stock_name']), axis=1)
    merge_data['buy_turnover'] = merge_data.apply(lambda x: locale.atof(x['buy_turnover']), axis=1)
    merge_data['sell_turnover'] = merge_data.apply(lambda x: locale.atof(x['sell_turnover']), axis=1)
    merge_data['total_turnover'] = merge_data.apply(lambda x: locale.atof(x['total_turnover']), axis=1)

    merge_data['buy_percent'] = merge_data['buy_turnover'] / merge_data['total_turnover']
    merge_data = merge_data.sort_values(by='buy_percent')

    merge_data['buy_turnover'] = merge_data.apply(lambda x: '%.0f,000,000' % (x['buy_turnover'] / 1000000), axis=1)
    merge_data['sell_turnover'] = merge_data.apply(lambda x: '%.0f,000,000' % (x['sell_turnover'] / 1000000), axis=1)
    merge_data['total_turnover'] = merge_data.apply(lambda x: '%.0f,000,000' % (x['total_turnover'] / 1000000), axis=1)
    print(merge_data)


if __name__ == '__main__':
    get_today_trade_info(datetime.datetime(2021, 7, 6))
    # get_today_trade_info(datetime.datetime.today())
    # d = datetime.datetime.today()
    # # %Y - %m - %d
    # print(d.strftime("%m"))
    # print(d.day, d.month, d.year)
