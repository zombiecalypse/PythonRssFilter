from .filters import Filter
from ..helpers import *

import os
import re

class PredicateFilter(Filter):
    def __init__(self, filt):
        self.filter = filt

    def applied(self, rss):
        for item in rss:
            if self.filter(item):
                yield item

class TitleFilter(PredicateFilter):
    def __init__(self):
        PredicateFilter.__init__(self, lambda x: self.match(x['title']))

class BlackListFilter(TitleFilter):
    "blocks any title that matches the regex in `blocked`"
    def __init__(self, *blocked):
        TitleFilter.__init__(self)
        self.blocked = map(lambda x: re.compile(".*{}.*".format(x)), blocked)

    def match(self, x):
        return not any(e.match(x) for e in self.blocked)

class WhiteListFilter(TitleFilter):
    "allows only titles that matches the regex in `allowed`"
    def __init__(self, *allowed):
        TitleFilter.__init__(self)
        self.allowed = map(lambda x: re.compile(".*{}.*".format(x)), allowed)

    def match(self, x):
        return any(e.match(x) for e in self.allowed)
