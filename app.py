import akshare as ak
from flask import Flask, render_template, request, session, redirect, url_for
from markupsafe import Markup
import pandas as pd
import os
from flask import redirect
import matplotlib.pyplot as plt
import datetime

from handle_stock_data import get_stock_data, save_plot

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



@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/home/market-data', methods=['GET', 'POST'])
def market_data():
    if request.method == 'POST':
        print("Processing POST request")
        stock_code = request.form.get('stock_code')
        # Directly redirect to the stock information page
        return redirect(url_for('stock', stock_code=stock_code))
    else:
        print("Processing GET request")
        return render_template('market_data.html')

@app.route('/home/stock/<stock_code>')
def stock(stock_code):
    plot_status = ""  # Initialize plot_status to a default value
    data = get_stock_data(stock_code)
    print('Processing stock data retrieval')
    if isinstance(data, pd.DataFrame):
        print('Data retrieved successfully')
        data_html = data.to_html(classes='table table-striped', border=0)
        plot_filename, plot_success = save_plot(data, stock_code)
        if not plot_success:
            plot_status = "图表生成失败: " + plot_filename  # Update plot_status if plot generation fails
            plot_filename = None  # Ensure no attempt to load the plot
    else:
        print('Data retrieval failed')
        data_html = data
        plot_filename = None
        plot_status = "数据获取失败"  # Update plot_status if data retrieval fails

    print(plot_filename)
    return render_template('stock_data.html', table=Markup(data_html), stock_code=stock_code, plot_filename=plot_filename, plot_status=plot_status)




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
