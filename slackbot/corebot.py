# -*- coding: utf-8 -*-

from slacker import Slacker
import websockets

from abc import ABCMeta, abstractmethod
import asyncio
import json, itertools
import sys


class CoreBot(metaclass=ABCMeta):
    def __init__(self, config):
        self.config = config
        self.slack_info = None
        self.websocket = None
        self._seq = itertools.count(1)
        self._timeouts = 0
        self.stopping = False
        self.stopped = asyncio.Future()

    def stop(self):
        self.stopping = True
        return self.stopped

    async def start(self):
        slack = Slacker(self.config.token)
        resp = await slack.rtm.start()
        self.slack_info = resp.body

        ws_url = self.slack_info['url']
        self.websocket = await websockets.connect(ws_url)
        # endless async loop
        while not self.stopping:
            await self.loop()
        await self.websocket.close()
        self.stopped.set_result(None)


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

    async def send(self, msg):
        msg['id'] = next(self._seq)
        data = json.dumps(msg)
        await asyncio.wait_for(self.websocket.send(data), self.config.timeout)
        self.log("> {}".format(data))

    async def recv(self):
        data = await asyncio.wait_for(self.websocket.recv(), self.config.timeout)
        self.log("< {}".format(data))
        return json.loads(data)

    @abstractmethod
    async def process(self, event):
        raise Exception(NotImplemented)

    def log(self, msg):
        print(msg, file=sys.stderr, flush=True)
