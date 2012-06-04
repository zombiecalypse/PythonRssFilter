import os
from itertools import chain

def filter(rss):
    return list(main_filter(rss)) #TODO

main_filter = PredicateFilter(lambda x: False)

class CompositionFilter(Filter):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __call__(self, rss):
        for item in self.second(self.first(rss)):
            yield item

class CombinationFilter(Filter):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __call__(self, rss):
        hashed = set()
        for i in chain(self.first(rss), self.second(rss)): 
            if hash(i) not in hashed:
                hashed.add(hash(i))
                yield i

class Filter(object):
    def __rshift__(self, other):
        return CompositionFilter(self, other)
    def __and__(self, other):
        return CombinatonFilter(self, other)

class PredicateFilter(Filter):
    def __init__(self, filt):
        self.filter = filt

    def __call__(self, rss):
        for item in rss:
            if self.filter(item):
                yield item

class BlackListFilter(PredicateFilter):
    def __init__(self, blocked):
        self.name = filename
        self.blocked = blocked
        PredicateFilter.__init__(self, lambda i: i not in blocked)

class WhiteListFilter(PredicateFilter):
    def __init__(self, allowed):
        self.name = filename
        self.allowed = allowed
        PredicateFilter.__init__(self, lambda i: i in allowed)
