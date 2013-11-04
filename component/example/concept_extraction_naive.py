import codecs
import json
import sys

from framework.concept_extraction import ConceptExtraction


class ConceptExtractionNaive(ConceptExtraction):
    """ Concept extraction component that returns every term as a concept """

    def run(self):
        conceptPairs = {}

        # treat every term as a concept
        for docid, txt in self.stream_docs():
            for term in set(txt.split(" ")):
                if term not in conceptPairs:
                    conceptPairs[term] = set()

                conceptPairs[term].add(docid)

        conceptPairs = dict([(k, list(v)) for k, v in conceptPairs.iteritems()])
        json.dump(conceptPairs, codecs.open(self.outfn, "w", encoding="utf-8"))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print >> sys.stderr, "usage: <docfiles file> <output file>"
        sys.exit(1)

    ce = ConceptExtractionNaive(docfiles=sys.argv[1], outfn=sys.argv[2])
    ce.run()
