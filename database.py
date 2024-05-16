#pip install sqlite3
import sqlite3
from sqlite3 import Error

# 数据库文件路径
db_file = './qtdb.db'

# SQL语句，用于创建四个表
create_tables_sql = """
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS Users (
    User_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT NOT NULL UNIQUE,
    Password_Hash TEXT NOT NULL,
    Email TEXT NOT NULL UNIQUE,
    Creation_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Last_Login_Date TIMESTAMP DEFAULT NULL
);
CREATE TABLE IF NOT EXISTS Strategies (
    Strategy_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    User_ID INTEGER,
    Strategy_Name TEXT NOT NULL,
    Strategy_Description TEXT,
    Strategy_Code TEXT NOT NULL,
    Parameters TEXT,
    Creation_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS Orders (
    Order_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    User_ID INTEGER,
    Strategy_ID INTEGER,
    Trading_Pair TEXT NOT NULL,
    Order_Type TEXT NOT NULL,
    Order_Status TEXT NOT NULL,
    Creation_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Completion_Date TIMESTAMP,
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID) ON DELETE CASCADE,
    FOREIGN KEY (Strategy_ID) REFERENCES Strategies(Strategy_ID) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS Risk_Control_Rules (
    Rule_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    User_ID INTEGER,
    Strategy_ID INTEGER,
    Stop_Loss REAL,
    Take_Profit REAL,
    Position_Limit REAL,
    Leverage_Level INTEGER,
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID) ON DELETE CASCADE,
    FOREIGN KEY (Strategy_ID) REFERENCES Strategies(Strategy_ID) ON DELETE CASCADE
);
COMMIT;
"""

