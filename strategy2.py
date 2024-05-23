import akshare as ak
import pandas as pd
import numpy as np

def produce_signal(stock_code):
    # 获取股票数据
    stock_zh_a_daily_df = ak.stock_zh_a_daily(symbol="sh"+str(stock_code), adjust="qfq")
    # print(stock_zh_a_daily_df)

    # 计算移动平均线
    stock_zh_a_daily_df['MA10'] = stock_zh_a_daily_df['close'].rolling(window=10).mean()

    # 创建一个空的DataFrame来存储交易信号
    signals = pd.DataFrame(index=stock_zh_a_daily_df.index)
    signals['signal'] = 0.0

    # 当股票价格上穿移动平均线时，生成买入信号
    signals['signal'][10:] = np.where(stock_zh_a_daily_df['close'][10:] > stock_zh_a_daily_df['MA10'][10:], 1.0, -1.0)   

    # 生成交易订单
    signals['positions'] = signals['signal'].diff()

    # 打印交易信号
    #print(signals)
    return signals

result=produce_signal(688031)
#print(result['positions'])