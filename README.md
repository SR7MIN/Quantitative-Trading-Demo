# Quantitative-Trading-Demo
安装mysql后，输入以下命令来创建相应的用户及数据库：
1. mysql -u root -p
2. CREATE USER '1'@'localhost' IDENTIFIED BY '123456';
3. GRANT ALL PRIVILEGES ON db_fin_tech.* TO '1'@'localhost';
4. FLUSH PRIVILEGES;
5. exit
6. mysql -u 1 -p
7. CREATE DATABASE db_fin_tech;
8. USE db_fin_tech;
9. CREATE TABLE users (
    username VARCHAR(50),
    nickname VARCHAR(50),
    password VARCHAR(50),
    balance FLOAT DEFAULT 1000000,
    stocks_held JSON,
    history JSON,
    yesterdayTotal JSON
);
