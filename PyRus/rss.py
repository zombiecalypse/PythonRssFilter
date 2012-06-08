from concurrent import futures
import feedparser

def get_feed(feed_url):
    return feedparser.parse(feed_url)

def get_feeds(feed_urls):
    "Returns all feeds for the list"
    if not feed_urls: return []
    with futures.ThreadPoolExecutor(max_workers = 10) as e:
        return list(e.map(get_feed, feed_urls))
