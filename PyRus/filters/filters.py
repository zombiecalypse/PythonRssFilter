from itertools import chain
from ..helpers import *
from .rssxml import xml_string


def filter(main_filter, rss):
    return list(main_filter(rss)) 

def make_filter_from_config(config):
    return BlackListFilter(config['blacklist'])

class Filter(object):
    """
    A simple DSL for processing rss feeds.

    >>> getter = GetUrl('http://www.reddit.com/r/Poetry/.rss') 
    >>> filter = WhiteListFilter('rain') & KeywordFilter('autumn') # '&' joins sets
    >>> sink = Sink('/var/rss/poetry_about_rain_or_autumn.rss')
    >>> proc = getter >> filter >> sink # '>>' feeds one into the other
    >>> proc()
    """
    def __rshift__(self, other):
        return CompositionFilter(self, other)
    def __and__(self, other):
        return CombinationFilter(self, other)
    def __not__(self):
        return NegationFilter(self)
    def __call__(self, rss = None):
        if rss is None: rss = dict(entries=[])
        return updated(rss, entries = self.applied(rss['entries']))

class CompositionFilter(Filter):
    def __init__(self, *lst):
        assert all(isinstance(x, Filter) for x in lst)
        self.list = lst
        self.composition = reduce(self.compose, reversed(self.list))

    @staticmethod
    def compose(f,g):
        return lambda x: f(g(x))

    def __call__(self, rss):
        return of_type(dict, self.composition(rss))

    def __rshift__(self, other):
        if isinstance(other, CompositionFilter):
            return CompositionFilter(*(self.list + other.list))
        else:
            return CompositionFilter(*(self.list + (other,)))

class NegationFilter(Filter):
    def __init__(self, first):
        assert isinstance(first, Filter)
        self.first = first
    def __not__(self):
        return  self.first

    def applied(self, rss):
        inv = set(self.first(rss))
        for item in rss:
            if item not in inv:
                yield item

class CombinationFilter(Filter):
    def __init__(self, *filters):
        assert all(isinstance(x, Filter) for x in filters)
        self.list = filters

    def applied(self, rss = []):
        hashed = set()
        for i in chain.from_iterable(f.applied(rss) for f in self.list): 
            if i not in hashed:
                hashed.add(i)
                yield i

    def __and__(self, other):
        if isinstance(other, CombinationFilter):
            return CombinationFilter(*(self.filters+other.filters))
        else:
            return CombinationFilter(other, *self.filters)


