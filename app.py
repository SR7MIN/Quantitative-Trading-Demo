import akshare as ak
from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL
from markupsafe import Markup
import pandas as pd
import os
import matplotlib.pyplot as plt
import datetime
import yaml
from handle_stock_data import get_stock_data, save_plot

app=Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, 'db.yaml')
with open(db_path, 'r') as file:
    db = yaml.load(file, Loader=yaml.FullLoader)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userDetails = request.form
        username = userDetails['username']
        password = userDetails['password']
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        if result > 0:
            session['username'] = username
            return redirect(url_for('home', username=username))
        else:
            return 'Login not successful'
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        userDetails = request.form
        username = userDetails['username']
        password = userDetails['password']
        
        cur = mysql.connection.cursor()
        # 检查用户名是否已存在
        cur.execute("SELECT * FROM users WHERE username = %s", [username])
        if cur.fetchone():
            # 如果用户名已存在，返回错误消息
            flash('Username already taken, please choose another one!')
            return render_template('signup.html')
        
        # 如果用户名不存在，插入新用户
        cur.execute("INSERT INTO users(username, password) VALUES(%s, %s)", (username, password))
        mysql.connection.commit()
        cur.close()
        
        session['username'] = username
        return redirect(url_for('home', username=username))
    
    return render_template('signup.html')

@app.route('/home/<username>')
def home(username):
    return render_template('home.html', username=username)

@app.route('/home/market-data', methods=['GET', 'POST'])
def market_data():
    username = session.get('username')
    if request.method == 'POST':
        print("Processing POST request")
        stock_code = request.form.get('stock_code')
        # Directly redirect to the stock information page
        return redirect(url_for('stock', stock_code=stock_code,username=username))
    else:
        print("Processing GET request")
        return render_template('market_data.html',username=username)
@app.route('/home/stock/<stock_code>')
def stock(stock_code):
    username = session.get('username')
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
    return render_template('stock_data.html', table=Markup(data_html), stock_code=stock_code, plot_filename=plot_filename, plot_status=plot_status, username=username)

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
