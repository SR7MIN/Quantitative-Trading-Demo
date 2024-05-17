from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建数据库连接
DATABSE_URI = 'mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(
    user='root', password='123456', server='localhost', database='all_users')
engine = create_engine(DATABSE_URI)
# engine = create_engine('mysql://root:428099@114.212.81.66/mydb')
# 创建会话工厂
Session = sessionmaker(bind=engine)

# 创建数据模型基类
Base = declarative_base()

# 创建数据模型类


class Student(Base):
    __tablename__ = 'All_User_table'
    account = Column(String(25), primary_key=True)
    name = Column(String(50))
    password = Column(String(10))


# 创建表
Base.metadata.create_all(engine)

# 创建会话
session = Session()

# 插入数据
student1 = Student(account='1257047642', name="Alice", password="123")
student2 = Student(account="1271060910",name='Bob',password="123")
session.add_all([student1, student2])
session.commit()

# 查询数据
students = session.query(Student).all()
for student in students:
    print(student.account, student.name, student.password)

# 更新数据
student1.name = "Jack"
session.commit()

# 删除数据
session.delete(student2)
session.commit()

# 关闭会话
session.close()


# import mysql.connector

# # 创建数据库连接
# cnx = mysql.connector.connect(user='root', password='123456', host='localhost', database='all_users')

# # 创建游标
# cursor = cnx.cursor()

# # 执行 SQL 查询
# query = 'SELECT name, age, gender, major FROM students'
# cursor.execute(query)

# # 获取查询结果
# for (name, age, gender, major) in cursor:
#     print(name, age, gender, major)
#     print("xxxx")

# # 关闭游标和连接
# cursor.close()
# cnx.close()