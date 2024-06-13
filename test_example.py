import pytest
import akshare as ak
import numpy as np  # 导入numpy以处理numpy.float64
import json
import itertools
def get_stock_current_price(stock_code, place='cn'):
    stock_code = str(stock_code)
    print("get_stock_current_price, stock_code:", stock_code)
    if len(stock_code) == 5:
        place = 'hk'
    print("aaaaa")
    print('place', place)
    try:
        if place == 'cn':
            print("cn")
            stock_info = ak.stock_zh_a_spot_em()
            current_price = stock_info[stock_info['代码'] == stock_code]['最新价'].values[0]
        elif place == 'hk':
            print('hk')
            stock_info = ak.stock_hk_spot_em()
            current_price = stock_info[stock_info['代码'] == stock_code]['最新价'].values[0]
        else:
            raise ValueError("Unsupported place code")
        return current_price
    except ValueError:
        raise  # 重新抛出ValueError以确保测试能捕获
    except Exception as e:
        print(e)
        print("异常")
        return 0


with open('stock_prices.json', 'r', encoding='utf-8') as f:
    stocks_expected_prices = json.load(f)

@pytest.mark.parametrize("stock_code, expected_price", itertools.islice(stocks_expected_prices.items(), 200,300))
def test_stock_prices(stock_code, expected_price):
    actual_price = get_stock_current_price(stock_code, 'cn')
    assert np.isclose(actual_price, expected_price, atol=0.01), f"Expected price for {stock_code} was {expected_price}, but got {actual_price}."
