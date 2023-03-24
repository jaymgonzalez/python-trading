import yfinance as yf
import time

# Get current epoch time
current_time = int(time.time())

# Calculate epoch time one hour ago
one_hour_ago = current_time - 3600 * 24

print(one_hour_ago)


data = yf.download('BTC-USD', start='2023-03-23', end=None, interval='1h')


print(data)