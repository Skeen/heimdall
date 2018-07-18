==========
Code Style
==========
To ensure consistency across the codebase, a common code style will be utilized.

For this project the PEP8_ style will be utilized. A tool is in place to check
whether the codebase is currently fulfilling the required codestyle. See
:ref:`Check PEP8 compliance`.

Additionally code will be statically analyzed using the pylint_ tool, this tool
checks for many pitfalls and ensures that the code fulfills several invariants
with regards to documentation, formatting and functionality. See :ref:`Linting
the code`.

.. _PEP8: https://www.python.org/dev/peps/pep-0008/
.. _pylint: https://www.pylint.org/

Checking everything
-------------------
All checks that are available can be run using :code:`./check.sh` (for more
details, see: :ref:`check.sh`)

.. code:: console

    $ ./check.sh

    ************* Module webapp.tests.viewtests
    W: 63, 0: Unnecessary semicolon (unnecessary-semicolon)
    W: 63, 8: Redundant use of assertTrue with constant value True (redundant-unittest-assert)
    ./webapp/tests/viewtests.py:23:1: E302 expected 2 blank lines, found 1
    ./webapp/tests/viewtests.py:37:50: E703 statement ends with a semicolon

If the program does:

* not produce any output; the code does not contain any linting issues
* does produce output; it will be as in the above example, descriptions of the
  errors, and instructions on how to make the code compliant.

Check PEP8 compliance
---------------------
This can be done, by running: :code:`./pycodestyle.sh` (for more details, see:
:ref:`pycodestyle.sh`)

.. code:: console

    $ ./pycodestyle.sh

    ./webapp/tests/viewtests.py:23:1: E302 expected 2 blank lines, found 1
    ./webapp/tests/viewtests.py:37:50: E703 statement ends with a semicolon

If the program does:

* not produce any output; the code is compliant.
* does produce output; it will be as in the above example, descriptions of the
  errors, and instructions on how to make the code compliant.

Linting the code
----------------
This can be done, by running: :code:`./lint.sh` (for more details, see:
:ref:`lint.sh`)

.. code:: console

    $ ./lint.sh

    ************* Module webapp.tests.viewtests
    W: 63, 0: Unnecessary semicolon (unnecessary-semicolon)
    W: 63, 8: Redundant use of assertTrue with constant value True (redundant-unittest-assert)

If the program does:

* not produce any output; the code does not contain any linting issues
* does produce output; it will be as in the above example, descriptions of the
  errors, and instructions on how to make the code compliant.
