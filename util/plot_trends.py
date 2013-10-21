# plots TrendTimes if start=end; doesn't handle collapsed times
import codecs
import datetime
import json
import os
import sys

import matplotlib.dates as mdates
import matplotlib.pyplot as plt


if len(sys.argv) != 2:
    print >> sys.stderr, "usage: <TrendTimes file>"
    sys.exit(1)

trendtimes = json.load(codecs.open(sys.argv[1], "r", encoding="utf-8"))

if not os.path.exists("data/plots/"):
    os.mkdir("data/plots/")

for concept, dates in trendtimes.iteritems():
    fn = concept.replace(" ", "_") + ".png"
    print fn

    xs, ys = [], []
    for point in dates:
        xs.append(datetime.datetime.fromtimestamp(int(point["start"])).date())
        ys.append(float(point["strength"]))

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %d, %Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.scatter(xs, [y / max(ys) for y in ys])
    plt.gcf().autofmt_xdate(rotation=90)

    plt.xlabel("Date")
    plt.ylabel("Strength")
    plt.ylim(0, 1.1)
    plt.show()
    break
