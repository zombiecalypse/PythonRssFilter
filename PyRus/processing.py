from operator import add
from concurrent import futures
from time import struct_time
from .filters import filter, make_filter_from_config


def _updated(d, **kwargs):
    d2 = dict(d)
    d2.update(kwargs)
    return d2

def sort_key(x):
	if 'updated_parsed' in x:
		return x['updated_parsed']
	else:
		return struct_time((2000,1,1,0,0,0,0,0,0))

class Processor(object):
    def __init__(self, config):
        self.new_name = config['new_name'] if 'new_name' in config else "merged"
        self.main_filter = make_filter_from_config(config['filter']) if 'filter' in config else lambda x: x

    def filter(self, rss):
        "RssFeed -> RssFeed, such that unwanted items are removed"
        return _updated(rss, entries = filter(self.main_filter, rss['entries']))

    def sort(self, rss):
        "RssFeed -> RssFeed, such that important items turn up top"
        return _updated(rss, entries = 
                    list(reversed(sorted(
                        rss['entries'], 
                        key = sort_key)))) #TODO

    def process_single(self, rss):
        return self.sort(self.filter(rss))

    def add_rss_title_to_items(self, rss):
        for e in rss['entries']:
            e['title'] = u"[{}] {}".format(rss['feed']['title'], e['title'])
        return rss

    def merge(self, rsses):
        "[RssFeed] -> RssFeed"
        all_items = reduce(add, [self.add_rss_title_to_items(e)['entries'] for e in rsses], [])
        return self.sort( dict(entries = all_items, feed = dict(title = self.new_name)))

    def process(self, rsses):
        with futures.ThreadPoolExecutor(max_workers=10) as e:
            return self.merge(e.map(self.process_single, rsses))
