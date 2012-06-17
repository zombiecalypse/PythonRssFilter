from .filters import Filter
from concurrent import futures
import feedparser

class GetFeed(Filter):
    def __init__(self, url):
        self.url = url
        self.cached = None

    def add_rss_title_to_items(self, d):
        for e in d['entries']:
            e['title'] = u"[{}] {}".format(d['feed']['title'], e['title'])
        return d

    def __call__(self, *args):
        if self.cached is None:
            self.cached = self.add_rss_title_to_items(feedparser.parse(self.url))
        return self.cached

    def applied(self, *args):
        return self()['entries']
