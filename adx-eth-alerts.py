import ccxt, yfinance
import pandas_ta as ta
import pandas as pd
import requests

exchange = ccxt.binance()

bars = exchange.fetch_ohlcv('BTC/USDT', timeframe='5m', limit=500)
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

WEBHOOK_URL = "https://discord.com/api/webhooks/861696033436598293/m6-jMeIAQs6va6ePHr_HFK6npwaswkugWDLcSmHWBXYf5POzMgQIJySrO9-3FNd0ZUAj"


if last_row['ADX_14'] >= 25:
    if last_row['DMP_14'] > last_row['DMN_14'] and last_row['RSI_14'] <= 35:
        message = f"Watch for Buy Opportunity: The ADX is {last_row['ADX_14']:.2f}, ${last_row['close']:.4f}, H:{last_row['high']:.2f}, L:{last_row['low']:.2f}, RSI:{last_row['RSI_14']:.0f}"
    if last_row['DMP_14'] > last_row['DMN_14'] and last_row['RSI_14'] < 35:
        message = f"Strong Uptrend: The ADX is {last_row['ADX_14']:.2f}, ${last_row['close']:.4f}, H:{last_row['high']:.2f}, L:{last_row['low']:.2f}, RSI:{last_row['RSI_14']:.0f}"
    if last_row['DMN_14'] > last_row['DMP_14'] and last_row['RSI_14'] >= 65:
        message = f"Watch for Sell Opportunity: The ADX is {last_row['ADX_14']:.2f}, ${last_row['close']:.4f}, H:{last_row['high']:.2f}, L:{last_row['low']:.2f}, RSI:{last_row['RSI_14']:.0f}"
    if last_row['DMN_14'] > last_row['DMP_14'] and last_row['RSI_14'] > 65:
        message = f"Strong Downtrend: The ADX is {last_row['ADX_14']:.2f}, ${last_row['close']:.4f}, H:{last_row['high']:.2f}, L:{last_row['low']:.2f}, RSI:{last_row['RSI_14']:.0f}"    

    payload = {
        "username": "btc-bot",
        "content": message
    }
    requests.post(WEBHOOK_URL, json=payload)

if last_row['ADX_14'] < 25:
    message = f"NO TREND: The ADX is {last_row['ADX_14']:.2f}, ${last_row['close']:.4f}, H:{last_row['high']:.2f}, L:{last_row['low']:.2f}, RSI:{last_row['RSI_14']:.0f}"
    payload = {
        "username": "btc-bot",
        "content": message}

    requests.post(WEBHOOK_URL, json=payload)

