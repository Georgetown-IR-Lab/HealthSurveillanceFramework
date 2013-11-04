import calendar
import codecs
import datetime
import json
import sys

import isoweek

from framework.trend_detection import TrendDetection


class WeeklyTrendDetection(TrendDetection):
    """ Trend detection component that returns all detected concepts as weekly trends regardless of frequency """

    def run(self):

        # map concept -> (date -> count)
        trends = {}
        for concept, docids in self.conceptPairs.iteritems():
            if concept not in trends:
                trends[concept] = {}

            for docid in docids:
                date = datetime.datetime.fromtimestamp(self.docMeta[docid]['created_at']).date()

                if date not in trends[concept]:
                    trends[concept][date] = 1
                else:
                    trends[concept][date] += 1

        # output trends
        trendsout = {}
        for concept, datecounts in trends.iteritems():
            if concept not in trendsout:
                trendsout[concept] = []

            for date, count in datecounts.iteritems():
                week = isoweek.Week(date.year, date.isocalendar()[1]).monday()
                unixtime = calendar.timegm(week.timetuple())
                trendsout[concept].append({"start": unixtime, "end": unixtime, "strength": count})

        json.dump(trendsout, codecs.open(self.outfn, "w", encoding="utf-8"))

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print >> sys.stderr, "usage: <document metadata file> <ConceptPairs file> <output file>"
        sys.exit(1)

    td = WeeklyTrendDetection(docMeta=sys.argv[1], conceptPairs=sys.argv[2], outfn=sys.argv[3])
    td.run()
