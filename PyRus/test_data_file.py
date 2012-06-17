from testtools import TestCase
from testtools.matchers import *
from testtools.testcase import ExpectedException
from ludibrio import Stub

from StringIO import StringIO

from .data_file import *
from .filters import *

from .test_helpers import *

simple_config="""
GetFeed('http://xkcd.com/rss') >> BlackListFilter('Hitler') >> DictSink('XKCD')
"""

complex_config="""
( GetFeed('http://xkcd.com/rss') & 
    (GetFeed('http://reddit.org') >> WhiteListFilter('rain'))) 
    >> BlackListFilter('Hitler') >> DictSink('XKCD and reddit')
"""

class TestLoadPipeline(TestCase):
    @Test
    def simple(self):
        file = StringIO(simple_config)
        file.name = '<string>'
        self.pipeline =  read_config(file)

    @Given(simple)
    def has_been_parsed_flat(self):
        self.assertThat(self.pipeline, IsInstance(CompositionFilter))

    @Given(has_been_parsed_flat)
    def deep_check(self):
        self.assertThat(self.pipeline.list, MatchesListwise([IsInstance(GetFeed),
            IsInstance(BlackListFilter), IsInstance(DictSink)]))

    @Test
    def complex(self):
        file = StringIO(complex_config)
        file.name = '<string>'
        self.pipeline =  read_config(file)

    @Given(complex)
    def has_been_parsed_flat_complex(self):
        self.assertThat(self.pipeline, IsInstance(CompositionFilter))

    @Given(has_been_parsed_flat_complex)
    def deep_check_complex(self):
        self.assertThat(self.pipeline.list, MatchesListwise([IsInstance(CombinationFilter),
            IsInstance(BlackListFilter), IsInstance(DictSink)]))
        comb = self.pipeline.list[0]
        self.assertThat(comb.list, MatchesListwise([IsInstance(GetFeed),
            IsInstance(CompositionFilter)]))
        reddit = comb.list[1]
        self.assertThat(reddit.list, MatchesListwise([IsInstance(GetFeed),
            IsInstance(WhiteListFilter)]))
