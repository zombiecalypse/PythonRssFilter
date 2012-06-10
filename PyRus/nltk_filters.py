import nltk

class Extractor(object):
    "Caching Borg that extracts a list of important words from a text"
    __state = dict()

    def __init__(self):
        self.__dict__ = self.__state

    def is_noun(self, w):
        return w[0] == 'N'

    def is_verb(self, w):
        return w[0] == 'V'

    def is_adjunction(self, w):
        return w[0:2] == 'JJ'

    def is_important(self, w):
        return self.is_verb(w) or self.is_noun(w) or self.is_adjunction(w)

    def extract(self, text):
        tagged_words = [(w,tag) for sent in nltk.sent_tokenize(text) for w,tag in nltk.pos_tag(nltk.word_tokenize(sent))]
        return set(w.lower() for w,tag in tagged_words if
                self.is_important(tag))

