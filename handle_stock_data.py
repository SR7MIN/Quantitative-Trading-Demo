import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')# don't delete it!!!
import datetime
import akshare as ak
import os
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
    try:
        end_date = datetime.datetime.today().strftime('%Y%m%d')  
        start_date = (datetime.datetime.today() - datetime.timedelta(days=365)).strftime('%Y%m%d') 
        stock_data = ak.stock_zh_a_hist(symbol=stock_code, period="daily", start_date=start_date, end_date=end_date, adjust="qfq")
        return stock_data
    except Exception as e:
        return f"获取数据失败: {str(e)}"
    

def get_stock_current_price(stock_code, place='cn'):
    stock_code=str(stock_code)
    # 判断stock_code是5位还是6位
    if len(stock_code) == 5:
        place = 'hk'
    try:
        if place == 'cn':
            stock_info = ak.stock_zh_a_spot_em()
            current_price = stock_info[stock_info['代码'] == stock_code]['最新价'].values[0]
        elif place == 'hk':
            stock_info = ak.stock_hk_spot_em()
            current_price = stock_info[stock_info['代码'] == stock_code]['最新价'].values[0]
        return current_price
    except Exception as e:
        return 0
    # stock_code=str(stock_code)
    # stock_info = ak.stock_zh_a_spot_em()
    # current_price = stock_info[stock_info['代码'] == stock_code]['最新价'].values[0]
    # return current_price

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
