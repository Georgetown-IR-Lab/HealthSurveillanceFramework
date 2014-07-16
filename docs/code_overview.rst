Requirements
============
* Python 2.7
* PyPI packages: fp-growth_, isoweek_, matplotlib_, orange_, pylucene_

.. _fp-growth: https://github.com/enaeseth/python-fp-growth
.. _isoweek: https://github.com/gisle/isoweek
.. _matplotlib: http://matplotlib.org/
.. _orange: http://orange.biolab.si/download/
.. _pylucene: http://lucene.apache.org/pylucene/index.html

File Overview
=============

Python
------
* *framework*: Python abstract classes for implementing the framework's API
* *component*: implementations of concept extraction, concept aggregation, and trend detection components
* *component/example*: simple examples for each type of component

Java
----
* *java/src/healthSurveillanceFramework/fileFormats*: Java classes for parsing input/output files

Data
------------
* *data/example*: synthetic data to run the component examples
* *data/plots*: plots of trends in *data/trends*
* *data/trends*: trend detection method output
* *data/health_tweet_ids.gz*: health-related tweet IDs
