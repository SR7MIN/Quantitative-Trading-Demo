import os
import yaml
import pandas as pd
from flask import Flask, request, session, jsonify, Response, redirect, url_for, send_file
from flask_mysqldb import MySQL,MySQLdb
from markupsafe import Markup
from handle_stock_data import get_stock_data, save_plot, get_stock_current_price, get_stock_name, get_beijing_time, get_stock_all_info
import json
from datetime import datetime
from flask_cors import CORS
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
CORS(app, resources={r'/*': {'origins': '*'}}) # 不要修改此行！
# CORS(app)
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
        print(result2['nickname'])
        if result > 0:
            #return jsonify({'status': 'success', 'nickname': result2['nickname']})
            #返回status nickname history balance stocks_held
            cur.execute("SELECT history FROM users WHERE username = %s", (currentUser.username,))
            result3 = cur.fetchone()
            history=result3['history']
            cur.execute("SELECT balance FROM users WHERE username = %s", (currentUser.username,))
            result4 = cur.fetchone()
            balance=result4['balance']
            cur.execute("SELECT stocks_held FROM users WHERE username = %s", (currentUser.username,))
            result5 = cur.fetchone()
            stocks_held=result5['stocks_held']
            stocks_held=json.loads(stocks_held)
            stocks_info={}
            for stock_code in stocks_held:
                price=get_stock_current_price(stock_code)
                stocks_info[stock_code]=[get_stock_name(stock_code), price, stocks_held[stock_code], price*stocks_held[stock_code]]
            if history is None:
                history=[]
            else:
                history=json.loads(history)
            return jsonify({'status': 'success', 'nickname': result2['nickname'], 'history': history, 'balance': balance, 'stocks_info': stocks_info})
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

@app.route('/home/CNstock', methods=['GET', 'POST']) #从前端获取股票代码，在json中的key是"code"
def CNstock():
    if request.method == 'POST':
        stock_code = request.get_json()['code']
        stock_data = get_stock_data(stock_code)
        print(stock_data)
        print(type(stock_data))
        if isinstance(stock_data, pd.DataFrame):
            # 将DataFrame转换为字典
            data_dict = stock_data.to_dict(orient='records')
            all_info = get_stock_all_info(stock_code)
            return jsonify({'status': 'succeed', 'data': data_dict, 'stock_name': get_stock_name(stock_code), 'all_info': all_info.to_dict(orient='records')})
            # return send_file(output, mimetype='image/png')
        else:
            return jsonify({'status': 'failed'})
    return jsonify({'status': 'waiting for stock code'})

@app.route('/home/HKstock', methods=['GET', 'POST']) #从前端获取股票代码，在json中的key是"code"
def HKstock():
    if request.method == 'POST':
        stock_code = request.get_json()['code']
        stock_data = get_stock_data(stock_code)
        print(stock_data)
        print(type(stock_data))
        if isinstance(stock_data, pd.DataFrame):
            # 将DataFrame转换为字典
            data_dict = stock_data.to_dict(orient='records')
            all_info = get_stock_all_info(stock_code)
            return jsonify({'status': 'succeed', 'data': data_dict, 'stock_name': get_stock_name(stock_code), 'all_info': all_info.to_dict(orient='records')})
            # return send_file(output, mimetype='image/png')
        else:
            return jsonify({'status': 'failed'})
    return jsonify({'status': 'waiting for stock code'})

@app.route('/home/recharge', methods=['GET', 'POST']) # 充值
def recharge():
    if request.method == 'POST':
        userDetails = request.get_json()
        sum=int(userDetails['sum'])
        sum=int(userDetails['sum'])
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
            return jsonify({'status': 'success', "balance": balance})
    return jsonify({'status': 'waiting for recharging'})

@app.route('/home/buy', methods=['GET', 'POST']) # 买入
def buy(): #交易执行 获取的json格式为{"code":int, "num":int ,"account":""}
    if request.method == 'POST':
        print("buy")
        userDetails = request.get_json()
        stock_code=userDetails['code']
        print(type(stock_code))
        num=int(userDetails['num'])
        print(type(num))
        account=userDetails['account']
        place=userDetails['place']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        result = cur.execute("SELECT * FROM users WHERE username = %s", (account,))
        if result > 0:#接下来要select balance and stocks_held 前者是float 后者是json
            cur.execute("SELECT balance FROM users WHERE username = %s", (account,))
            result2 = cur.fetchone()
            balance=result2['balance']
            cur.execute("SELECT stocks_held FROM users WHERE username = %s", (account,))
            result3 = cur.fetchone()
            stocks_held=result3['stocks_held']
            price=get_stock_current_price(stock_code,place)
            if price==0:
                print("股票代码未找到")
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
                # update history
                cur.execute("SELECT history FROM users WHERE username = %s", (account,))
                result4 = cur.fetchone()
                history=result4['history']
                if history is None:
                    history=[]
                else:
                    history=json.loads(history)
                history.append({'type': 'buy', 'stock_code': stock_code, 'stock_name': get_stock_name(stock_code), 'num': num, 'price': price, 'time': get_beijing_time()})
                cur.execute("UPDATE users SET history = %s WHERE username = %s", (json.dumps(history), account))
                mysql.connection.commit()
                return jsonify({'status': 'success', 'balance':balance})
            else:
                print("余额不足！")
                return jsonify({'status': 'failed', 'message': 'Insufficient balance'})
    return jsonify({'status': 'waiting for trade execution'})

