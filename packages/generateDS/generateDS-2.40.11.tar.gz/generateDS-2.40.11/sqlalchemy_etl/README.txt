================================================
Instructions on running the SQLAlchemy support
================================================

**Caution:** WIP -- work in progress.  This work is exploratory.
Use at your own risk.  If you attempt to use it, you will likely
have to make fixes, modifications, and additions.

If you try it and have suggestions or fixes, as with the rest of the
generateDS project, please let me (Dave Kuhlman) know.

Also see:
http://www.davekuhlman.org/generateDS.html#sqlalchemy-generating-models-and-forms


What it does
==============

1. Generates definitions (that is, a model) for the SQLAlchemy
   database ORM from an XML schema.

2. Enables you to load an XML instance document that obeys the XML
   schema into a SQLAlchemy data base.


Create the SQLAlchemy schema
==============================

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

2. Change directory to the ``sqlalchemy_etl`` directory (i.e. the
   directory containing this file)::

       $ cd generateds/sqlalchemy_etl

3. In that directory, either, (a) create, a symbolic link to
   ``generateDS.py`` and another to ``process_includes.py``::

       $ ln -s ../generateDS.py
       $ ln -s ../process_includes.py

   Or, (b) copy ``generateDS.py`` and ``process_includes.py`` to
   that directory::

       $ cp ../generateDS.py .
       $ cp ../process_includes.py .

4. In that directory, Run ``gends_run_gen_sa.py``.  For
   example::

       $ cp ../tests/people.xsd .
       $ ./gends_run_gen_sa.py -f -v people.xsd

If the above ran successfully, it should have created this file:
``models_sqa.py``.

You can use this file to create your SqlAlchemy tables.  You can
find help for doing so here --
https://docs.sqlalchemy.org/en/latest/orm/tutorial.html


Insert/load your data
=======================

This section describes how to extract data from an XML instance
document and load it into an SQLAlchemy database.

1. Generate a Python module containing the ``exportSQLAlchema``
   export methods.  In order to do so, use the "--export" command
   line option.  Example::

       $ generateDS.py --export="write sqlalchemy" -o mymodule.py myschema.xsd

2. Run this generated module under SQLAlchemy.  Example::

       ./db_loader.py create my_sqalchemy_database.db
       ./db_loader.py -d people.xml add my_sqalchemy_database.db

   There is a bash shell script in this directory that will run the
   above.  See: ``./run-load-test.sh``.

You can inspect the data in your new database with something like
the following::

    $ sqlite3 my_sqalchemy_database
    sqlite> .tables
    sqlite> .dump some_table
    sqlite> select * from some_table;

.. vim:ft=rst:
