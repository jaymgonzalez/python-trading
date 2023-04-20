from openbb_terminal.sdk import openbb

# oi = openbb.crypto.dd.oi("BTC")


# print(oi)

import requests

url = "https://open-api.coinglass.com/public/v2/long_short?time_type=m5&symbol=BTC"

headers = {
    "accept": "application/json",
    "coinglassSecret": "",
}

response = requests.get(url, headers=headers)

print(response.text)
