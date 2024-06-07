# Quantitative-Trading-Demo
登录mysql后，输入以下命令来创建相应的数据库：
1. CREATE DATABASE db_fin_tech;
2. USE db_fin_tech;
3. CREATE TABLE users (
    username VARCHAR(50),
    nickname VARCHAR(50),
    password VARCHAR(50),
    balance FLOAT DEFAULT 1000000,
    stocks_held JSON,
    history JSON,
    yesterdayTotal JSON
);
