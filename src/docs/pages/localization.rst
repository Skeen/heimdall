============
Localization
============
In this project we have decided to have all text strings written in english through out the code.
This has been chosen so we are forced to localize every text string, and for future support of multiple languages.

The localization tool in django produces to files for each language needed. A .po and .mo.
The .mo file is text representation of all the text string found throughout the project. Is text string consist of a message key and a translation.
When the .mo file is generated for your needed language you need to find the messages keys you have just added and translate them.
When everything has been translated you can generate the .po files, which is a compiled version of the .mo file.

Generate localization files
---------------------------
This can be done, by running: :code:`../compile_messages.sh` (for more details, see:
:ref:`compile_messages.sh`) from the inside the folder you need to localize.

.. code:: console

    $ ../compile_messages.sh

This will update all the already existing language packages within the locale folder.

You can add a new language by running:

.. code:: console

    $ ../manage.py makemessages -l %language_code%

To check that all text string have been executed run the following from the src folder:

.. code:: console

    $ ./find_missing_translations.sh
