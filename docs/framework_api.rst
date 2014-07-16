API v1
''''''

The framework consists of three components. Each component's inputs and
outputs are listed in the `components <#components>`__ section; the
input and output files' formats are listed in the `file
formats <#fileformats>`__ section.

Components 
===========

Concept extraction method
-------------------------

Example: *component/example/concept\_extraction\_naive.py*

Input
~~~~~

-  DocumentFiles
-  Thesaurus (optional)

Output
~~~~~~

-  ConceptPairs: one (concept, document id) pair for each concept
   detected

Concept aggregation method
--------------------------

Example: *component/example/concept\_aggregation\_naive.py*

Input
~~~~~

-  ConceptPairs: (Concept, document id) pairs (i.e., the concept
   extraction method's output)
-  Method-specific data sources (optional): a resource needed by the
   method such as Wikipedia or a thesaurus

Output
~~~~~~

-  ConceptPairs: (Higher-level concept, document id) pair for each
   concept in the input

Trend detection method
----------------------

Example: *component/example/trend\_detection\_naive.py*

Input
~~~~~

-  Document metadata
-  ConceptPairs: (Higher-level concept, document id) pairs (i.e., the
   concept aggregation method's output)

Output
~~~~~~

-  TrendTimes: the times at which each concept is trending

File formats 
=============

All files are in JSON format. ## DocumentFiles [ "document\_file\_1",
..., "document\_file\_n" ] A list of JSON `document <#document>`__
files. Each document file may contain many documents, but each should be
small enough to load into memory.

Example: *data/example/docfiles.json*

Documents 
----------

::

    { "document_id_1": <document 1's text>, "document_id_2": <document 2's text>, ... }

Document text is a space-separated string of tokenized text (e.g., "I
have the flu")

Example: *data/example/docs.json*

Document metadata
-----------------

::

    { "document_id_1": { "created_at": <date>, "author": <username> }, ... }

Dates are strings in the `Unix
time <http://en.wikipedia.org/wiki/Unix_time>`__ format, which is the
number of seconds since the epoch (1970-01-01 UTC).

Usernames are strings.

Example: *data/example/docmeta.json*

Thesaurus
---------

::

    { "concept_id_1": ["phrase 1 expressing concept", "phrase 2 expressing concept", ...], ... }

For example, a thesaurus containing only a few phrases about the hair
loss concept might look like this:

::

    { "26": ["bald", "alopecia", "hair_loss"] }

To use a dictionary as input rather than a thesaurus, simply assign only
one phrase to each concept.

Example: *data/example/thesaurus.json*

ConceptPairs
------------

::

    { "concept_id_X": ["document_id_123", "document_id_128", ...],
      "concept_id_Y": ...
    }

Each concept id is mapped to a list of documents it occurs in.

TrendTimes
----------

::

    { "concept_id_X": [ { "start": <date>, "end": <date>, "strength": <strength> },
                        { "start": <date>, "end": <date>, "strength": <strength> },
                        ...
                      ],
      "concept_id_Y": [ { "start": <date>, "end": <date>, "strength": <strength> }, ... ]
    }

