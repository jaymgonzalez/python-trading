import requests
import json

# API endpoint
url = "https://fapi.binance.com"

# API endpoint for open interest and volume data
path = "/futures/data/openInterestHist"

# Parameters for API request
symbol = "BTCUSDT"
period = "1d"
limit = "10"

# API request
params = {"symbol": symbol, "period": period, "limit": limit}
response = requests.get(url + path, params=params)

# Parse JSON response
data = json.loads(response.text)

print(data)

# Extract open interest and volume data
open_interest = [float(datum["sumOpenInterest"]) for datum in data]
volume = [float(datum["sumVolume"]) for datum in data]

# Calculate position size
margin_balance = 10000  # example margin balance
leverage = 10  # example leverage
position_size = margin_balance / leverage

# Calculate bankruptcy price
bankruptcy_price = position_size / (open_interest[-1] * leverage)

# Calculate liquidation price
entry_price = 50000  # example entry price
liquidation_price = bankruptcy_price + (entry_price - bankruptcy_price) * (1 - leverage)

# Calculate liquidation levels
stop_loss_percentage = 0.05  # example stop loss percentage
long_liquidation_price = liquidation_price - (liquidation_price - entry_price) * (
    1 - stop_loss_percentage
)
short_liquidation_price = liquidation_price + (entry_price - liquidation_price) * (
    1 - stop_loss_percentage
)

print("Long liquidation price:", long_liquidation_price)
print("Short liquidation price:", short_liquidation_price)
