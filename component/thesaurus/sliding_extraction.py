import codecs
import json
import sys

from framework.concept_extraction import ConceptExtraction


class ConceptExtractionSliding(ConceptExtraction):
    """ Sliding window concept extraction component """

    def run(self):
        conceptPairs = {}

        for docid, txt in self.stream_docs():
            for thesaurus_term in self._window_find(txt, winsize=5):
                concept = self.revthesaurus[thesaurus_term]
                conceptPairs.setdefault(concept, set()).add(docid)

        conceptPairs = dict([(k.replace("_", " "), list(v)) for k, v in conceptPairs.iteritems()])
        json.dump(conceptPairs, codecs.open(self.outfn, "w", encoding="utf-8"))

    def load_thesaurus(self, fn):
        self.thesaurus = json.load(codecs.open(fn, "r", encoding="utf-8"))
        synterms = {term: set(term.split("_")) for group in self.thesaurus.values() for term in group}

        self.syndict = {}
        self.synlens = {}
        for p, st in synterms.iteritems():
            for term in st:
                if term not in self.syndict:
                    self.syndict[term] = set()
                self.syndict[term].add(p)
            self.synlens[p] = len(st)

        # note: this is only valid for thesauri with no overlap between entries
        self.revthesaurus = {term: groupname for groupname, terms in self.thesaurus.iteritems() for term in terms}

    def _window_find(self, txt, winsize=50):
        found = set()

        terms = txt.replace("_", " ").split(" ")

        if winsize is None or winsize > len(terms):
            winsize = len(terms)

        for start, end in self._get_windows(txt, winsize=winsize):
            window = terms[start:end]
            termset = set(window)

            found.update(self._terms_present(termset))

        return found

    def _terms_present(self, termset):
        found = set()
        matchlens = {}
        for term in termset:
            if term in self.syndict:
                for p in self.syndict[term]:
                    if p in matchlens:
                        matchlens[p] += 1
                    else:
                        matchlens[p] = 1

        for p, count in matchlens.iteritems():
            if count == self.synlens[p]:
                found.add(p)

        return found

    def _get_windows(self, txt, winsize=None):
        terms = txt.replace("_", " ").split(" ")
        if winsize > len(terms):
            winsize = len(terms)

        windows = []
        for i in range(0, len(terms) - winsize + 1):
            windows.append((i, i + winsize))
        return windows


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print >> sys.stderr, "usage: <docfiles file> <thesaurus file> <output file>"
        sys.exit(1)

    ce = ConceptExtractionSliding(docfiles=sys.argv[1], outfn=sys.argv[3])
    ce.load_thesaurus(sys.argv[2])
    ce.run()
