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

def xml_item(item):
    "Item -> Xml"
    return E.item(
            E.title(item['title']),
            E.pubDate(item['updated']),
            E.description(item['description']),
            E.guid(item['id'], isPermaLink = str(item['guidislink']).lower()),
            E.link(item['link']))
