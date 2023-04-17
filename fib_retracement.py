# Fibonacci Retracement Levels
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Download historical data from Yahoo Finance
ticker = 'SPY'
data = yf.download(ticker, start='2022-05-01', end='2023-01-01')

# Calculate the high, low, and close prices
high = data['High']
low = data['Low']
close = data['Close']

# print(high)

# Calculate the range of the price movement
range_price = high - low

# Calculate the retracement levels
retracements = [0,0.236, 0.5, 0.618, 0.786,1]

# Calculate the retracement levels in terms of price levels
retracement_levels = []

for retracement in retracements:
    print(range_price)
    retracement_level = high - (range_price * retracement)
    retracement_levels.append(retracement_level)
    print(retracement_level)


# # Plot the Fibonacci retracement levels
# plt.figure(figsize=(15,8))
# plt.plot(close, 'k')
# # for i, retracement_level in enumerate(retracement_levels):
# # plt.axhline(retracement_level[4], linestyle='--', label=f'{retracements[4]*100}%')
# plt.axhline(retracement_level[5], color="limegreen", linestyle="--", label="100%")
# plt.axhline(retracement_level[4], color="slateblue", linestyle="--", label="78.6%")
# plt.axhline(retracement_level[3], color="mediumvioletred", linestyle="--", label="61.8%")
# plt.axhline(retracement_level[2], color="gold", linestyle="--", label="50%")
# plt.axhline(retracement_level[1], color="darkturquoise", linestyle="--", label="23.6%")
# plt.axhline(retracement_level[0], color="lightcoral", linestyle="--", label="0%")

# plt.legend()
# plt.title('Fibonacci Retracement Levels')
# plt.xlabel('Date')
# plt.ylabel('Price $')
# plt.show()

# Plot the price data and retracement levels
plt.plot(high.index, high, label='High')
plt.plot(low.index, low, label='Low')

for i, retracement_level in enumerate(retracement_levels):
    plt.axhline(y=retracement_level.iloc[0], color='grey', linestyle='--')
    plt.text(x=high.index[0], y=retracement_level.iloc[0], s=f'{retracements[i]*100}%')

plt.legend()
plt.show()