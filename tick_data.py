import asyncio
import json
import os
from websockets import connect
import sqlite3


websocket_uri = "wss://stream.binance.com:9443/ws/btcusdt@trade"


async def binance_tick_data(uri):
    con = sqlite3.connect("tick_btcusdt.db")
    cur = con.cursor()

    res = cur.execute("SELECT name FROM sqlite_master")

    if res.fetchall() is None:
        cur.execute("CREATE TABLE btcusdt(time, price, qty, is_mm)")
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

        except Exception as e:
            print(e)
            continue

    con.close()


asyncio.run(binance_tick_data(websocket_uri))
