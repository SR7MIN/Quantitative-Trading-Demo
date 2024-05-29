import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')# don't delete it!!!
import datetime
import akshare as ak
import os
import time
import pytz
import json
import pandas as pd

def save_plot(stock_data, stock_code):
    try:
        plt.figure(figsize=(10, 5))
        plt.plot(stock_data['日期'], stock_data['收盘'])
        plt.title(f'Stock {stock_code} Closing Prices')
        plt.xlabel('Date')
        plt.ylabel('Closing Price')
        plt.xticks(rotation=0)
        plt.tight_layout()
        plt.grid()
        # 使用绝对路径来避免目录问题
        base_dir = os.path.dirname(os.path.abspath(__file__))
        plot_filename = f'{stock_code}.png'
        plot_path = os.path.join(base_dir, 'static', plot_filename)
        
        plt.savefig(plot_path)
        plt.close()
        print(f'Plot saved to {plot_path}')
        return plot_filename, True 
    except Exception as e:
        return str(e), False 


def get_stock_data(stock_code):
    stock_code=str(stock_code)
    try:
        end_date = datetime.datetime.today().strftime('%Y%m%d')  
        start_date = (datetime.datetime.today() - datetime.timedelta(days=365)).strftime('%Y%m%d') 
        if len(stock_code) == 5:
            stock_data = ak.stock_hk_hist(symbol=stock_code, period="daily", start_date=start_date, end_date=end_date, adjust="qfq")
        else:
            stock_data = ak.stock_zh_a_hist(symbol=stock_code, period="daily", start_date=start_date, end_date=end_date, adjust="qfq")
        return stock_data
    except Exception as e:
        return f"获取数据失败: {str(e)}"
    
def get_stock_current_price(stock_code, place='cn'):
    stock_code=str(stock_code)
    print("get_stock_current_price, stock_code:",stock_code)
    # 判断stock_code是5位还是6位
    if len(stock_code) == 5:
        place = 'hk'
    print("aaaaa")
    print('place',place)
    try:
        if place == 'cn':
            print("cn")
            stock_info = ak.stock_zh_a_spot_em()
            current_price = stock_info[stock_info['代码'] == stock_code]['最新价'].values[0]
        elif place == 'hk':
            print('hk')
            stock_info = ak.stock_hk_spot_em()
            current_price = stock_info[stock_info['代码'] == stock_code]['最新价'].values[0]
        return current_price
    except Exception as e:
        print(e)
        print("异常")
        return 0

def get_stock_all_info(stock_code, place='cn'):
    stock_code=str(stock_code)
    if len(stock_code) == 5:
        place = 'hk'
    try:
        if place == 'cn':
            stock_info = ak.stock_zh_a_spot_em()
            stock_all_info = stock_info[stock_info['代码'] == stock_code]
        elif place == 'hk':
            stock_info = ak.stock_hk_spot_em()
            stock_all_info = stock_info[stock_info['代码'] == stock_code]
        return stock_all_info
    except Exception as e:
        return 0


def get_stock_name(stock_code,place='cn'):
    stock_code=str(stock_code)
    if len(stock_code) == 5:
        place = 'hk'
    try:
        if place == 'cn':
            stock_info = ak.stock_zh_a_spot_em()
            stock_name = stock_info[stock_info['代码'] == stock_code]['名称'].values[0]
        elif place == 'hk':
            stock_info = ak.stock_hk_spot_em()
            stock_name = stock_info[stock_info['代码'] == stock_code]['名称'].values[0]
        print(stock_name)
        a={}
        a['stock_name']=stock_name
        print(a)
        return stock_name

    except Exception as e:
        return 0


def get_beijing_time():
    timestamp = time.time()
    utc_time = datetime.datetime.utcfromtimestamp(timestamp)
    beijing_tz = pytz.timezone('Asia/Shanghai')
    beijing_time = utc_time.replace(tzinfo=pytz.utc).astimezone(beijing_tz)
    formatted_beijing_time = beijing_time.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_beijing_time

def get_yesterday_price(stock_code):
    stock_code=str(stock_code)
    try:
        start_date = (datetime.datetime.today() - pd.Timedelta(days=1)).strftime('%Y%m%d')
        if len(stock_code) == 5:
            stock_data = ak.stock_hk_hist(symbol=stock_code, period="daily", start_date=start_date, end_date=start_date, adjust="qfq")['收盘'].values[0]
        else:
            stock_data = ak.stock_zh_a_hist(symbol=stock_code, period="daily", start_date=start_date, end_date=start_date, adjust="qfq")['收盘'].values[0]
        return stock_data
    except Exception as e:
        return f"获取数据失败: {str(e)}"
    