@app.route('/home/sell', methods=['GET', 'POST']) # 卖出
def sell():
    if request.method == 'POST':
        userDetails = request.get_json()
        stock_code=userDetails['code']
        print("/home/sell, stock_code",stock_code)
        num=int(userDetails['num'])
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
            print("price:",price)
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
                        # update history
                        cur.execute("SELECT history FROM users WHERE username = %s", (account,))
                        result4 = cur.fetchone()
                        history=result4['history']
                        if history is None:
                            history=[]
                        else:
                            history=json.loads(history)
                        history.append({'type': 'sell', 'stock_code': stock_code, 'stock_name': get_stock_name(stock_code), 'num': num, 'price': price, 'time': get_beijing_time()})
                        cur.execute("UPDATE users SET history = %s WHERE username = %s", (json.dumps(history), account))
                        mysql.connection.commit()
                        return jsonify({'status': 'success', 'balance':balance})
                    else:
                        return jsonify({'status': 'failed', 'message': 'Insufficient stocks held'})
                else:
                    return jsonify({'status': 'failed', 'message': 'No stocks held'})
    return jsonify({'status': 'waiting for trade execution'})

@app.route('/home/stock-holding', methods=['GET', 'POST']) # 查看持仓,返回{股票代码:[股票数量，单价，总价值]}
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
                    stocks_info[stock_code]=[get_stock_name(stock_code), price, stocks_held[stock_code], price*stocks_held[stock_code]]
                    print("stocks_info:",stocks_info)
                    print("code: ", stocks_info[stock_code])
                return jsonify({'status': 'success', 'stocks_info': stocks_info})
    return jsonify({'status': 'waiting for getting stock holding'})

@app.route('/home/history', methods=['GET', 'POST']) # 查看历史交易记录
def history():
    if request.method == 'POST':
        userDetails = request.get_json()
        account=userDetails['account']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        result = cur.execute("SELECT * FROM users WHERE username = %s", (account,))
        if result > 0:
            cur.execute("SELECT history FROM users WHERE username = %s", (account,))
            result2 = cur.fetchone()
            history=result2['history']
            if history is None:
                return jsonify({'status': 'failed', 'message': 'No history'})
            else:
                history=json.loads(history)
                print("bbbb:",history)
                return jsonify({'status': 'success', 'history': history})
    return jsonify({'status': 'waiting for getting history'})

@app.route('/home/topFive', methods=['GET', 'POST']) # 查看持股最多的前五名股票
def topFive():
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
                    stocks_info[stock_code]=[get_stock_name(stock_code), price, stocks_held[stock_code], price*stocks_held[stock_code]]
                # 按数量排序
                #sorted_stocks_info=sorted(stocks_info.items(), key=lambda x: x[1][2], reverse=True)
                # 按金额排序
                sorted_stocks_info=sorted(stocks_info.items(), key=lambda x: x[1][3], reverse=True)
                # 如果持仓股票种类少于5种，返回全部
                print("type: ", type(sorted_stocks_info))
                print(sorted_stocks_info)
                if len(sorted_stocks_info)<=5:
                    return jsonify({'status': 'success', 'topFive': sorted_stocks_info})
                else:
                    return jsonify({'status': 'success', 'topFive': sorted_stocks_info[:5]})
    return jsonify({'status': 'waiting for getting topFive'})

@app.route('/home/price', methods=['GET', 'POST']) # 查看当前股票价格
def price():
    if request.method == 'POST':
        userDetails = request.get_json()
        stock_code=userDetails['code']
        price=get_stock_current_price(stock_code)
        if price==0:
            return jsonify({'status': 'failed', 'message': 'Stock code not found'})
        return jsonify({'status': 'success', 'price': price})
    return jsonify({'status': 'waiting for getting price'})

@app.route('/home/total', methods=['GET', 'POST'])
def total():
    if request.method == 'POST':
        userDetails = request.get_json()
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
            if stocks_held is None:
                return jsonify({'status': 'success', 'total': balance})
            else:
                stocks_held=json.loads(stocks_held)
                total=balance
                for stock_code in stocks_held:
                    price=get_stock_current_price(stock_code)
                    total+=price*stocks_held[stock_code]
                return jsonify({'status': 'success', 'total': total})
    return jsonify({'status': 'waiting for getting total'})
           
@app.route('/home/risk-management')
def risk_management():
    return jsonify({'message': 'risk-managemant'})

if __name__ == '__main__':
    app.run(debug=True)