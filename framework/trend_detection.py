import codecs
import json
import time

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

    def _aggregate_trends(self, trends, aggregatef):
        """ Aggregate document counts from different days by calling aggregatef on each date. Args:
        trends: a dictionary mapping concepts to dates to counts
        aggregatef: a function taking a datetime object and returning a new datetime object at some level of aggregation
        """

        agg_trends = {}
        for concept, datecounts in trends.iteritems():
            if concept not in agg_trends:
                agg_trends[concept] = {}

            for date, count in datecounts.iteritems():
                unixtime = time.mktime(aggregatef(date).timetuple())
                agg_trends[concept][unixtime] = agg_trends[concept].get(unixtime, 0) + count

        return {concept: [{"start": unixtime, "end": unixtime, "strength": count} for unixtime, count in times.iteritems()]
                for concept, times in agg_trends.iteritems()}
