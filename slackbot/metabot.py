import jsonpath_rw_ext
import inspect

from abc import ABCMeta

class Meta(ABCMeta):
    def __init__(cls, name, bases, namespace, **kwargs):
        super().__init__(name, bases, namespace)
        cls._patterns = list(Meta.get_all_patterns(cls))   # each class gets its own set

    @staticmethod
    def get_all_patterns(cls):
        for _name, func in inspect.getmembers(cls, predicate=inspect.isfunction):
            pattern = getattr(func, '_pattern', None)
            if pattern:
                yield (func, pattern)

    # decorator
    @staticmethod
    def match(pattern):
        def annotate(f):
            f._pattern = jsonpath_rw_ext.parse(pattern)
            return f
        return annotate


from .corebot import CoreBot
class MetaBot(CoreBot, metaclass=Meta):
    match = Meta.match

    async def process(self, event):
        for func, pattern in self._patterns:
            match = pattern.find([event])
            if match:
                return await func(self, event)
