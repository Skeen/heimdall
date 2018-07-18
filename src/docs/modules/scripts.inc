Scripts
=======
manage.py
---------
.. automodule:: manage
    :members:

runtests.sh
-----------
.. automodule:: tools.runtests
    :members:

runlivetests.sh
---------------
.. automodule:: tools.runlivetests
    :members:

lint.sh
-------
Tool for linting all python files of interest.

Utilizes:

* :ref:`tools.find_files`
* :ref:`tools.filter_files`
* Pylint_
* PylintDjango_

.. _Pylint: https://www.pylint.org/
.. _PylintDjango: https://github.com/landscapeio/pylint-django

Note:

    The `_cont` version, does continuous checking; firing the checker on file
    changes.

i18nlint.sh
-----------
Tool for linting all python files of interest for localization issues

Utilizes:

* :ref:`tools.find_files`
* :ref:`tools.filter_files`
* Pylint_
* PylintDjango_
* PylintI18N_

.. _Pylint: https://www.pylint.org/
.. _PylintDjango: https://github.com/landscapeio/pylint-django
.. _PylintI18N: https://www.technomancy.org/python/pylint-i18n-lint-checker/

pycodestyle.sh
--------------
Tool for PEP8 style checking all python files of interest.

Utilizes:

* :ref:`tools.find_files`
* :ref:`tools.filter_files`
* pycodestyle_

.. _pycodestyle: http://pycodestyle.pycqa.org/en/latest/

Note:

    The `_cont` version, does continuous checking; firing the checker on file
    changes.

i18nlint_templates.sh
---------------------
Tool for checking Django templates for missing :code:`{% trans '...' %}` tags.

Utilizes:

* :ref:`tools.find_files`
* :ref:`tools.filter_files`
* TemplateLint_

.. _TemplateLint: https://github.com/Skeen/django-template-i18n-lint

find_missing_i18n.sh
--------------------
Tool for finding Django template files, which utilize the translation tag
(:code:`{% trans '...' %}`), but does not include the :code:`i18n` library.

Utilizes:

* :ref:`tools.find_files`
* :ref:`tools.filter_files`

find_missing_translations.sh
----------------------------
Tool for reporting whether non-translated strings exist.

compile_messages.sh
-------------------
Tool for pulling out messages / translation tags, updating :code:`/locale/...`
and compiling them for use.

../jenkins.sh
-------------
Entry point for Jenkins CI, utilizes :ref:`../jenkins/jenkins.sh`

gen_data.sh
-----------
Generate testing data for the database. Utilizes the :code:`webapp.models.gen`
scripts to do so.

check.sh
--------
Tool for running all available subcheckers.

Checks:

* Missing i18n headers
* Missing translations
* Linting and PEP8
