import yfinance as yf
import logging

logging.basicConfig(level=logging.INFO)


def get_close_prices(stok):
    tesla = yf.Ticker(stok)
    close_prices = tesla.history(period="60d", interval="15m")["Close"]
    return close_prices


def get_rsi(close_prices):
    rsi_lst = []
    list_of_diffs = []
    gains = []
    losses = []
    for i in range(len(close_prices)-1):
        diff = close_prices[i+1] - close_prices[i]
        list_of_diffs.append(diff)
        if len(list_of_diffs) >= 13:
            gains_and_losses = list_of_diffs[i-13:i]
            for j in gains_and_losses:
                if j > 0:
                    gains.append(j)
                else:
                    losses.append(j)
            if sum(losses) != 0:
                rs = abs((sum(gains)/14)/(sum(losses)/14))
            else:
                rs = 100
            rsi = 100 - (100 / (1 + rs))
            rsi_lst.append(rsi)
            gains.clear()
            losses.clear()
    rsi_lst.remove(rsi_lst[0])
    return rsi_lst


def give_signal(closed_prices, rsi_lst):
    closed_prices = closed_prices[14:]
    time = closed_prices.index
    prices_and_rsi = dict(zip(closed_prices, rsi_lst))
    order = False
    for i, (closed_price, rsi) in enumerate(prices_and_rsi.items()):
        if not order and rsi < 30:
            logging.info("order in place , %s , %s", closed_price, time[i].strftime('%Y-%m-%d %H:%M:%S'))
            order = True
        if order and rsi > 50:
            logging.info("order closed , %s , %s \n", closed_price, time[i].strftime('%Y-%m-%d %H:%M:%S'))
            order = False


stock = "TSLA"

prices = get_close_prices(stok=stock)
rsi_list = get_rsi(close_prices=prices)
give_signal(prices, rsi_list)
