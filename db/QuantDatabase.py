import pymysql
from pymysql.constants import CLIENT

class QuantDatabase:
    def __init__(self, host, user, password, db_name):
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def connect(self):
        """连接到MySQL数据库"""
        self.connection = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            db=self.db_name,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            client_flag=CLIENT.MULTI_STATEMENTS
        )
        self.cursor = self.connection.cursor()

    def execute_query(self, sql, params=None):
        """执行SQL查询并返回结果"""
        if params:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)
        return self.cursor.fetchall()

    def execute_command(self, sql, params=None):
        """执行SQL命令并提交更改"""
        if params:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)
        self.connection.commit()

    def fetch_data(self, sql):
        """获取数据"""
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def insert_data(self, table, data):
        """向指定表插入数据"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        sql = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
        self.execute_command(sql, data.values())

    def update_data(self, table, data, condition):
        """更新指定表的数据"""
        updates = ', '.join([f"{k}=%s" for k in data])
        sql = f'UPDATE {table} SET {updates} WHERE {condition}'
        self.execute_command(sql, list(data.values()))

    def close(self):
        """关闭数据库连接"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

# 使用示例
if __name__ == '__main__':
    db = QuantDatabase(host='localhost', user='root', password='password', db_name='quant_db')
    db.connect()

    # 插入数据示例
    db.insert_data('stocks', {'code': 'AAPL', 'price': 150.0, 'date': '2024-04-11'})

    # 查询数据示例
    data = db.fetch_data('SELECT * FROM stocks WHERE code=%s', ('AAPL',))
    for record in data:
        print(record)

    db.close()