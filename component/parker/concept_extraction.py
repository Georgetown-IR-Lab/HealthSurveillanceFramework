import codecs
import datetime
import json
import sys

import Orange

from framework.concept_extraction import ConceptExtraction


class ConceptExtractionParker(ConceptExtraction):
    """ Concept extraction component based on
        J. Parker, Y. Wei, A. Yates, N. Goharian, O. Frieder, "A Framework for Detecting Public Health Trends with Twitter",
        The 2013 IEEE/ACM International Conference on Advances in Social Network Analysis and Mining, August 2013. """

    def run(self):
        conceptPairs = {}

        months = {}
        for docid, txt in self.stream_docs():
            dt = datetime.datetime.fromtimestamp(self.docmeta[docid]['created_at'])
            month = (dt.year - 2009) * 12 + dt.month

            months.setdefault(month, []).append((docid, txt))

        # map each term in an itemset to the docs from the associated month that contain the term
        termdocs = {}
        # map each month to the frequent itemsets that occurred in it
        monthitems = {k: [] for k in months.keys()}

        for month, docs in months.iteritems():
            print "month %s" % month
            monthitems[month] = []

            if len(docs) == 0:
                print "empty month: %s" % month
                continue

            with codecs.open(".orange.basket", "w", encoding="utf-8") as f:
                for docid, txt in docs:
                    print >> f, ", ".join(txt.split(" "))
            data = Orange.data.Table(".orange.basket")
            monthterms = set()
            inducer = Orange.associate.AssociationRulesSparseInducer(support=0.001,
                                                                     store_examples=False,
                                                                     maxItemSets=1000000)
            for items, _ in inducer.get_itemsets(data):
                terms = tuple(data.domain[x].name for x in items)
                monthitems[month].append(terms)
                monthterms.update(terms)

            for docid, txt in docs:
                for term in set(txt.split(" ")).intersection(monthterms):
                    termdocs.setdefault(term, set()).add(docid)

        months = None

        monthdocs = {}
        for month in monthitems.keys():
            patterns = monthitems[month]
            print "comb", month
            for pattern in patterns:
                if any(ord(c) >= 128 for term in pattern for c in term):
                    continue
                docs = set.intersection(*[termdocs[term] for term in pattern])
                monthdocs.setdefault(month, {}).setdefault(u" ".join(pattern), set()).update(docs)

            del monthitems[month]
        monthitems = None

        # keep only pairs with increased frequency
        lastmonth = {}
        conceptPairs = {}
        for month in monthdocs.keys():
            print "filter %s" % month
            for pattern, docs in monthdocs[month].iteritems():
                if pattern not in lastmonth or len(docs) / lastmonth[pattern] > 1.5:
                    conceptPairs.setdefault(pattern, set()).update(docs)

                lastmonth[pattern] = float(len(docs))

            for pattern in lastmonth.keys():
                if pattern not in monthdocs[month]:
                    del(lastmonth[pattern])

        conceptPairs = dict([(k, list(v)) for k, v in conceptPairs.iteritems()])
        json.dump(conceptPairs, codecs.open(self.outfn, "w", encoding="utf-8"))

    def load_docmeta(self, docmeta):
        self.docmeta = json.load(codecs.open(docmeta, "r", encoding="utf-8"))

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print >> sys.stderr, "usage: <docfiles file> <output file> <document metadata file>"
        sys.exit(1)

    ce = ConceptExtractionParker(docfiles=sys.argv[1], outfn=sys.argv[2])
    ce.load_docmeta(docmeta=sys.argv[3])
    ce.run()
