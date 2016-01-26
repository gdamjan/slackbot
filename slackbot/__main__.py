from .basebot import Bot
from .smartbot import SmartBot

from collections import namedtuple
import os, asyncio


def get_config():
    Config = namedtuple('Config', ['timeout', 'token'])
    token = os.environ['BOT_SLACK_TOKEN']
    timeout = int(os.environ.get('BOT_PING_INTERVAL', 20))
    return Config(timeout, token)

def run(Class):
    config = get_config()
    bot = Class(config)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.run())
    loop.close()

def base():
    run(Bot)

def smart():
    run(SmartBot)

if __name__ == '__main__':
    base()
