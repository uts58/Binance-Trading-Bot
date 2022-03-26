import configparser


class Config:
    def __init__(self):
        parser = configparser.ConfigParser()
        parser.read('./configs/config.cfg')

        self.KLINE_PERIOD = parser.get('config', 'KLINE_PERIOD')
        self.RSI_PERIOD = parser.getint('config', 'RSI_PERIOD')
        self.RSI_OVERBOUGHT = parser.getint('config', 'RSI_OVERBOUGHT')
        self.RSI_OVERSOLD = parser.getint('config', 'RSI_OVERSOLD')
        self.TRADE_SYMBOL = parser.get('config', 'TRADE_SYMBOL')
        self.TRADE_QUANTITY = parser.getfloat('config', 'TRADE_QUANTITY')
        self.HAS_COIN = parser.getboolean('config', 'HAS_COIN')

        self.SOCKET_URL = f'wss://stream.binance.com:9443/ws/{self.TRADE_SYMBOL}@kline_{self.KLINE_PERIOD}'

        self.API_KEY = parser.get('api_key', 'API_KEY')
        self.API_SECRET = parser.get('api_key', 'API_SECRET')
        self.TLD = parser.get('api_key', 'TLD')

    def get_config(self):
        return self.SOCKET_URL, self.KLINE_PERIOD, self.RSI_PERIOD, self.RSI_OVERBOUGHT, self.RSI_OVERSOLD, self.TRADE_SYMBOL, self.TRADE_QUANTITY, self.HAS_COIN

    def get_api_keys(self):
        return self.API_KEY, self.API_SECRET, self.TLD
