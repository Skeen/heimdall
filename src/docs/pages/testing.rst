=========================
Testing and Code Coverage
=========================
This project utilizes both Unit-Testing and End-to-End (E2E) testing.

During the installation as mentioned in the :ref:`Quick Start`, or in the
:ref:`Installation` sections of the documentation, setup the environment for
Unit-Testing, but not for running End-to-End tests.

Below will be an introduction into running each kinds of tests, and checking
code coverage.

Running Unit-tests
------------------
This can be done, by running: :code:`./runtests.sh` (for more details, see:
:ref:`runtests.sh`)

.. code:: console

    $ ./runtests.sh

    Creating test database for alias 'default'...
    ..........................................................................................
    ----------------------------------------------------------------------
    Ran 90 tests in 1.804s

    OK
    Destroying test database for alias 'default'...

If the program exists with the line:

* :code:`OK`, all tests passed.
* :code:`FAILED`, some tests failed, and this should be corrected.

Checking code coverage
^^^^^^^^^^^^^^^^^^^^^^
Running the unit-tests as described above, has the side-effect og generating
code-coverage information in the file :code:`.coverage` inside :code:`src`.

This file is not suited for human consumption, but should rather be read using
the `coverage.py`_ program. This can be done by running :code:`coverage report`

.. code:: console

    $ coverage report

    Name                                                      Stmts   Miss Branch BrPart  Cover
    -------------------------------------------------------------------------------------------
    adminapp/admin.py                                             0      0      0      0   100%
    adminapp/apps.py                                              4      0      0      0   100%
    adminapp/templates/adminapp/auth/login.html                  22      0      0      0   100%
    adminapp/templates/adminapp/base.html                        37      0      0      0   100%
    adminapp/templates/adminapp/home.html                        37      0      0      0   100%
    adminapp/templates/adminapp/messages/base_messages.html      14      0      0      0   100%
    adminapp/templates/adminapp/messages/message.html             8      0      0      0   100%
    adminapp/urls.py                                              4      0      0      0   100%
    adminapp/views.py                                            32      0      4      0   100%
    webapp/admin.py                                              41      0      0      0   100%
    ...                                                         ...    ...    ...    ...    ...
    ...                                                         ...    ...    ...    ...    ...
    -------------------------------------------------------------------------------------------
    TOTAL                                                       761      0     14      0   100%

An alternative is to output the coverage report as :code:`html` and view it
using a web-browser, this can be done by running :code:`coverage html` and
opening the generated :code:`htmlcov/index.html` file.

If the coverage is less than 100% in TOTAL, this should be corrected by adding
additional tests (for more details, see: :ref:`Adding tests`).

For :code:`python` files, this can be done by adding tests that directly
exercise the code, while for Django templates :code:`.html`, this can be done by
adding test cases for the Django views resposible for rendering those templates.

.. _coverage.py: https://coverage.readthedocs.io/en/coverage-4.3.4/

Running End-to-End tests
------------------------
This can be done, by running: :code:`./runlivetests.sh` (for more details, see:
:ref:`runlivetests.sh`)

.. code:: console

    $ WebDriver=gecko ./runlivetests.sh 

    Creating test database for alias 'default'...
    ...
    ----------------------------------------------------------------------
    Ran 3 tests in 3.935s

    OK
    Destroying test database for alias 'default'...

If the program exists with the line:

* :code:`OK`, all tests passed.
* :code:`FAILED`, some tests failed, and this should be corrected.

If however the tests do not run, and instead an error occurs, please check
:ref:`runlivetests.sh` for the additional required setup.

It should be noted, that we do not count End-to-End tests towards code coverage,
and that End-to-End testing does therefore not generate coverage results.

Adding tests
------------
Adding additional test cases is a simple task, but to keep the project
consistant, several guidelines are in place, following the below checklist
should help you out.

#. Figure which app you are testing

    The first step is figuring out which app you are testing, whether it is the
    :code:`adminapp` or the :code:`webapp`.
    
    Each has its own test folder, located as:

    * :code:`webapp/tests/` (webapp)
    * :code:`adminapp/tests/` (adminapp)

#. Figure out what you are testing

    The next step is figuring out what you are testing, you may be testing a
    Django view, a Django model, or something else.

    Each entity has a unique tests file, by the name of :code:`{{ENTITY}}tests.py`,
    examples are:

    * :code:`webapp/tests/viewtests/*` (Django views)
    * :code:`webapp/tests/modeltests/*` (Django models)

#. Figure out how you are testing

    This last step is figuring out which method of testing will be utilized,
    either Unit-Testing or End-to-End testing. Unit tests go directly into the
    :code:`tests` subfolder of the project, while End-to-End tests, go into the
    :code:`livetests` subfolder of :code:`tests`.

    Examples:

    * :code:`webapp/tests/viewtests/*` (Unit Tests)
    * :code:`webapp/tests/livetests/viewtests/*` (End-to-End Tests)

