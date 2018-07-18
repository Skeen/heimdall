===============
Solr & Haystack
===============

We use solr_ as our search engine for haystack_.
Solr provide us with a quick and efficient way to do text search for different content.
While Haystack provides the necessary glue between Solr and Django.

.. _solr: http://lucene.apache.org/solr/
.. _haystack: http://haystacksearch.org/

Running Solr
------------
While the system does work without Solr running (only searching will stop working).
Solr can easily be started, like any other of our services, by running the
management command;

.. code:: console

    $ python manage.py solr start

Similarily solr can be stopped, by running;

.. code:: console

    $ python manage.py solr stop


Setup Haystack
--------------
Haystack and the pysolr package is installed during the :ref:`installation <Installation>`.
Or you can run the install requirements command again.

.. code:: console

    (venv) $ pip install -r requirements.txt

Adding search to views
----------------------
TODO: Document this


Notes:
------

* We are currently using django-haystack master branch, as the latest version 2.6.0 does not support django 1.11. See django-render_.

* Currently the automatic signal processer, which keeps collection up-to-date,
  is disabled, as it throws a lot of errors during testing, when solr isn't
  running.

.. _django-render: https://stackoverflow.com/questions/37911278/django-warning-removedindjango110warning-render-must-be-called-with-a-dict
