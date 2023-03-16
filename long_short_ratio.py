import requests
import json

# API endpoint
url = "https://fapi.binance.com"

# API endpoint for open interest and volume data
path = "/futures/data/topLongShortAccountRatio"

# Parameters for API request
symbol = "BTCUSDT"
period = "12h"
limit = 250

# API request
params = {"symbol": symbol, "period": period, "limit": limit}
response = requests.get(url + path, params=params)

# Parse JSON response
data = json.loads(response.text)

# print(data)

# Extract open interest and volume data
longShortRatio = [float(datum["longShortRatio"]) for datum in data]
longAccount = [float(datum["longAccount"]) for datum in data]
shortAccount = [float(datum["shortAccount"]) for datum in data]


print("longShortRatio:", longShortRatio)
print("longAccount:", longAccount)
print("shortAccount:", shortAccount)
