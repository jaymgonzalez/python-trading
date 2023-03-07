import asyncio
import json
import os
from websockets import connect

websocket_uri = 'wss://stream.binance.com:9443/ws'