import codecs
import json
import sys

import lucene

from framework.concept_aggregation import ConceptAggregation


class ConceptAggregationWiki(ConceptAggregation):
    """ Concept aggregation component based on
        J. Parker, Y. Wei, A. Yates, N. Goharian, O. Frieder, "A Framework for Detecting Public Health Trends with Twitter",
        The 2013 IEEE/ACM International Conference on Advances in Social Network Analysis and Mining, August 2013. """

    def run(self):
        aggConceptPairs = {}

        for concept, docids in self.conceptPairs.iteritems():
            hits = self.search(concept)

            for hit in hits[:10]:
                title, intro, infobox = hit
                aggConceptPairs.setdefault(title, set()).update(docids)
                print title, len(docids)

        json.dump({k: list(v) for k, v in aggConceptPairs.iteritems()}, codecs.open(self.outfn, "w", encoding="utf-8"))

    def init_lucene(self, wiki_index):
        lucene.initVM()
        self.version = lucene.Version.LUCENE_35

        self.searcher = lucene.IndexSearcher(lucene.SimpleFSDirectory(lucene.File(wiki_index)))
        self.analyzer = lucene.StandardAnalyzer(self.version)

    def search(self, q):
        if q.find("~") != -1:
            return []

        query = lucene.QueryParser(self.version, "body", self.analyzer).parse(q)
        scoreDocs = self.searcher.search(query, 50).scoreDocs

        hits = []
        for scoreDoc in scoreDocs:
            doc = self.searcher.doc(scoreDoc.doc)
            hits.append((doc.get("doctitle"), doc.get("intro"), doc.get("infoBox")))

        return [hit for hit in hits if self._is_medical(*hit)]

    def _is_medical(self, title, intro, infobox):
        if infobox is not None and (infobox.find("ICD9") != -1 or infobox.find("ICD10") != -1):
            return True
        else:
            return False

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print >> sys.stderr, "usage: <ConceptPairs file> <output file> <path to Lucene index of Wikipedia>"
        print >> sys.stderr, "\tthe Lucene index should contain body, doctitle, infoBox, and intro fields"
        sys.exit(1)

    ca = ConceptAggregationWiki(conceptPairs=sys.argv[1], outfn=sys.argv[2])
    ca.init_lucene(wiki_index=sys.argv[3])
    ca.run()
