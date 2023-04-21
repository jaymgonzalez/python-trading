import asyncio
import json
import os
from websockets import connect
import sqlite3


con = sqlite3.connect("tick_btcusdt.db")
cur = con.cursor()

res = cur.execute("SELECT name FROM sqlite_master")

if res.fetchall() is None:
    cur.execute("CREATE TABLE btcusdt(time, price, qty, is_mm)")


websocket_uri = "wss://stream.binance.com:9443/ws/btcusdt@trade"
filename = "binance.csv"

# if not os.path.isfile(filename):
#     with open(filename, "w") as f:
#         f.write(
#             ",".join(
#                 [
#                     "event_type",
#                     "event_time",
#                     "symbol",
#                     "trade_id",
#                     "price",
#                     "quantity",
#                     "buyer_order_id",
#                     "seller_order_id",
#                     "trade_time",
#                     "is_the_buyer_the_market_maker",
#                     "ignore",
#                 ]
#             )
#             + "\n"
#         )


async def binance_tick_data(uri, filename):
    async for websocket in connect(uri):
        try:
            while True:
                msg = await websocket.recv()
                print(msg)
                msg = json.loads(msg)
                msg = [str(x) for x in list(msg.values())]
                selected_values = (msg[1], msg[4], msg[5], msg[8])
                print(selected_values)
                cur.execute(
                    f"INSERT INTO btcusdt(time, price, qty, is_mm) VALUES(?,?,?,?)",
                    selected_values,
                )
                con.commit()
                # with open(filename, "a") as f:
                #     f.write(",".join(msg) + "\n")
        except Exception as e:
            print(e)
            continue


asyncio.run(binance_tick_data(websocket_uri, filename))
