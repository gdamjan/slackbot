# -*- coding: utf-8 -*-

import dispatchonvalue as dv
import random, pkg_resources
from .basebot import Bot

dispatch = dv.DispatchOnValue()

class SmartBot(Bot):

    def __init__(self, config):
        super().__init__(config)
        fn = pkg_resources.resource_filename(__name__, 'smarties.txt')
        self.smarties = open(fn, encoding='utf-8', newline='\n').readlines()

    async def process(self, event):
        try:
            return dispatch.dispatch(event, self)
        except dv.DispatchFailed:
            return None

@dispatch.add({'type':'message', 'message': dv.any_a})
def reply_smartly(event, bot):
    me_id = bot.slack_info['self']['id']
    me_mentioned = '<@{}>'.format(me_id)

    if me_mentioned in event['text']:
        smarts = random.choice(bot.smarties)
        smarts = smarts.strip()
        smarts = smarts.replace('\r', '\n')
        response = "Hi <@{}>. {}".format(event['user'], smarts)
        channel = event['channel']
        return {'type': 'message', 'channel': channel, 'text': response}
    return None
