from lxml.objectify import ElementMaker
from lxml.etree import tostring

E= ElementMaker(annotate=False)

def xml_string(rss):
    return tostring(rss_xml(rss), pretty_print =True)

def rss_xml(rss):
    "RssFeed -> Xml"
    feed = rss['feed']
    return E.rss(
            E.channel(
                E.title(feed['title']),
                *map(xml_item, rss['entries'])
                ),
            version = "2.0"
            )

def try_to_make_guid(item):
    try:
        return E.guid(item['id'], isPermaLink = str(item['guidislink']).lower())
    except KeyError as e:
        return E.guid(item['link'], isPermaLink = 'true')

def try_to_make_pubdate(item):
	try:
		return E.pubDate(item['updated'])
	except KeyError as e:
		return None

def try_to_make_description(item):
    try:
        return E.description(item['description'])
    except Exception as e:
        print e
        print item['description']

def xml_item(item):
    "Item -> Xml"
    return E.item(
            E.title(item['title']),
            try_to_make_pubdate(item),
            try_to_make_description(item),
            try_to_make_guid(item),
            E.link(item['link']))
