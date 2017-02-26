import jsonpath_rw_ext

from abc import ABCMeta
import inspect

class Meta(ABCMeta):
    def __init__(cls, name, bases, namespace, **kwargs):
        super().__init__(name, bases, namespace)
        cls._patterns = list(Meta.get_all_annotated(cls))   # each class gets its own set

    @staticmethod
    def get_all_annotated(cls):
        for _name, func in inspect.getmembers(cls, predicate=inspect.isfunction):
            pattern = getattr(func, '_pattern', None)
            if pattern:
                yield (func, pattern)

    # decorator
    @staticmethod
    def match(pattern):
        def annotate(func):
            setattr(func, '_pattern', pattern)
            return func
        return annotate


from .corebot import CoreBot
class MetaBot(CoreBot, metaclass=Meta):
    async def process(self, event):
        for func, pattern in self._patterns:
            path_finder = jsonpath_rw_ext.parse(pattern)
            match = path_finder.find([event])
            if match:
                return await func(self, event)
