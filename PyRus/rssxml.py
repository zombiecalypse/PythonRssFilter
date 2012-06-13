from PyRSS2Gen import *
from datetime import datetime
from time import mktime


def xml_string(rss):
    return rss_xml(rss).to_xml(encoding='utf8')

def rss_xml(rss):
    "RssFeed -> Xml"
    feed = rss['feed']
    return RSS2(
            title = feed['title'],
            lastBuildDate = datetime.utcnow(),
            items = map(xml_item, rss['entries']))

def try_to_make_guid(item):
    try:
        return Guid(item['id'])
    except KeyError as e:
        return Guid(item['link'])

def try_to_make_pubdate(item):
	try:
		return datetime.fromtimestamp(mktime(item['updated_parsed']))
	except KeyError as e:
		return None

def try_to_make_description(item):
    try:
        item['description'] = sanitize(item['description'])
        return E.description(item['description'])
    except Exception as e:
        print e
        print repr(item['description'])

def sanitize(string):
    return unicode(string)

def xml_item(item):
    "Item -> Xml"
    return RSSItem(
            title = item['title'],
            link = item['link'],
            pubDate = try_to_make_pubdate(item),
            description = try_to_make_description(item),
            guid = try_to_make_guid(item))
