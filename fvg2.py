import yfinance as yf
import pandas as pd

def fair_value_gap(ticker):
    data = yf.download(ticker, period="1d", interval="1m")
    data['mid'] = (data['High'] + data['Low']) / 2
    data['body'] = abs(data['Open'] - data['Close'])
    data['shadows'] = abs(data['High'] - data['Low'])

    body_avg = data['body'].rolling(3).mean()
    shadows_avg = data['shadows'].rolling(3).mean()
    volume_avg = data['Volume'].rolling(3).mean()

    is_fvg = (data['mid'] >= body_avg.shift(2)) & (data['Volume'] >= volume_avg.shift(2))                & (data['body'] >= body_avg) & (data['shadows'] < shadows_avg.shift(2))

    return is_fvg

# Example usage
ticker = 'AAPL'
fvg = fair_value_gap(ticker)
print(fvg)