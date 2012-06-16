import nltk
from nltk.probability import FreqDist, LaplaceProbDist
from cPickle import load

class Extractor(object):
    "Caching Borg that extracts a list of important words from a text"
    __state = None
    def __init__(self):
        if self.__state is None:
            self.init_state()
        self.__dict__ = self.__state

    def init_state(self):
        with open('data/word_freq.pickle') as f:
            self.__state = dict(
                    log_threshold = -11,
                    prob_dist = load(f))

    def is_noun(self, w):
        return w[0] == 'N'

    def is_verb(self, w):
        return w[0] == 'V'

    def is_adjunction(self, w):
        return w[0:2] == 'JJ'

    def is_important(self, w, tag):
        return self.is_unusual(w) and (self.is_verb(tag) or self.is_noun(tag) or self.is_adjunction(tag))

    def is_unusual(self, w):
        return self.prob_dist.logprob(w) < self.log_threshold

    def extract(self, text):
        tagged_words = [(w.lower(),tag) for sent in nltk.sent_tokenize(text) for w,tag in nltk.pos_tag(nltk.word_tokenize(sent))]
        return set(w for w,tag in tagged_words if
                self.is_important(w,tag))
