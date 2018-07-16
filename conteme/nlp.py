
from .Opinionizer.Opinionizer import Opinionizer
from pampo import ner
import spacy as sp
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class NLPPlugin(object):
    def __init__(self, lang):
        print('Loading plugin (lang=%s)' % lang)
        self.lang = lang
    def detect_ner(self, text):
        raise NotImplementedError
    def detect_sent(self, text):
        raise NotImplementedError

class NLPPluginPT(object):
    def __init__(self):
        NLPPlugin.__init__(self, 'pt')
        self.opinion = Opinionizer()
        self.pampo = ner.extract_entities
        #self.spacy_nlp = sp.load('pt_core_news_sm')
    def detect_ner(self, text):
        return self.pampo(text)
    def detect_sent(self, text):
        opt,_,_ = self.opinion.classify(text)
        if opt is None:
            opt = 0
        return opt

class NLPPluginEN(object):
    def __init__(self):
        NLPPlugin.__init__(self, 'en')
        self.opinion = SentimentIntensityAnalyzer()
        self.spacy_nlp = sp.load('en_core_web_sm')
    def detect_ner(self, text):
        doc_nlp = self.spacy_nlp(text)
        return doc_nlp.ents
    def detect_sent(self, text):
        opt = self.opinion.polarity_scores(text)
        return round(opt['compound'])

class NLPallLanguages(object):
    INSTANCE = None
    def __init__(self):
        self.plugins = {}
        if NLPallLanguages.INSTANCE is not None:
            self = NLPallLanguages.INSTANCE
        else:
            for lang in ['pt','en']:
                self.plugins[lang] = self.getPlugin(lang)
    @staticmethod
    def getInstance():
        if NLPallLanguages.INSTANCE is None:
            NLPallLanguages.INSTANCE = NLPallLanguages()
        return NLPallLanguages.INSTANCE
    def get_sentiment(self, text, lang):
        if lang not in self.plugins:
            self.plugins[lang] = self.getPlugin(lang)
        return self.plugins[lang].detect_sent(text)
    def get_ner(self, text, lang):
        if lang not in self.plugins:
            self.plugins[lang] = self.getPlugin(lang)
        return self.plugins[lang].detect_ner(text)
    def getPlugin(self, lang):
        if lang[:2] == 'pt':
            return NLPPluginPT()
        if lang[:2] == 'en':
            return NLPPluginEN()
