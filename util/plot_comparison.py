import codecs
import datetime
import json
import sys

from itertools import cycle

import isoweek
import matplotlib.dates as mdates
import matplotlib.pyplot as plt


def get_points(trendtimes, mainconcept, concepts, by_week=False):
    if mainconcept not in trendtimes:
        print "error: missing concept:", mainconcept
        return None, None

    for concept in concepts:
        dates = trendtimes[concept]
        months, weeks = {}, {}
        for point in dates:
            dt = datetime.datetime.fromtimestamp(int(point["start"])).date()
            strength = float(point["strength"])

            if dt.year < 2009 or dt.year > 2010:
                continue

            month = datetime.datetime(dt.year, dt.month, 1)
            months.setdefault(month, []).append(strength)

            week = isoweek.Week(dt.year, dt.isocalendar()[1]).monday()
            weeks.setdefault(week, []).append(strength)

    xs, ys = [], []

    if by_week:
        times = weeks
    else:
        times = months

    for timeperiod, points in sorted(times.iteritems()):
        xs.append(timeperiod)
        ys.append(sum(points))

    return (xs, ys)

# from http://stackoverflow.com/questions/7799156/can-i-cycle-through-line-styles-in-matplotlib
lines = ["o-", "s--", "v-.", "^:"]
linecycler = cycle(lines)

methods = {"data/trends/trends-parker_ca-parker_ce": (False, "Term Sets\n+ Wiki"),
           "data/trends/trends-parker_ca-thesaurus_ce": (True, "Term Sets\n+ Thesaurus"),
           "data/trends/trends-sw_ca-parker_ce": (False, "Sliding Window\n+ Wiki"),
           "data/trends/trends-sw_ca-thesaurus_ce": (True, "Sliding Window\n+ Thesaurus")}

conceptnames = {"Flu": ("flu", "Influenza"), "Allergy": ("allergic hypersensitivity", "Allergy")}

import itertools
conpoints = {}
for targetcon in conceptnames.keys():
    for tp in ("Monthly", "Weekly"):
        for m1, m2 in itertools.combinations(methods.keys(), 2):
            plt.close('all')

            plt.title("%s (%s)" % (targetcon, tp))
            plt.xlabel("Date")
            plt.ylabel("Strength")
            plt.ylim(0, 1.1)

            for ttfn in sorted([m1, m2]):
                isThes, n = methods[ttfn]
                tt = json.load(codecs.open(ttfn, "r", encoding="utf-8"))

                if isThes:
                    c = conceptnames[targetcon][0]
                else:
                    c = conceptnames[targetcon][1]

                if tp == "Monthly":
                    by_week = False
                elif tp == "Weekly":
                    by_week = True
                else:
                    print >> sys.stderr, "INVALID TP", tp
                    sys.exit(2)

                if (targetcon, tp) in conpoints and ttfn in conpoints[(targetcon, tp)]:
                    continue

                print ttfn
                cs = set([c])

                xs, ys = get_points(tt, c, cs, by_week=by_week)
                if xs is None or ys is None:
                    continue

                ys = [y / max(ys) for y in ys]
                conpoints.setdefault((targetcon, tp), {})[ttfn] = (xs, ys, n)

            for m in sorted([m1, m2]):
                xs, ys, label = conpoints[(targetcon, tp)][m]
                plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
                plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
                plt.gcf().autofmt_xdate(rotation=60)
                plt.plot(xs, ys, next(linecycler), label=label)

            fn = "%s_%s_%s" % (targetcon, tp, "_".join((m1, m2)))

            plt.legend(loc='upper left')
            plt.savefig("data/plots/%s.png" % fn, dpi=300)
            plt.savefig("data/plots/%s.pdf" % fn, dpi=300)
            plt.close()

        plt.close('all')
        plt.title("%s (%s)" % (targetcon, tp))
        plt.xlabel("Date")
        plt.ylabel("Strength")
        plt.ylim(0, 1.1)

        for m in sorted(methods.keys()):
            xs, ys, label = conpoints[(targetcon, tp)][m]

            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
            plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
            plt.gcf().autofmt_xdate(rotation=60)

            plt.plot(xs, ys, next(linecycler), label=label)

        fn = "%s_%s_%s" % (targetcon, tp, "all")

        plt.legend(loc='upper right')
        plt.savefig("data/plots/%s.png" % fn, dpi=300)
        plt.savefig("data/plots/%s.pdf" % fn, dpi=300)
        plt.close()
