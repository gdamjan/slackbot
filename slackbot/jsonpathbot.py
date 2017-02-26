import jsonpath_rw_ext
import inspect
from .corebot import CoreBot

class JsonPathBot(CoreBot):
    @staticmethod
    def match(pattern):
        def annotate(func):
            setattr(func, '_pattern', pattern)
            return func
        return annotate

    async def process(self, event):
        for _name, func in inspect.getmembers(self, predicate=inspect.ismethod):
            pattern = getattr(func, '_pattern', None)
            if pattern:
                path_finder = jsonpath_rw_ext.parse(pattern)
                match = path_finder.find([event])
                if match:
                    return await func(self, event)
