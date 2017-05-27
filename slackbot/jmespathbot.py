import jmespath
import inspect
from .corebot import CoreBot

class JMESPathBot(CoreBot):
    @staticmethod
    def match(pattern):
        def annotate(func):
            setattr(func, '_pattern', pattern)
            return func
        return annotate

    async def process(self, event):
        for _name, func in inspect.getmembers(self, predicate=inspect.ismethod):
            pattern = getattr(func, '_pattern', None)
            if pattern and jmespath.search(pattern, [event]):
                return await func(event)
