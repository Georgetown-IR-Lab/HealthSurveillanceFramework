import codecs
import json
import sys

from framework.concept_aggregation import ConceptAggregation


class ThesaurusConceptAggregation(ConceptAggregation):
    """ Concept aggregation component that maps each concept to the thesaurus entries containing the concept """

    def run(self):
        aggConceptPairs = {}

        for concept, docids in self.conceptPairs.iteritems():
            if concept in self.revthesaurus:
                agg_concepts = self.revthesaurus[concept]
            else:
                agg_concepts = set(subconcept for x in concept.split(" ") for subconcept in x if x in self.revthesaurus)

            for agg_concept in agg_concepts:
                aggConceptPairs.setdefault(agg_concept, set()).update(docids)

        json.dump({k: list(v) for k, v in aggConceptPairs.iteritems()}, codecs.open(self.outfn, "w", encoding="utf-8"))

    def load_thesaurus(self, fn):
        self.thesaurus = json.load(codecs.open(fn, "r", encoding="utf-8"))

        self.revthesaurus = {}
        for entryid, concepts in self.thesaurus.iteritems():
            for concept in concepts:
                self.revthesaurus.setdefault(concept, set()).add(entryid)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print >> sys.stderr, "usage: <ConceptPairs file> <thesaurus file> <output file>"
        sys.exit(1)

    ca = ThesaurusConceptAggregation(conceptPairs=sys.argv[1], outfn=sys.argv[3])
    ca.load_thesaurus(sys.argv[2])
    ca.run()
