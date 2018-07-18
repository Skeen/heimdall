Tools
=====
tools.filter_files
------------------
.. automodule:: tools.filter_files
    :members:

tools.find_files
----------------
.. automodule:: tools.find_files
    :members:

tools/gen_settings.sh
---------------------
Tool for generating `heimdall/settings.py`, overriding configuration
specific options.

Utilizes :ref:`tools.secret_key`.

tools.secret_key
------------------
.. automodule:: tools.secret_key
    :members:

tools/gen_setup.sh
------------------
Tool for parsing :ref:`installation`, pulling out information on how to setup the
project.

Can be run directly to setup a developer environment as:

.. code:: bash

    ./tools/gen_setup.sh | bash

tools/install_chromedriver.sh
-----------------------------
Install the chromedriver for selenium into a currently active virtual
environment.

.. code:: bash

    ./tools/install_chromedriver.sh


tools/install_geckodriver.sh
-----------------------------
Install the geckodriver for selenium into a currently active virtual
environment.

.. code:: bash

    ./tools/install_geckodriver.sh


tools/reverse_model_checker.sh
------------------------------
Checks reverse references on Django models are in place, and following the
prespecified format (:code:`# {{NAME}} = incoming foreign key from {{TYPE}}`).

Can be run by:

.. code:: bash

    $ ./tools/reverse_model_checker.sh webapp/models/

    Filename                      related_name                  Missing type                  
    ========================================================================
    ApplicationTarget.py          applications                  Application                   
    ApprobationCommittee.py       buildings                     Building                      
    ...                           ...                           ...
    Building.py                   tenancies                     Tenancy                       
    TenancyGroup.py               tenancies                     Tenancy                       

    ^^-- Files which are missing related_name comment (with Type) --^^

Note: Requires models to be seperate :code:`.py` files in the folder.

../jenkins/jenkins.sh
---------------------
Script to be run inside docker isolation when running on Jenkins.

Setups a developer environment using :ref:`tools/gen_setup.sh`, activates it,
and runs all the analysis and checks available.

tools/runtests.py
-----------------
See :ref:`runtests.sh`.

tools/runlivetests.py
---------------------
See :ref:`runlivetests.sh`.

tools/setup_flow.sh
-------------------
Configure git-flow according to the Magenta standard.

tools/setup_postgres.sh
-----------------------
Configure the project to utilize postgresql instead of sqlite3.

Changes are made to heimdall/settings.py
