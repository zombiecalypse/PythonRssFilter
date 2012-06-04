from operator import add
from concurrent import futures
from .filters import filter as filt

def updated(d, **kwargs):
    d2 = dict(d)
    d2.update(kwargs)
    return d2

def filter(rss):
    "RssFeed -> RssFeed, such that unwanted items are removed"
    return filt(rss)

def sort(rss):
    "RssFeed -> RssFeed, such that important items turn up top"
    return updated(rss, entries = 
                list(reversed(sorted(
                    rss['entries'], 
                    key = lambda x: x['updated_parsed'])))) #TODO

def process_single(rss):
    return sort(filter(rss))

def merge(rsses, new_name = "Merged"):
    "[RssFeed] -> RssFeed"
    all_items = reduce(add, [e['entries'] for e in rsses], [])
    return sort( dict(entries = all_items, feed = dict(title = new_name)))

def process(rsses, new_name = "Combined"):
    with futures.ThreadPoolExecutor(max_workers=10) as e:
        return merge(e.map(process_single, rsses), new_name)
