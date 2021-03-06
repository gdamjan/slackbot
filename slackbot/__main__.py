from collections import namedtuple
import os
import sys
import signal
import asyncio
import argparse

def main():
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

    async def start():
        try:
            await bot.start()
        except:
            loop.stop()
            raise

    async def shutdown():
        await bot.shutdown()
        loop.stop()

    for signum in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(signum, lambda : asyncio.ensure_future(shutdown()))

    asyncio.ensure_future(start())
    try:
        loop.run_forever()
    finally:
        loop.close()

if __name__ == '__main__':
    main()
