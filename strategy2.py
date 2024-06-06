# import akshare as ak
# import pandas as pd
# import numpy as np

# def produce_signal(stock_code):
#     # 获取股票数据
#     stock_zh_a_daily_df = ak.stock_zh_a_daily(symbol="sh"+str(stock_code), adjust="qfq")
#     # print(stock_zh_a_daily_df)

#     # 计算移动平均线
#     stock_zh_a_daily_df['MA10'] = stock_zh_a_daily_df['close'].rolling(window=10).mean()

#     # 创建一个空的DataFrame来存储交易信号
#     signals = pd.DataFrame(index=stock_zh_a_daily_df.index)
#     signals['signal'] = 0.0

#     # 当股票价格上穿移动平均线时，生成买入信号
#     signals['signal'][10:] = np.where(stock_zh_a_daily_df['close'][10:] > stock_zh_a_daily_df['MA10'][10:], 1.0, -1.0)   

#     # 生成交易订单
#     signals['positions'] = signals['signal'].diff()

#     # 打印交易信号
#     #print(signals)
#     return signals

# result=produce_signal(688031)
# #print(result['positions'])


import akshare as ak
import pandas as pd
import numpy as np

def produce_signal(stock_code):
    # 获取股票数据
    stock_zh_a_daily_df = ak.stock_zh_a_daily(symbol="sh"+str(stock_code), adjust="qfq")
    print(stock_zh_a_daily_df)

    # 计算移动平均线
    stock_zh_a_daily_df['MA10'] = stock_zh_a_daily_df['close'].rolling(window=10).mean()

    # 创建一个空的DataFrame来存储交易信号
    signals = pd.DataFrame(index=stock_zh_a_daily_df.index)
    signals['signal'] = 0.0

    # 当股票价格上穿移动平均线时，生成买入信号
    signals['signal'][10:] = np.where(stock_zh_a_daily_df['close'][10:] > stock_zh_a_daily_df['MA10'][10:], 1.0, -1.0)   

    # 生成交易订单
    signals['positions'] = signals['signal'].diff()

    # 计算交易数量
    signals['trade_volume'] = np.where(signals['positions'] != 0, 100, 0)

    # 添加止损和止盈条件
    stop_loss_level = -0.05
    take_profit_level = 0.10
    stock_zh_a_daily_df['daily_return'] = stock_zh_a_daily_df['close'].pct_change()
    signals['stop_loss'] = np.where(stock_zh_a_daily_df['daily_return'] < stop_loss_level, -1.0, 0.0)
    signals['take_profit'] = np.where(stock_zh_a_daily_df['daily_return'] > take_profit_level, 1.0, 0.0)

    # 如果触发止损或止盈条件，立即清仓
    signals['positions'] = np.where((signals['stop_loss'] == -1.0) | (signals['take_profit'] == 1.0), 0, signals['positions'])
    signals['trade_volume'] = np.where((signals['stop_loss'] == -1.0) | (signals['take_profit'] == 1.0), 0, signals['trade_volume'])

    return signals

result=produce_signal(688031)
print(result)