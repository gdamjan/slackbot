from collections import namedtuple
import os, asyncio


def get_config():
    Config = namedtuple('Config', ['timeout', 'token'])
    token = os.environ['SLACKBOT_TOKEN']
    timeout = int(os.environ.get('SLACKBOT_PING_INTERVAL', 20))
    return Config(timeout, token)

def run(Class):
    config = get_config()
    bot = Class(config)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.run())
    loop.close()

def stupid():
    from .stupidbot import StupidBot
    run(StupidBot)

def smart():
    from .smartbot import SmartBot
    run(SmartBot)

if __name__ == '__main__':
    stupid()
