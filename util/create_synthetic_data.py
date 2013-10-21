import calendar
import datetime
import json
import math
import random


def datediff(start, end):
    return int((end - start).days)


def daterange(start, end):
    for n in range(datediff(start, end)):
        yield start + datetime.timedelta(n)

databegin = datetime.datetime.strptime("01 01 01", "%d %m %y")
dataend = datetime.datetime.strptime("01 05 01", "%d %m %y")

flubegin = datetime.datetime.strptime("01 02 01", "%d %m %y")
flupeak = datetime.datetime.strptime("01 03 01", "%d %m %y")
fluend = datetime.datetime.strptime("15 03  01", "%d %m %y")
fluuplen = datediff(flubegin, flupeak)
fludownlen = datediff(flupeak, fluend)

fluterms = json.load(open("data/example/thesaurus.json"))["flu"]
okterms = ["fine", "bieber", "music", "happy", "follow", "friends", "party", "excellent",
           "good", "beer", "college", "biology", "python", "lol", "emacs", "hm"]

doclen = 9
maxflulen = doclen - 3
docs = {}
docmeta = {}
docid = 1
for date in daterange(databegin, dataend):
    for x in range(100):
        if date < flubegin or date > fluend:
            doc = random.sample(okterms, doclen)
        else:
            if date <= flupeak:
                progress = float(datediff(flubegin, date) + 1) / fluuplen
            else:
                progress = float(datediff(date, fluend) + 1) / fludownlen

            flulen = int(math.ceil(maxflulen * progress))
            doc = random.sample(okterms, doclen - flulen) + random.sample(fluterms, flulen)

        docs[docid] = " ".join(doc)
        docmeta[docid] = {"created_at": calendar.timegm(date.utctimetuple()),
                          "author": "synthetic"}
        docid += 1

docfn = "data/example/docs.json"
json.dump([docfn], open("data/example/docfiles.json", "w"))
json.dump(docs, open(docfn, "w"))
json.dump(docmeta, open("data/example/docmeta.json", "w"))
