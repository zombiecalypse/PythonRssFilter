import os
import re
from itertools import chain

def filter(main_filter, rss):
    return list(main_filter(rss)) 

def make_filter_from_config(config):
    return BlackListFilter(config['blacklist'])

class Filter(object):
    def __rshift__(self, other):
        return CompositionFilter(self, other)
    def __and__(self, other):
        return CombinatonFilter(self, other)
    def __not__(self):
        return NegationFilter(self)

compose = lambda f,g: lambda x: f(g(x))

class CompositionFilter(Filter):
    def __init__(self, *lst):
        self.list = lst
        self.composition = reduce(compose, self.list)

    def __call__(self, rss):
        for item in self.composition(rss):
            yield item

class NegationFilter(Filter):
    def __init__(self, first):
        self.first = first
    def __not__(self):
        return  self.first

    def __call__(self, rss):
        inv = set(self.first(rss))
        for item in rss:
            if item not in inv:
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


class PredicateFilter(Filter):
    def __init__(self, filt):
        self.filter = filt

    def __call__(self, rss):
        for item in rss:
            if self.filter(item):
                yield item

class TitleFilter(PredicateFilter):
    def __init__(self):
        PredicateFilter.__init__(self, lambda x: self.match(x['title']))

class BlackListFilter(TitleFilter):
    "blocks any title that matches the regex in `blocked`"
    def __init__(self, blocked):
        TitleFilter.__init__(self)
        self.blocked = map(lambda x: re.compile(".*{}.*".format(x)), blocked)

    def match(self, x):
        return not any(e.match(x) for e in self.blocked)
