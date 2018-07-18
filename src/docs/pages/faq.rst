.. _faq:

==========================
Frequently Asked Questions
==========================
**Q: I'm getting the error "attempt to write a readonly database". Why?**

This error occurs when Django is unable to access the :code:`db.sqlite3`
database inside the :code:`src` folder. This is usually a case of bad
permission and/or user/group configuration.

A proper configuration should have both the read and write flag set
(:code:`rw`), for the user running the code:

.. code:: console

    $ ls -lh db.sqlite3

    -rw-r--r-- 1 username username 156K Mar 23 12:52 db.sqlite3

When running in a WSGI_ setup, like the UBSDev server, it is necessary to set
the permission as :code:`-rw-rw-r--` or :code:`664`, and to change the group
owner of the files to :code:`www-data`, such that the WSGI server user can write
the database file.

.. code:: console

    $ ls

    autogen/  doc/  LICENSE  README.md  src/

    $ sudo chown :www-data -R .
    $ sudo chmod 664 src/db.sqlite3

.. _WSGI: https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface

**Q: I'm getting the error "RuntimeError: dictionary changed size during iteration" while running runtests.py. Why?**

We are not quite sure why this error occurs, however we know that it is related to the virtual environment that is being used.
So the solution is to create a new virtual environment and use that instead.

**Q: I am trying to translate a label for a FormView in views.py and it is not being translated. Why?**

This is likely because the translation is being executed during parsing, instead of when the view is activated.
This can be fixed by importing ugettext_lazy instead of ugettext. 

**Q: I'm getting the error
"NoReverseMatch: 'en-us' is not a registered namespace". Why?**

Fix this by clearing your DB and rerun
:code:`python manage.py migrate`.


**Q: When running tests, I get:
" \'module\' object has no attribute \'tests\' ". Why?**

.. code:: console

    Traceback (most recent call last):
      File "./tools/runtests.py", line 65, in <module>
        main()
      File "./tools/runtests.py", line 56, in main
        'adminapp.tests',
      File "[...]/site-packages/django/test/runner.py", line 548, in run_tests
        suite = self.build_suite(test_labels, extra_tests)
      File "[...]/site-packages/django/test/runner.py", line 437, in build_suite
        tests = self.test_loader.loadTestsFromName(label)
      File "/usr/lib/python2.7/unittest/loader.py", line 100, in loadTestsFromName
        parent, obj = obj, getattr(obj, part)
    AttributeError: 'module' object has no attribute 'tests'
    No data to combine

This might be due to an import error that is obscured by django.
Try running:

.. code:: console

    $ ./tools/import_tests.py

Or alternatively try open a manage.py shell and try importing the tests
to get a more accurate error message.

.. code:: console

    $ python manage.py shell
    $ import webapp.tests


**Q: I am getting "Permission denied" when trying to start solr. Why?**

.. code:: console

    $ python manage.py solr start

    Traceback (most recent call last):
      File "manage.py", line 44, in <module>
        main()
      File "manage.py", line 40, in main
        execute_from_command_line(sys.argv)
      File "/home/danni/Development/UBSBolig/test_boliga/heimdall/venv/local/lib/python2.7/site-packages/django/core/management/__init__.py", line 363, in execute_from_command_line
        utility.execute()
      File "/home/danni/Development/UBSBolig/test_boliga/heimdall/venv/local/lib/python2.7/site-packages/django/core/management/__init__.py", line 355, in execute
        self.fetch_command(subcommand).run_from_argv(self.argv)
      File "/home/danni/Development/UBSBolig/test_boliga/heimdall/venv/local/lib/python2.7/site-packages/django/core/management/base.py", line 283, in run_from_argv
        self.execute(*args, **cmd_options)
      File "/home/danni/Development/UBSBolig/test_boliga/heimdall/venv/local/lib/python2.7/site-packages/django/core/management/base.py", line 330, in execute
        output = self.handle(*args, **options)
      File "/home/danni/Development/UBSBolig/test_boliga/heimdall/src/core/management/ServiceCommand.py", line 65, in handle
        if self.is_running(identifier) and options['force'] is False:
      File "/home/danni/Development/UBSBolig/test_boliga/heimdall/src/core/management/DockerService.py", line 104, in is_running
        container = self.client.containers.get(identifier)
      File "/home/danni/Development/UBSBolig/test_boliga/heimdall/venv/local/lib/python2.7/site-packages/docker/models/containers.py", line 723, in get
        resp = self.client.api.inspect_container(container_id)
      File "/home/danni/Development/UBSBolig/test_boliga/heimdall/venv/local/lib/python2.7/site-packages/docker/utils/decorators.py", line 21, in wrapped
        return f(self, resource_id, *args, **kwargs)
      File "/home/danni/Development/UBSBolig/test_boliga/heimdall/venv/local/lib/python2.7/site-packages/docker/api/container.py", line 748, in inspect_container
        self._get(self._url("/containers/{0}/json", container)), True
      File "/home/danni/Development/UBSBolig/test_boliga/heimdall/venv/local/lib/python2.7/site-packages/docker/utils/decorators.py", line 47, in inner
        return f(self, *args, **kwargs)
      File "/home/danni/Development/UBSBolig/test_boliga/heimdall/venv/local/lib/python2.7/site-packages/docker/api/client.py", line 183, in _get
        return self.get(url, **self._set_request_timeout(kwargs))
      File "/home/danni/Development/UBSBolig/test_boliga/heimdall/venv/local/lib/python2.7/site-packages/requests/sessions.py", line 526, in get
        return self.request('GET', url, **kwargs)
      File "/home/danni/Development/UBSBolig/test_boliga/heimdall/venv/local/lib/python2.7/site-packages/requests/sessions.py", line 513, in request
        resp = self.send(prep, **send_kwargs)
      File "/home/danni/Development/UBSBolig/test_boliga/heimdall/venv/local/lib/python2.7/site-packages/requests/sessions.py", line 623, in send
        r = adapter.send(request, **kwargs)
      File "/home/danni/Development/UBSBolig/test_boliga/heimdall/venv/local/lib/python2.7/site-packages/requests/adapters.py", line 490, in send
        raise ConnectionError(err, request=request)
    requests.exceptions.ConnectionError: ('Connection aborted.', error(13, 'Permission denied'))

In this particular case it is the docker.sock file which is owned by root. You can find it in folder /var/run.
Change the owner to the user running the command.

.. code:: console

    $ sudo chown user:user docker.sock

You can also check permission for the solr instance in /opt/solr and in /var/solr if the above command does not solve your problem.

**Q: I'm getting the error "django.core.exceptions.ImproperlyConfigured: Requested setting DEFAULT_INDEX_TABLESPACE, but settings are not configured." when running gen_data.py. Why?**

If you inserted model imports at the top of gen_data.py, this error will occur. They should be placed locally in the method where they are used.
