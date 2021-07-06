import ccxt, yfinance
import pandas_ta as ta
import pandas as pd
import requests

exchange = ccxt.binance()

bars = exchange.fetch_ohlcv('ETC/USDT', timeframe='5m', limit=500)
df = pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'volume'])

adx = df.ta.adx(fast=14, slow=6)
macd = df.ta.macd(fast=14, slow=28)
rsi = df.ta.rsi()

df = pd.concat([df, adx, macd, rsi], axis=1)

print(df)


last_row = df.iloc[-1]
comparison_row = df.iloc[-2]
confirmation_row = df.iloc[-3]

print(last_row)

WEBHOOK_URL = "https://discord.com/api/webhooks/861696853313585153/q3ypGxNqoTckuD4bmI88YgMkeJac-V85S8MpgUgTxbiRuwPdNXp7wPHTzm2p0usOm_oJ"

if last_row['ADX_14'] >= 25:
    if last_row['DMP_14'] > last_row['DMN_14'] and last_row['RSI_14'] <= 30:
        message = f"Watch for Buy Opportunity: The ADX is {last_row['ADX_14']:.2f}, ${last_row['close']:.4f}, H:{last_row['high']:.2f}, L:{last_row['low']:.2f}"
    if last_row['DMP_14'] > last_row['DMN_14'] and last_row['RSI_14'] > 30:
        message = f"Strong Uptrend: The ADX is {last_row['ADX_14']:.2f}, ${last_row['close']:.4f}, H:{last_row['high']:.2f}, L:{last_row['low']:.2f}"
    if last_row['DMN_14'] > last_row['DMP_14'] and last_row['RSI_14'] <= 30:
        message = f"Watch for Sell Opportunity: The ADX is {last_row['ADX_14']:.2f}, ${last_row['close']:.4f}, H:{last_row['high']:.2f}, L:{last_row['low']:.2f}"
    if last_row['DMN_14'] > last_row['DMP_14'] and last_row['RSI_14'] > 30:
        message = f"Strong Downtrend: The ADX is {last_row['ADX_14']:.2f}, ${last_row['close']:.4f}, H:{last_row['high']:.2f}, L:{last_row['low']:.2f}"    

    payload = {
        "username": "etc-bot",
        "content": message
    }

    requests.post(WEBHOOK_URL, json=payload)

if last_row['ADX_14'] < 25:
    message = f"NO TREND: The ADX is {last_row['ADX_14']:.2f}, ${last_row['close']:.4f}, H:{last_row['high']:.2f}, L:{last_row['low']:.2f}"

    payload = {
        "username": "etc-bot",
        "content": message
    }

    requests.post(WEBHOOK_URL, json=payload)

if last_row['low'] > comparison_row['low']:
    message = f"Possible Reversal, moving up"
     
    payload = {
        "username": "etc-bot",
        "content": message
    }

if last_row['low'] > confirmation_row['low']:
    message = f"Reversal confirmed, moving up"
    payload = {
        "username": "etc-bot",
        "content": message
    }

if last_row['high'] < confirmation_row['low']:
    message = f"Reversal confirmed, moving up"
    payload = {
        "username": "etc-bot",
        "content": message
    }