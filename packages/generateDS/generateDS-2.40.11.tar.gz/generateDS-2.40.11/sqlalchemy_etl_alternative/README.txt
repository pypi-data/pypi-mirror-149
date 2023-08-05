================================================
Instructions on running the SQLAlchemy support
================================================

Introduction
==============

**Note:** The code in this directory is experimental.  It is a work
in progress.

This is an alternative implementation of the support for (1)
creating models for SQLAlchemy from XML schemas and (2) loading data
from an XML instance doc into an SQLAlchemy database.

Also see:
http://www.davekuhlman.org/generateDS.html#django-generating-models


Instructions
==============

Although, there are likely other configurations that will work, one
reasonably simple way is the following:

1. Download the source distribution of generateDS with the
   following::

       $ hg clone https://dkuhlman@bitbucket.org/dkuhlman/generateds

   Alternatively, you can download a Zip file from here:
   https://bitbucket.org/dkuhlman/generateds/downloads/

   Or, a tar file from here:
   https://pypi.python.org/pypi/generateDS

   And, then unroll it.

2. Change directory to the ``sa`` directory (i.e. the directory
   containing this file)::

       $ cd generateds/sa

3. In that directory, either, (a) create, a symbolic link to
   ``generateDS.py``::

       $ ln -s ../generateDS.py

   Or, (b) copy ``generateDS.py`` to that directory::

       $ cp ../generateDS.py .

4. In that directory, Run ``gends_run_gen_sa.py``.  For
   example::

       $ cp ../tests/people.xsd .
       $ ./gends_run_gen_sa.py -f -v people.xsd

If the above ran successfully, it should have created these files::

    models.py
    main.py


.. vim:ft=rst:
