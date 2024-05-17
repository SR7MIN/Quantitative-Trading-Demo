import os
import yaml
import pandas as pd
from flask import Flask, request, session, jsonify, Response, redirect, url_for
from flask_mysqldb import MySQL,MySQLdb
from markupsafe import Markup
from handle_stock_data import get_stock_data, save_plot
import json
from datetime import datetime
from flask_cors import CORS
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
CORS(app, resources={r'/*': {'origins': '*'}})
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
    

class User():
    def __init__(self, username, password, nickname):
        self.username = username
        self.password = password
        self.nickname = nickname
current_user = User('not logged in', 'no password', 'no nickname')

@app.route('/home/change-password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        userDetails = request.get_json()
        currentUser = User(userDetails['account'], userDetails['password'], "")
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        result = cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", 
                             (currentUser.username, currentUser.password))
        if result > 0:
            cur.execute("UPDATE users SET password = %s WHERE username = %s", (userDetails['newPassword'], currentUser.username))
            mysql.connection.commit()
            return jsonify({'status': 'success', 'message': 'Password changed successfully!'})
        else:
            return jsonify({'status': 'failed', 'message': 'Password change not successful'})
    return jsonify({'status': 'waiting for changing password'})

@app.route('/home/change-nickname', methods=['GET', 'POST'])
def change_nickname():
    if request.method == 'POST':
        userDetails = request.get_json()
        currentUser = User(userDetails['account'], userDetails['password'], "")
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        result = cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", 
                             (currentUser.username, currentUser.password))
        if result > 0:
            cur.execute("UPDATE users SET nickname = %s WHERE username = %s", (userDetails['newNickname'], currentUser.username))
            mysql.connection.commit()
            print("bbbbb")
            return jsonify({'status': 'success', 'message': 'Nickname changed successfully!'})
        
        else:
            return jsonify({'status': 'failed', 'message': 'Nickname change not successful'})
    return jsonify({'status': 'waiting for changing nickname'})

@app.route('/')
def index():
    return jsonify({'message': 'Welcome to the stock trading app'})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userDetails = request.get_json()
        # Create a new User object
        currentUser = User(userDetails['account'], userDetails['password'], "")
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        result = cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", 
                             (currentUser.username, currentUser.password))
        cur.execute("SELECT nickname FROM users WHERE username = %s", (currentUser.username,))
        result2 = cur.fetchone()
        print(result2)
        print("aaaaa")
        print(result2['nickname'])
        if result > 0:
            return jsonify({'status': 'success', 'nickname': result2['nickname']})
        else:
            return jsonify({'status': 'failed', 'message': 'Login not successful'})
    return jsonify({'status': 'waiting for login'})

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    print("enter signup")
    if request.method == 'POST':
        userDetails = request.get_json()
        currentUser = User(userDetails['account'], userDetails['password'], userDetails['name'])
        cur = mysql.connection.cursor()
        # Check if the username already exists
        cur.execute("SELECT * FROM users WHERE username = %s", [currentUser.username])
        if cur.fetchone():
            print("重复")
            return jsonify({'status': 'failed', 'message': 'Username already taken, please choose another one!'})   
        print("ccccc")
        cur.execute("INSERT INTO users(username, nickname, password) VALUES(%s, %s, %s)", (currentUser.username, currentUser.nickname, currentUser.password))
        mysql.connection.commit()
        cur.close()
        return jsonify({'status': 'success', 'username': currentUser.username})
        # return redirect(url_for('home'))
    return jsonify({'status': 'waiting for signing up'})

@app.route('/home')
def home():
    data = {'username':current_user.username, 'nickname':current_user.nickname}
    response = json.dumps(data, ensure_ascii=False)
    return Response(response, mimetype='application/json; charset=utf-8')

@app.route('/home/market-data', methods=['GET', 'POST'])
def market_data():
    if request.method == 'POST':
        print("Processing POST request")
        stock_code = request.form.get('stock_code')
        # Directly redirect to the stock information page
        return redirect(url_for('stock', stock_code=stock_code))
    else:
        return jsonify({'status': 'GET request processed'})

@app.route('/home/stock/<stock_code>')
def stock(stock_code):
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

    response = json.dumps({'data': data_json, 'plot_status': plot_status, 'plot_filename': plot_filename}, ensure_ascii=False)
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
