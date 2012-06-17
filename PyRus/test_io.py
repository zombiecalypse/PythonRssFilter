from testtools import TestCase
from testtools.matchers import *
from testtools.testcase import ExpectedException
from ludibrio import Stub

from StringIO import StringIO

from .filters import *

from .test_helpers import *

simple_string = """<?xml version="1.0" encoding="UTF-8"?>
        <rss xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:media="http://search.yahoo.com/mrss/" version="2.0">
            <channel>
                <title>Example feed</title>
                <link>http://www.example.com/rss/</link>
                <description>the description is great</description>
                <item>
                  <title>The number 101010</title>
                  <link>http://www.example.com/article/101010</link>
                  <guid isPermaLink="true">http://www.reddit.com/r/Poetry/comments/stbxy/learning_thursday_share_a_poetry_technique_with/</guid>
                  <pubDate>Thu, 26 Apr 2012 02:27:01 -0700</pubDate>
                  <description>item description 101010</description>
                </item>
            </channel>
        </rss>"""
xkcd_string = """<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom"
xml:lang="en"><title>xkcd.com</title><link href="http://xkcd.com/"
rel="alternate"></link><id>http://xkcd.com/</id><updated>2012-06-01T00:00:00Z</updated><entry><title>Kill
Hitler</title><link href="http://xkcd.com/1063/"
rel="alternate"></link><updated>2012-06-01T00:00:00Z</updated><id>http://xkcd.com/1063/</id><summary
type="html">&lt;img src="http://imgs.xkcd.com/comics/kill_hitler.png"
title="Revised directive: It is forbidden for you to interfere with human
history until you've at least taken a class on it." alt="Revised directive: It
is forbidden for you to interfere with human history until you've at least taken
a class on it." /&gt;</summary></entry><entry><title>Budget News</title><link
href="http://xkcd.com/1062/"
rel="alternate"></link><updated>2012-05-30T00:00:00Z</updated><id>http://xkcd.com/1062/</id><summary
type="html">&lt;img src="http://imgs.xkcd.com/comics/budget_news.png" title="I
will vote, no questions asked, for any candidate who describes themselves as
'more of a deficit sugar glider.'" alt="I will vote, no questions asked, for any
candidate who describes themselves as 'more of a deficit sugar glider.'"
/&gt;</summary></entry><entry><title>EST</title><link
href="http://xkcd.com/1061/"
rel="alternate"></link><updated>2012-05-28T00:00:00Z</updated><id>http://xkcd.com/1061/</id><summary
type="html">&lt;img src="http://imgs.xkcd.com/comics/est.png" title="The month
names are the same, except that the fourth month only has the name 'April' in
even-numbered years, and is otherwise unnamed." alt="The month names are the
same, except that the fourth month only has the name 'April' in even-numbered
years, and is otherwise unnamed."
/&gt;</summary></entry><entry><title>Crowdsourcing</title><link
href="http://xkcd.com/1060/"
rel="alternate"></link><updated>2012-05-25T00:00:00Z</updated><id>http://xkcd.com/1060/</id><summary
type="html">&lt;img src="http://imgs.xkcd.com/comics/crowdsourcing.png"
title="We don't sell products; we sell the marketplace. And by 'sell the
marketplace' we mean 'play shooters, sometimes for upwards of 20 hours
straight.'" alt="We don't sell products; we sell the marketplace. And by 'sell
the marketplace' we mean 'play shooters, sometimes for upwards of 20 hours
straight.'" /&gt;</summary></entry></feed>"""

class TestIoSimpleRss(TestCase):
    @Test
    def simple(self):
        self.rss =  GetFeed(simple_string)()

    @Given(simple)
    def has_been_parsed(self):
        self.assertThat(self.rss['feed'], Contains('title'))
        self.assertThat(self.rss['feed']['title'], Equals('Example feed'))
        self.assertThat(self.rss, Contains('entries'))
        self.assertThat(len(self.rss['entries']), Equals(1))

    @Given(simple)
    def reparse(self):
        new_xml = xml_string(self.rss)
        self.assertThat(new_xml, IsInstance(str))
        self.rss = GetFeed(new_xml)()
        self.assertThat(self.rss, IsInstance(dict))

    @Given(reparse, has_been_parsed)
    def reparsed_correctly(self): pass

class TestIoComplexRss(TestCase):
    @Test
    def xkcd(self):
        self.rss =  GetFeed(xkcd_string)()

    @Given(xkcd)
    def has_been_parsed(self):
        self.assertThat(self.rss['feed'], Contains('title'))
        self.assertThat(self.rss['feed']['title'], Equals('xkcd.com'))
        self.assertThat(self.rss, Contains('entries'))
        self.assertThat(len(self.rss['entries']), Equals(4))

    @Given(xkcd)
    def reparse(self):
        new_xml = xml_string(self.rss)
        self.assertThat(new_xml, IsInstance(str))
        self.rss = GetFeed(new_xml)()
        self.assertThat(self.rss, IsInstance(dict))

    @Given(reparse, has_been_parsed)
    def reparsed_correctly(self): pass

