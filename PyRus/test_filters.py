from testtools import TestCase
from testtools.matchers import *
from testtools.testcase import ExpectedException
from ludibrio import Stub

from .test_helpers import *

from .filters import *
from .nltk_filters import *
import nltk

class ExtractorTest(TestCase):
    @Test
    def stoplist_sanity(self):
        self.assertThat(nltk.corpus.stopwords.words('english'),
                Contains('most'))

    @Given(stoplist_sanity)
    def unusualness_test(self):
        self.assertFalse(Extractor().is_unusual("most"))
    @Test
    def set_text(self):
        self.texts = (
                "But now to something completely different",
                """Most part-of-speech tagsets make use of the same basic
                categories, such as noun, verb, adjective, and preposition.
                However, tagsets differ both in how finely they divide words
                into categories, and in how they define their categories""")

    @Given(set_text)
    def extract_monty(self):
        extracted = Extractor().extract(self.texts[0])
        self.assertThat(extracted, Contains("different"))

    @Given(set_text)
    def extract_difficult(self):
        self.extracted = Extractor().extract(self.texts[1])

    @Given(extract_difficult)
    def contains_important(self):
        extracted = self.extracted
        self.assertThat(extracted, Contains("part-of-speech"))
        self.assertThat(extracted, Contains("categories"))
        self.assertThat(extracted, Contains("tagsets"))
        self.assertThat(extracted, Contains("divide"))
        self.assertThat(extracted, Contains("preposition"))
        self.assertThat(extracted, Contains("define"))

    @Given(extract_difficult)
    def does_not_contain_boring(self):
        extracted = self.extracted
        self.assertThat(extracted, Not(Contains("in")))
        self.assertThat(extracted, Not(Contains("their")))
        self.assertThat(extracted, Not(Contains("how")))
        self.assertThat(extracted, Not(Contains("and")))
        self.assertThat(extracted, Not(Contains("into")))
        self.assertThat(extracted, Not(Contains("most")))

