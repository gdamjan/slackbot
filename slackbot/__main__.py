from collections import namedtuple
import os
import sys
import asyncio
import argparse

parser = argparse.ArgumentParser(prog='slackbot')
parser.add_argument("mode", choices=['smart','stupid'])
parser.add_argument("-i", "--ping-interval", type=int,
                    help="interval in seconds to send slack pings",
                    default=int(os.environ.get('SLACKBOT_PING_INTERVAL', 20)))
parser.add_argument("-t", "--token", type=str,
                    help="slack access token",
                    default=os.environ.get('SLACKBOT_TOKEN'))


args = parser.parse_args()

Config = namedtuple('Config', ['timeout', 'token'])
config = Config(args.ping_interval, args.token)

if args.mode == 'stupid':
    from .stupidbot import StupidBot
    bot = StupidBot(config)
elif args.mode == 'smart':
    from .smartbot import SmartBot
    bot = SmartBot(config)
else:
    sys.exit(1) # should not get here, since argparse would disallow it

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(bot.run())
except KeyboardInterrupt:
    pass
loop.close()
