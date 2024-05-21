import os
import yaml
import pandas as pd
from flask import Flask, request, session, jsonify, Response, redirect, url_for, send_file
from flask_mysqldb import MySQL,MySQLdb
from markupsafe import Markup
from handle_stock_data import get_stock_data, save_plot, get_stock_current_price
import json
from datetime import datetime
from flask_cors import CORS
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
CORS(app, resources={r'/*': {'origins': '*'}}) # 不要修改此行！
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
            return jsonify({'status': 'success', 'message': 'Nickname changed successfully!'})
        else:
            return jsonify({'status': 'failed', 'message': 'Nickname change not successful'})
    return jsonify({'status': 'waiting for changing nickname'})

@app.route('/home/stock', methods=['GET', 'POST']) #从前端获取股票代码，在json中的key是"code"
def stock():
    if request.method == 'POST':
        stock_code = request.get_json()['code']
        stock_data = get_stock_data(stock_code)
        print(stock_data)
        print(type(stock_data))
        if isinstance(stock_data, pd.DataFrame):
            plt.figure(figsize=(10, 5))
            plt.plot(stock_data['日期'], stock_data['收盘'])
            plt.title(f'Stock {stock_code} Closing Prices')
            plt.xlabel('Date')
            plt.ylabel('Closing Price')
            plt.xticks(rotation=0)
            plt.tight_layout()
            plt.grid()
            output=io.BytesIO()
            plt.savefig(output, format='png')
            output.seek(0)
            print("66666")
            # 将图像转换为Base64编码的字符串
            image_string = base64.b64encode(output.read()).decode('utf-8')
            # 将DataFrame转换为字典
            data_dict = stock_data.to_dict(orient='records')
            # 将图像和数据一起作为JSON发送
            return jsonify({'status': 'succeed','image': image_string, 'data': data_dict})
            # return send_file(output, mimetype='image/png')
        else:
            return jsonify({'status': 'failed'})
    return jsonify({'status': 'waiting for stock code'})

@app.route('/home/recharge', methods=['GET', 'POST'])#充值
def recharge():
    if request.method == 'POST':
        userDetails = request.get_json()
        sum=userDetails['sum']
        account=userDetails['account']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        result = cur.execute("SELECT * FROM users WHERE username = %s", (account,))
        if result > 0:
            cur.execute("SELECT balance FROM users WHERE username = %s", (account,))
            result2 = cur.fetchone()
            balance=result2['balance']
            balance+=sum
            cur.execute("UPDATE users SET balance = %s WHERE username = %s", (balance, account))
            mysql.connection.commit()
            return jsonify({'status': 'success'})
    return jsonify({'status': 'waiting for recharging'})

@app.route('/home/buy', methods=['GET', 'POST'])#买入
def buy(): #交易执行 获取的json格式为{"code":int, "num":int ,"account":""}
    if request.method == 'POST':
        userDetails = request.get_json()
        stock_code=userDetails['code']
        num=userDetails['num']
        account=userDetails['account']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        result = cur.execute("SELECT * FROM users WHERE username = %s", (account,))
        if result > 0:#接下来要select balance and stocks_held 前者是float 后者是json
            cur.execute("SELECT balance FROM users WHERE username = %s", (account,))
            result2 = cur.fetchone()
            balance=result2['balance']
            cur.execute("SELECT stocks_held FROM users WHERE username = %s", (account,))
            result3 = cur.fetchone()
            stocks_held=result3['stocks_held']
            price=get_stock_current_price(stock_code)
            if price==0:
                return jsonify({'status': 'failed', 'message': 'Stock code not found'})
            if balance>=num*price:
                balance-=num*price
                if stocks_held is None:
                    stocks_held={}
                else:
                    stocks_held=json.loads(stocks_held)
                if stock_code in stocks_held:
                    stocks_held[stock_code]+=num
                else:
                    stocks_held[stock_code]=num
                cur.execute("UPDATE users SET balance = %s WHERE username = %s", (balance, account))
                cur.execute("UPDATE users SET stocks_held = %s WHERE username = %s", (json.dumps(stocks_held), account))
                mysql.connection.commit()
                return jsonify({'status': 'success'})
            else:
                return jsonify({'status': 'failed', 'message': 'Insufficient balance'})
    return jsonify({'status': 'waiting for trade execution'})

@app.route('/home/sell', methods=['GET', 'POST'])#卖出
def sell():
    if request.method == 'POST':
        userDetails = request.get_json()
        stock_code=userDetails['code']
        num=userDetails['num']
        account=userDetails['account']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        result = cur.execute("SELECT * FROM users WHERE username = %s", (account,))
        if result > 0:
            cur.execute("SELECT balance FROM users WHERE username = %s", (account,))
            result2 = cur.fetchone()
            balance=result2['balance']
            cur.execute("SELECT stocks_held FROM users WHERE username = %s", (account,))
            result3 = cur.fetchone()
            stocks_held=result3['stocks_held']
            price=get_stock_current_price(stock_code)
            if price==0:
                return jsonify({'status': 'failed', 'message': 'Stock code not found'})
            if stocks_held is None:
                return jsonify({'status': 'failed', 'message': 'No stocks held'})
            else:
                stocks_held=json.loads(stocks_held)
                if stock_code in stocks_held:
                    if stocks_held[stock_code]>=num:
                        balance+=num*price
                        stocks_held[stock_code]-=num
                        if stocks_held[stock_code]==0:
                            del stocks_held[stock_code]
                        cur.execute("UPDATE users SET balance = %s WHERE username = %s", (balance, account))
                        cur.execute("UPDATE users SET stocks_held = %s WHERE username = %s", (json.dumps(stocks_held), account))
                        mysql.connection.commit()
                        return jsonify({'status': 'success'})
                    else:
                        return jsonify({'status': 'failed', 'message': 'Insufficient stocks held'})
                else:
                    return jsonify({'status': 'failed', 'message': 'No stocks held'})
    return jsonify({'status': 'waiting for trade execution'})

@app.route('/home/stock-holding', methods=['GET', 'POST'])#查看持仓,返回{股票代码:[股票数量，单价，总价值]}
def stock_holding():
    if request.method == 'POST':
        userDetails = request.get_json()
        account=userDetails['account']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        result = cur.execute("SELECT * FROM users WHERE username = %s", (account,))
        if result > 0:
            cur.execute("SELECT stocks_held FROM users WHERE username = %s", (account,))
            result2 = cur.fetchone()
            stocks_held=result2['stocks_held']
            if stocks_held is None:
                return jsonify({'status': 'failed', 'message': 'No stocks held'})
            else:
                stocks_held=json.loads(stocks_held)
                stocks_info={}
                for stock_code in stocks_held:
                    price=get_stock_current_price(stock_code)
                    stocks_info[stock_code]=[price, stocks_held[stock_code], price*stocks_held[stock_code]]
                return jsonify({'status': 'success', 'stocks_info': stocks_info})
    return jsonify({'status': 'waiting for getting stock holding'})


@app.route('/home/historical-data')
def historical_data():
    return jsonify({'message': 'historical-data'})

@app.route('/home/risk-management')
def risk_management():
    return jsonify({'message': 'risk-managemant'})

if __name__ == '__main__':
    app.run(debug=True)
