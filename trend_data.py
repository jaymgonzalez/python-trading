import asyncio
import json
import os
from websockets import connect

websocket_uri = "wss://stream.binance.com/ws/btcusdt@kline_1m"

# websocket_uri = "wss://stream.binance.com/ws/btcusdt@ticker_1h"

filename = "BTC_HOURLY_TEST.csv"

if not os.path.isfile(filename):
    with open(filename, "w") as f:
        f.write(
            ",".join(
                [
                    "Kline_start_time",
                    "Kline_close_time",
                    "Symbol",
                    "Interval",
                    "First_trade_ID",
                    "Last_trade_ID",
                    "Open_price",
                    "Close_price",
                    "High_price",
                    "Low_price",
                    "Base_asset_volume",
                    "Number_of_trades",
                    "Is_this_kline_closed?",
                    "Quote_asset_volume",
                    "Taker_buy_base_asset_volume",
                    "Taker_buy_quote_asset_volume",
                    "Ignore",
                    # "Event_type",
                    # "Event_time",
                    # "Symbol",
                    # "Price_change",
                    # "Price_change_percent",
                    # "Open_price",
                    # "High_price",
                    # "Low_price",
                    # "Last_price",
                    # "Weighted_average_price",
                    # "Total_traded_base_asset_volume",
                    # "Total_traded_quote_asset_volume",
                    # "Statistics_open_time",
                    # "Statistics_close_time",
                    # "First_trade_ID",
                    # "Last_trade_Id",
                    # "Total_number_of_trades",
                ]
            )
            + "\n"
        )


async def binance_liquidations(uri, filename):
    async for websocket in connect(uri):
        try:
            while True:
                msg = await websocket.recv()
                print(msg)
                msg = json.loads(msg)["k"]
                # msg = json.loads(msg)
                msg = [str(x) for x in list(msg.values())]
                print(msg[12])
                with open(filename, "a") as f:
                    if msg[12] == "True":
                        f.write(",".join(msg) + "\n")
        except Exception as e:
            print(e)
            continue


asyncio.run(binance_liquidations(websocket_uri, filename))
