# -*- coding: utf-8 -*-

import random, pkg_resources
from .jsonpathbot import JsonPathBot as Bot

class SmartBot(Bot):

    def __init__(self, config):
        super().__init__(config)
        fn = pkg_resources.resource_filename(__name__, 'smarties.txt')
        self.smarties = open(fn, encoding='utf-8', newline='\n').readlines()


    @Bot.match('$[?(type == "message")]')
    async def reply_smartly(self, event):
        me_id = self.slack_info['self']['id']
        me_mentioned = '<@{}>'.format(me_id)

        if me_mentioned in event['text']:
            smarts = random.choice(self.smarties)
            smarts = smarts.strip()
            smarts = smarts.replace('\r', '\n')
            response = "Hi <@{}>. {}".format(event['user'], smarts)
            channel = event['channel']
            return {'type': 'message', 'channel': channel, 'text': response}
        return None
