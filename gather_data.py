from binance.client import Client

client = Client()

klines = client.get_historical_klines(
    "BTCUSDT", Client.KLINE_INTERVAL_1HOUR, "1 hour ago UTC"
)


print(klines)
