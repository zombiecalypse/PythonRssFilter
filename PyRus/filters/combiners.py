from .filters import Filter
from time import struct_time
import itertools

class Sorter(Filter):
    def __call__(self, rss):
        return reversed(sorted(rss, key = self.sort_key))
    def sort_key(self, x):
        if 'updated_parsed' in x:
            return x['updated_parsed']
        else:
            return struct_time((2000,1,1,0,0,0,0,0,0))
