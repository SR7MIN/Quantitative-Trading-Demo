import akshare as ak
from flask import Flask, render_template, request, session, redirect, url_for
from markupsafe import Markup
import pandas as pd
import os
from flask import redirect
import matplotlib.pyplot as plt

app=Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
#app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# @app.route('/')
# def index():
#     if 'username' in session:   # session 中有一个键值叫 username，说明这个 session 是登录状态
#         return f'Logged in as {session["username"]}'
#     return 'You are not logged in'

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         session['username'] = request.form['username']   # 将 username 存储在 session 中
#         return redirect(url_for('index'))
#     return '''
#         <form method="post">
#             <p><input type=text name=username>
#             <p><input type=submit value=Login>
#         </form>
#     '''

# @app.route('/logout')
# def logout():
#     # remove the username from the session if it's there
#     session.pop('username', None)
#     return redirect(url_for('index'))

def save_plot(stock_data, stock_code):
    try:
        plt.figure(figsize=(10, 5))
        plt.plot(stock_data['日期'], stock_data['收盘'])
        plt.title(f'Stock {stock_code} Closing Prices')
        plt.xlabel('Date')
        plt.ylabel('Closing Price')
        plt.xticks(rotation=45)
        plt.tight_layout()
        # 保存图表为PNG
        plot_filename = f'{stock_code}.png'
        plot_path = os.path.join('static', plot_filename)
        plt.savefig(plot_path)
        plt.close()
        return plot_path, True  # 返回文件路径和成功标志
    except Exception as e:
        return str(e), False  # 返回错误信息和失败标志


def get_stock_data(stock_code):
    try:
        stock_data = ak.stock_zh_a_spot_em()  # 获取A股市场的所有实时数据
        stock_data = stock_data[stock_data['代码'] == stock_code]
        if stock_data.empty:
            return "未找到股票代码对应的数据。"
        return stock_data
    except Exception as e:
        return f"获取数据失败: {str(e)}"

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/home/market-data', methods=['GET', 'POST'])
def market_data():
    if request.method == 'POST':
        stock_code = request.form.get('stock_code')
        data = get_stock_data(stock_code)
        if isinstance(data, pd.DataFrame):
            data_html = data.to_html(classes='table table-striped', border=0)
        else:
            data_html = data
        return render_template('stock_data.html', table=Markup(data_html), stock_code=stock_code)
    else:
        return render_template('market_data.html')

@app.route('/home/stock/<stock_code>')
def stock(stock_code):
    data = get_stock_data(stock_code)
    plot_status = ""
    if isinstance(data, pd.DataFrame):
        data_html = data.to_html(classes='table table-striped', border=0)
        plot_path, plot_success = save_plot(data, stock_code)
        if not plot_success:
            plot_status = "图表生成失败: " + plot_path  # 如果失败，plot_path会是错误信息
            plot_path = None  # 设置为None，确保不尝试加载图表
    else:
        data_html = data
        plot_path = None  # 如果数据获取失败，不显示图表
        plot_status = "数据获取失败"

    return render_template('stock_data.html', table=Markup(data_html), stock_code=stock_code, plot_path=plot_path, plot_status=plot_status)



@app.route('/home/trade-execution')
def trade_execution():
    return "<h1>交易执行</h1><p>这里进行交易执行。</p>"

@app.route('/home/historical-data')
def historical_data():
    return "<h1>历史数据</h1><p>这里显示历史数据。</p>"

@app.route('/home/risk-management')
def risk_management():
    return "<h1>风险管理</h1><p>这里进行风险管理。</p>"

if __name__ == '__main__':
    app.run(debug=True)
