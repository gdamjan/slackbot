# -*- coding: utf-8 -*-

# requires: websockets slacker-asyncio
from slacker import Slacker
import websockets


import asyncio
import json, itertools
import sys

class Bot():
    def __init__(self, config):
        self.config = config
        self.slack_info = None
        self.websocket = None
        self._seq = itertools.count(1)
        self._timeouts = 0

    async def run(self):
        slack = Slacker(self.config.token)
        resp = await slack.rtm.start()
        self.slack_info = resp.body

        ws_url = self.slack_info['url']
        self.websocket = await websockets.connect(ws_url)
        # endless loop
        while True:
            await self.loop()
        await self.websocket.close()

    async def send(self, msg):
        msg['id'] = next(self._seq)
        data = json.dumps(msg)
        await asyncio.wait_for(self.websocket.send(data), self.config.timeout)
        print("> {}".format(data), file=sys.stderr, flush=True)

    async def recv(self):
        data = await asyncio.wait_for(self.websocket.recv(), self.config.timeout)
        print("< {}".format(data), file=sys.stderr, flush=True)
        return json.loads(data)

    async def loop(self):
        try:
            event = await self.recv()
            self._timeouts = 0
        except asyncio.TimeoutError:
            self._timeouts += 1
            if self._timeouts > 3:
                raise asyncio.TimeoutError
            await self.send({'type': 'ping'})
            return
        reply = await self.process(event)
        if not reply:
            return
        await self.send(reply)

    async def process(self, event):
        return
