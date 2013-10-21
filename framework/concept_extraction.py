import codecs
import json

from abc import ABCMeta, abstractmethod


class ConceptExtraction(object):
    __metaclass__ = ABCMeta

    def __init__(self, docfiles=None, outfn=None, thesaurus=None):
        """ Args:
        docfiles: a JSON DocumentFiles file
        outfn: the filename to write this component's ConceptPairs output to
        thesaurus (optional): a JSON thesaurus file
        """

        for var in ['docfiles', 'outfn']:
            if eval(var) is None:
                raise TypeError("%s cannot be None" % var)

        self.docfiles = json.load(codecs.open(docfiles, "r", encoding="utf-8"))
        self.outfn = outfn

        if thesaurus is None:
            self.thesaurus = None
        else:
            self.thesaurus = json.load(codecs.open(thesaurus, "r", encoding="utf-8"))

    def open_docfile(self, docfile):
        """ Returns the document in docfile """
        f = codecs.open(docfile, "r", encoding="utf-8")
        doc = json.load(f)
        f.close()

        return doc

    def stream_docs(self):
        """ Generator for iterating over the input documents """
        for docfile in self.docfiles:
            doc = self.open_docfile(docfile)
            for doctup in doc.iteritems():  # should be (docid, text)
                yield doctup

    @abstractmethod
    def run(self):
        """ Runs component and writes output to self.outfn """
        pass
