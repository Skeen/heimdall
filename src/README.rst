=====================
Boligadmin - UBSBolig
=====================
Boligadmin is a Django_-based project aimed at maintaining housing assignments,
waiting lists and such. Developed for UBSBolig_. The system is similar in scope
to the findbolig.nu_ and developed by DEAS_.

The focus is on automating currently labor intensive tasks, as thus easing
workloads on employees, and allowing them to focus their time on value creating
activities.

.. _DEAS: https://deas.dk/
.. _findbolig.nu: http://www.findbolig.nu/
.. _UBSBolig: http://www.ubsbolig.dk/da
.. _Django: https://www.djangoproject.com/

Quick Start
===========
Getting started is easy:

* For the brave (or foolhardy), there's an automated setup:

    .. code:: bash

        ./tools/gen_setup.sh | bash

* For the resonable man, there's a guide (for more details, see: :ref:`installation`):

**Note** These instructions are to be run inside the :code:`src` subfolder.

    #. Install the required software packages.

        It is required to have :code:`pip`, :code:`python2.7`, :code:`python-dev` and :code:`gettext` installed.

    #. (Optional) Setup a :code:`virtualenv`.

    #. Install the project dependencies:

        .. code:: bash

            (venv) $ pip install -r requirements.txt

    #. Setup the project:

        .. code:: bash

            (venv) $ ./tools/gen_settings.sh
            (venv) $ python manage.py migrate
     
    #. Ensure everything works:

        .. code:: bash

            (venv) $ ./runtests.sh

    #. Setup git-flow:

        .. code:: bash
            
            (venv) $ ./tools/setup_flow.sh

Using the project
=================
For development the project can be started using (inside the :code:`src` folder):

.. code:: bash

    (venv) $ python manage.py runserver

During so will start a development server running at http://localhost:8000/.

The project has several subpages, but 3 main entry points:

+------------+--------------------------------+----------+----------+
| Identifier | URL                            | Login    | Password |
+------------+--------------------------------+----------+----------+
| Web-app    | http://localhost:8000/         | ubsuser  | ubsuser  |
+------------+--------------------------------+----------+----------+
| Admin-app  | http://localhost:8000/adminapp | ubsadmin | ubsadmin |
+------------+--------------------------------+----------+----------+
| Django-adm | http://localhost:8000/admin    | ubsadmin | ubsadmin |
+------------+--------------------------------+----------+----------+

The :code:`login` and :code:`password` pairs are to login to their specific
subsites.

All applicant users can be logged into, using their username (name before '@'
in their email address), and 'heimdall' as password.
Their email addresses can be found via. their profiles, the admin interface or
the django admin interface.

Getting help
============
If the :ref:`FAQ <faq>` doesn't answer your question, you can try the
developers `IRC channel`_ located at: :code:`#magentaubs @ freenode.net`

.. _IRC channel: http://webchat.freenode.net/?channels=magentaubs&nick=heimdall-visitor
