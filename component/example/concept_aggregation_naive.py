import codecs
import json
import sys

from framework.concept_aggregation import ConceptAggregation


class ConceptAggregationNaive(ConceptAggregation):
    """ Concept aggregation component that maps each concept to the first thesaurus entry containing the concept """

    def run(self):
        aggConceptPairs = {}

        for concept, docids in self.conceptPairs.iteritems():
            if concept in self.revthesaurus:
                    aggConceptPairs[self.revthesaurus[concept]] = list(docids)

        json.dump(aggConceptPairs, codecs.open(self.outfn, "w", encoding="utf-8"))

    def load_thesaurus(self, fn):
        self.thesaurus = json.load(codecs.open(fn, "r", encoding="utf-8"))

        self.revthesaurus = {}
        for entryid, concepts in self.thesaurus.iteritems():
            for concept in concepts:
                if concept not in self.revthesaurus:
                    self.revthesaurus[concept] = entryid

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print >> sys.stderr, "usage: <ConceptPairs file> <thesaurus file> <output file>"
        sys.exit(1)

    ca = ConceptAggregationNaive(conceptPairs=sys.argv[1], outfn=sys.argv[3])
    ca.load_thesaurus(sys.argv[2])
    ca.run()
