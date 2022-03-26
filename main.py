import json
import os
import sys

import websocket
from binance.client import Client
from binance.enums import *

from classes.apprise_client import AppriseClient
from classes.coin import Coin
from classes.config import Config
from library.library import log_printer

sys.dont_write_bytecode = True

config = Config()
SOCKET_URL, KLINE_PERIOD, RSI_PERIOD, RSI_OVERBOUGHT, RSI_OVERSOLD, TRADE_SYMBOL, TRADE_QUANTITY, in_position = config.get_config()
API_KEY, API_SECRET, TLD = config.get_api_keys()
apprise_client = AppriseClient()

client = Client(API_KEY, API_SECRET, tld=TLD)
open('bot.pid', 'w').write(str(os.getpid()))


def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        order_ = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        log_printer(f'Side: {side}, Quantity: {quantity}, Symbol: {symbol}')
        log_printer(order_)
        coin.send_notification(order_)
    except Exception as e:
        log_printer(f'EXEPTION: {e}')
        coin.send_notification(e)
        return False
    return True


def on_open(ws):
    log_printer('Webstream Opened')


def on_close(ws):
    log_printer('Webstream Closed')


def on_message(ws, message):
    global in_position

    json_message = json.loads(message)
    is_candle_closed = json_message['k']['x']
    if is_candle_closed:
        coin.update(json_message)
        last_rsi = coin.coin_df['rsi'].iloc[-1]
        log_printer(f'Last RSI: {last_rsi}')

        if last_rsi > RSI_OVERBOUGHT:
            if in_position:
                log_printer(f'Overbought detected, Selling')
                order_succeeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
                if order_succeeded:
                    in_position = False
            else:
                log_printer('Overbought detected, but nothing to do')

        if last_rsi < RSI_OVERSOLD:
            if in_position:
                log_printer('Oversold detected, but but nothing to do')
            else:
                log_printer(f'Oversold detected, buying')
                order_succeeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                if order_succeeded:
                    in_position = True


coin = Coin(symbol=TRADE_SYMBOL, interval=KLINE_PERIOD, limit=100)
ws = websocket.WebSocketApp(SOCKET_URL, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()
