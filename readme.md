#BINANCE-TRADING-BOT


Trading bot using RSI indicator for **Binance Exchange**. This bot uses basic RSI overbought/oversold strategy.

Python 3.6 or greater version is required.
****
***This is not a financial service or investment advice! USE IT AS YOUR OWN RISK***
****

## Install Packages
Run:
```
pip install requirements.txt
```
****
## Quick Start
Install requirements first

- Edit `configs/config.cfg`
- Edit `configs/apprise_config.yml` (If you want to send push notifications to discord/ telegram etc.)
- Run `python3 main.py`


Config

- `KLINE_PERIOD` = Candle period (ex: 1m)
- `RSI_PERIOD` = RSI Time Frame (ex: 30)
- `RSI_OVERBOUGHT` = RSI Oversold (ex: 30)
- `RSI_OVERSOLD` = RSI Oversold (ex: 30)
- `TRADE_SYMBOL` = coin pair (ex: GALAUSDT)
- `TRADE_QUANTITY` = How many coins you want to buy sell (ex: 300)
- `HAS_COIN` = "true" if you've already bought the coin in trade symbol before starting bot, otherwise false
- `API_KEY` = API key from Binance
- `API_SECRET` = API secret from Binance
- `TLD` = "com" for non-US, otherwise "us"
****
# Issues, suggestions and contributing

If you run into any issues while using the bot or if you want to request any changes or new features, open a new issue
to let us know.

If you would like to contribute to the development and profitability of the bot, simply open a PR or let us know.