def create_connection(db_file):
    """Create a database connection to a SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

def close_connection(conn):
    """Close the database connection."""
    if conn:
        conn.close()

def db_connection():
    return sqlite3.connect(db_file)

def get_cursor(connection):
    return connection.cursor()


def insert_user(username, password_hash, email):
    """
    Inserts a user into the Users table.

    Args:
        username (str): The username of the user.
        password_hash (str): The hashed password of the user.
        email (str): The email address of the user.

    Returns:
        int: The ID of the inserted row.

    Raises:
        Error: If there is an error inserting the data.

    """
    query = "INSERT INTO Users (Username, Password_Hash, Email) VALUES (?, ?, ?)"
    try:
        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute(query, (username, password_hash, email))
        connection.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"Error inserting data: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

def get_user(user_id):
    """
    Retrieves a user from the Users table.

    Args:
        user_id (int): The ID of the user.

    Returns:
        tuple: The user data as a tuple.

    Raises:
        Error: If there is an error fetching the data.

    """
    query = "SELECT * FROM Users WHERE User_ID = ?"
    try:
        connection = db_connection()
        cursor = get_cursor(connection)
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
        return user
    except Error as e:
        print(f"Error fetching data: {e}")
    finally:
        if connection is not None:
            cursor.close()
            connection.close()

def insert_strategy(user_id, strategy_name, strategy_description, strategy_code, parameters):
    """
    Inserts a strategy into the Strategies table.

    Args:
        user_id (int): The ID of the user.
        strategy_name (str): The name of the strategy.
        strategy_description (str): The description of the strategy.
        strategy_code (str): The code of the strategy.
        parameters (str): The parameters of the strategy.

    Returns:
        int: The ID of the inserted row.

    Raises:
        Error: If there is an error inserting the data.

    """
    query = """
    INSERT INTO Strategies (User_ID, Strategy_Name, Strategy_Description, Strategy_Code, Parameters)
    VALUES (?, ?, ?, ?, ?)
    """
    try:
        connection = db_connection()
        cursor = get_cursor(connection)
        cursor.execute(query, (user_id, strategy_name, strategy_description, strategy_code, parameters))
        connection.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"Error inserting data: {e}")
    finally:
        if connection is not None:
            cursor.close()
            connection.close()

def get_strategy(strategy_id):
    """
    Retrieves a strategy from the Strategies table.

    Args:
        strategy_id (int): The ID of the strategy.

    Returns:
        tuple: The strategy data as a tuple.

    Raises:
        Error: If there is an error fetching the data.

    """
    query = "SELECT * FROM Strategies WHERE Strategy_ID = ?"
    try:
        connection = db_connection()
        cursor = get_cursor(connection)
        cursor.execute(query, (strategy_id,))
        strategy = cursor.fetchone()
        return strategy
    except Error as e:
        print(f"Error fetching data: {e}")
    finally:
        if connection is not None:
            cursor.close()
            connection.close()

def insert_order(user_id, strategy_id, trading_pair, order_type, order_status):
    """
    Inserts an order into the Orders table.

    Args:
        user_id (int): The ID of the user.
        strategy_id (int): The ID of the strategy.
        trading_pair (str): The trading pair of the order.
        order_type (str): The type of the order.
        order_status (str): The status of the order.

    Returns:
        int: The ID of the inserted row.

    Raises:
        Error: If there is an error inserting the data.

    """
    query = """
    INSERT INTO Orders (User_ID, Strategy_ID, Trading_Pair, Order_Type, Order_Status)
    VALUES (?, ?, ?, ?, ?)
    """
    try:
        connection = db_connection()
        cursor = get_cursor(connection)
        cursor.execute(query, (user_id, strategy_id, trading_pair, order_type, order_status))
        connection.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"Error inserting data: {e}")
    finally:
        if connection is not None:
            cursor.close()
            connection.close()

def get_order(order_id):
    """
    Retrieves an order from the Orders table.

    Args:
        order_id (int): The ID of the order.

    Returns:
        tuple: The order data as a tuple.

    Raises:
        Error: If there is an error fetching the data.

    """
    query = "SELECT * FROM Orders WHERE Order_ID = ?"
    try:
        connection = db_connection()
        cursor = get_cursor(connection)
        cursor.execute(query, (order_id,))
        order = cursor.fetchone()
        return order
    except Error as e:
        print(f"Error fetching data: {e}")
    finally:
        if connection is not None:
            cursor.close()
            connection.close()

def insert_risk_control_rule(user_id, strategy_id, stop_loss, take_profit, position_limit, leverage_level):
    """
    Inserts a risk control rule into the Risk_Control_Rules table.

    Args:
        user_id (int): The ID of the user.
        strategy_id (int): The ID of the strategy.
        stop_loss (float): The stop loss value.
        take_profit (float): The take profit value.
        position_limit (int): The position limit value.
        leverage_level (int): The leverage level value.

    Returns:
        int: The ID of the inserted row.

    Raises:
        Error: If there is an error inserting the data.

    """
    query = """
    INSERT INTO Risk_Control_Rules (User_ID, Strategy_ID, Stop_Loss, Take_Profit, Position_Limit, Leverage_Level)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    try:
        connection = db_connection()
        cursor = get_cursor(connection)
        cursor.execute(query, (user_id, strategy_id, stop_loss, take_profit, position_limit, leverage_level))
        connection.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"Error inserting data: {e}")
    finally:
        if connection is not None:
            cursor.close()
            connection.close()

def get_risk_control_rule(rule_id):
    """
    Retrieves a risk control rule from the Risk_Control_Rules table.

    Args:
        rule_id (int): The ID of the risk control rule.

    Returns:
        tuple: The risk control rule data as a tuple.

    Raises:
        Error: If there is an error fetching the data.

    """
    query = "SELECT * FROM Risk_Control_Rules WHERE Rule_ID = ?"
    try:
        connection = db_connection()
        cursor = get_cursor(connection)
        cursor.execute(query, (rule_id,))
        rule = cursor.fetchone()
        return rule
    except Error as e:
        print(f"Error fetching data: {e}")
    finally:
        if connection is not None:
            cursor.close()
            connection.close()


def main():
    """Create the tables in the SQLite database"""
    connection = create_connection(db_file)
    if connection is not None:
        try:
            # 创建表
            connection.executescript(create_tables_sql)
            print('表已成功创建。')
            print('测试')
            insert_user('testuser', 'testpassword', 'testemail')
            user = get_user(1)
            print(user)
            insert_strategy(1, 'Test Strategy', 'This is a test strategy', 'print("Hello, World!")', 'None')
            strategy = get_strategy(1)
            print(strategy)
            insert_order(1, 1, 'BTC/USDT', 'Buy', 'Open')
            order = get_order(1)
            print(order)
            insert_risk_control_rule(1, 1, 100.0, 200.0, 10, 5)
            rule = get_risk_control_rule(1)
            print(rule)

        except Error as e:
            print(e)
        finally:
            close_connection(connection)
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()


