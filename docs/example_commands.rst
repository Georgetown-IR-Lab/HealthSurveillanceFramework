Commands
========
Plotting
--------
* Plot trends from a TrendTimes file: *python -m util.plot_trends <TrendTimes file>*
* Plot trends from the *data/trends/* trend detection files: *python -m util.plot_comparison*
Example components
------------------
* Concept extraction: *python -m component.example.concept_extraction_naive data/example/docfiles.json ce*
* Concept aggregation: *python -m component.example.concept_aggregation_naive ce data/example/thesaurus.json ca*
* Trend detection: *python -m component.example.trend_detection_naive data/example/docmeta.json ca td*
