import codecs
import json

from abc import ABCMeta, abstractmethod


class TrendDetection(object):
    __metaclass__ = ABCMeta

    def __init__(self, docMeta=None, conceptPairs=None, outfn=None):
        """ Args:
        docMeta: a JSON document metadata file
        conceptPairs: a JSON ConceptPairs file
        outfn: the filename to write this component's TrendTimes output to
        """

        for var in ['docMeta', 'conceptPairs', 'outfn']:
            if eval(var) is None:
                raise TypeError("%s cannot be None" % var)

        self.docMeta = json.load(codecs.open(docMeta, "r", encoding="utf-8"))
        self.conceptPairs = json.load(codecs.open(conceptPairs, "r", encoding="utf-8"))
        self.outfn = outfn

    @abstractmethod
    def run(self):
        """ Runs component and writes output to self.outfn """
        pass
