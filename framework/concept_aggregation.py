import codecs
import json

from abc import ABCMeta, abstractmethod


class ConceptAggregation(object):
    __metaclass__ = ABCMeta

    def __init__(self, conceptPairs=None, outfn=None):
        """ Args:
        conceptPairs: a JSON ConceptPairs file
        outfn: the filename to write this component's ConceptPairs output to
        """

        for var in ['conceptPairs', 'outfn']:
            if eval(var) is None:
                raise TypeError("%s cannot be None" % var)

        self.conceptPairs = json.load(codecs.open(conceptPairs, "r", encoding="utf-8"))
        self.outfn = outfn

    @abstractmethod
    def run(self):
        """ Runs component and writes output to self.outfn """
        pass
