from .corebot import CoreBot as Bot

class StupidBot(Bot):
    async def process(self, event):
        return None