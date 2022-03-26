import datetime

import pandas
from binance import Client
from ta.momentum import rsi

from classes.apprise_client import AppriseClient
from classes.config import Config
from library.library import log_printer


class Coin:
    data = list()
    coin_df = None
    buying_price = 0
    config = Config()
    RSI_PERIOD = config.RSI_PERIOD
    api_key, api_secret, tld = config.get_api_keys()

    def __init__(self, symbol, interval, limit=None, how_long=None):
        '''
        :param symbol: coin pair symbol
        :param interval: candle interval
        :param limit: candle limit
        :param how_long: days for backtesting
        '''
        self.client = Client(self.api_key, self.api_secret, tld='com')
        if how_long:
            until_date = datetime.datetime.now()
            since_date = until_date - datetime.timedelta(days=how_long)
            klines = self.client.get_historical_klines(symbol, interval, str(since_date), str(until_date))
        else:
            log_printer(f'Generating {symbol} with {interval}')
            klines = self.client.get_klines(symbol=symbol, interval=interval, limit=limit)
        self.symbol = symbol
        self.interval = interval
        self.limit = limit
        self.prepare(klines)
        self.apprise_client = AppriseClient()

    def send_notification(self, order_data):
        if type(order_data) != dict:
            self.apprise_client.send_notification(title='Exception', body=f'{order_data}')
        else:
            title = f'{order_data["side"]}: {order_data["symbol"]}'
            body = f'Amount: {order_data["origQty"]}\n' \
                   f'Average: {order_data["fills"][0]["price"]}\n' \
                   f'Commission: {float(order_data["fills"][0]["commission"]) * 395}\n' \
                   f'Total: {order_data["cummulativeQuoteQty"]}\n'

            if order_data['side'] == 'BUY':
                self.buying_price = order_data["cummulativeQuoteQty"]
                self.apprise_client.send_notification(title, body)
            else:
                profit = f'Profit: {float(order_data["cummulativeQuoteQty"]) - float(self.buying_price)}'
                body += profit
                self.apprise_client.send_notification(title=title, body=body)

    def prepare(self, klines):
        for kline in klines:
            self.data.append({
                'open_times': datetime.datetime.fromtimestamp(kline[0] / 1000),
                'close_times': datetime.datetime.fromtimestamp(kline[6] / 1000),
                'open_values': float(kline[1]),
                'high_values': float(kline[2]),
                'low_values': float(kline[3]),
                'close_values': float(kline[4])
            })
        self.calculate()

    def update(self, stream_data):
        new_data = {
            'open_times': datetime.datetime.fromtimestamp(stream_data['k']['t'] / 1000),
            'close_times': datetime.datetime.fromtimestamp(stream_data['k']['T'] / 1000),
            'open_values': float(stream_data['k']['o']),
            'high_values': float(stream_data['k']['h']),
            'low_values': float(stream_data['k']['l']),
            'close_values': float(stream_data['k']['c'])
        }
        self.data.append(new_data)
        self.data.pop(0)
        self.calculate()

    def calculate(self):
        df = pandas.DataFrame(self.data)
        # stoch_ = stoch(df['high_values'], df['low_values'], df['close_values'], window=14, smooth_window=1, fillna=False)
        # macd_ = macd(df['close_values'], window_slow=26, window_fast=12, fillna=False)
        # macd_signal_ = macd_signal(df['close_values'], window_slow=26, window_fast=12, window_sign=9, fillna=False)
        # macd_diff_ = macd_diff(df['close_values'], window_slow=26, window_fast=12, window_sign=9, fillna=False)
        rsi_ = rsi(df['close_values'], window=self.RSI_PERIOD, fillna=False)
        # self.coin_df = pandas.concat([df, stoch_, macd_, macd_signal_, macd_diff_, rsi_], axis=1)
        self.coin_df = pandas.concat([df, rsi_], axis=1)
