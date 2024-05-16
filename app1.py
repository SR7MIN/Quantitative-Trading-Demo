import os
import yaml
import pandas as pd
from flask import Flask, request, session, jsonify, Response, redirect, url_for
from flask_mysqldb import MySQL
from markupsafe import Markup
from handle_stock_data import get_stock_data, save_plot
import json
from datetime import datetime

app = Flask(__name__)
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

# 定义一个辅助函数来转换日期类型
def default_converter(o):
    if isinstance(o, datetime):
        return o.isoformat()  # 或者任何其他格式化字符串

@app.route('/')
def index():
    return jsonify({'message': 'Welcome to the stock trading app'})

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
            return jsonify({'status': 'success', 'username': username})
        else:
            return jsonify({'status': 'failed', 'message': 'Login not successful'})
    return jsonify({'status': 'GET request - please provide credentials'})

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        userDetails = request.form
        username = userDetails['username']
        password = userDetails['password']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", [username])
        if cur.fetchone():
            return jsonify({'status': 'failed', 'message': 'Username already taken, please choose another one!'})
        
        cur.execute("INSERT INTO users(username, password) VALUES(%s, %s)", (username, password))
        mysql.connection.commit()
        cur.close()
        
        session['username'] = username
        return jsonify({'status': 'success', 'username': username})
    
    return jsonify({'status': 'GET request - please fill out the form'})

@app.route('/home/<username>')
def home(username):
    data = {'username': username}
    response = json.dumps(data, ensure_ascii=False)
    return Response(response, mimetype='application/json; charset=utf-8')

@app.route('/home/market-data', methods=['GET', 'POST'])
# def market_data():
#     username=session.get('username')
#     if request.method == 'POST':
#         stock_code = request.form.get('stock_code')
#         return jsonify({'status': 'POST request processed', 'stock_code': stock_code})
#     else:
#         return jsonify({'status': 'GET request processed'})

def market_data():
    username = session.get('username')
    if request.method == 'POST':
        print("Processing POST request")
        stock_code = request.form.get('stock_code')
        # Directly redirect to the stock information page
        return redirect(url_for('stock', stock_code=stock_code,username=username))
    else:
        return jsonify({'status': 'GET request processed'})
        


@app.route('/home/stock/<stock_code>')
def stock(stock_code):
    username = session.get('username')
    plot_status = ""
    data = get_stock_data(stock_code)
    if isinstance(data, pd.DataFrame):
        # 在 DataFrame 转字典之前转换所有日期类型的列
        for col in data.select_dtypes(include=[pd.Timestamp]):
            data[col] = data[col].apply(lambda x: x.isoformat() if pd.notnull(x) else None)
        
        data_dict = data.to_dict(orient='records')
        data_json = json.dumps(data_dict, ensure_ascii=False, default=default_converter)
        plot_filename, plot_success = save_plot(data, stock_code)
        if not plot_success:
            plot_status = "图表生成失败: " + plot_filename
            plot_filename = None
    else:
        data_json = '{}'
        plot_filename = None
        plot_status = "数据获取失败"

    response = json.dumps({'data': data_json, 'plot_status': plot_status, 'plot_filename': plot_filename, 'username': username}, ensure_ascii=False)
    return Response(response, mimetype='application/json; charset=utf-8')


@app.route('/home/trade-execution')
def trade_execution():
    return jsonify({'message': 'trade-execution'})

@app.route('/home/historical-data')
def historical_data():
    return jsonify({'message': 'historical-data'})

@app.route('/home/risk-management')
def risk_management():
    return jsonify({'message': 'risk-managemant'})

if __name__ == '__main__':
    app.run(debug=True)
