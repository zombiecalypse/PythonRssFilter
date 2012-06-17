from .filters import Filter
from ..helpers import *

class DictSink(Filter):
    def __init__(self, title):
        self.title = title
    def __call__(self, rss):
        if 'feed' not in rss: rss['feed'] = dict()

        return of_type(dict, updated(rss, feed = updated(rss['feed'], title = self.title),
                entries = list(rss['entries'])))

class FileSink(Filter):
    def __init__(self, file, title):
        self.file = file
        self.title = title
    def __call__(self, rss):
        if isinstance(self.file, basestring):
            with open(self.file, 'w') as f:
                self.write_to(f, rss)
        else:
            self.write_to(self.file, rss)
        return rss

    def write_to(self,file, rss):
        file.write(xml_string(rss))
