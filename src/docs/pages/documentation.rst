=========================
Documentation (out-dated)
=========================
This documentation is generated using Sphinx_, with the Intersphinx_, autodoc_
and Napoleon_ plugins.

The documentation utilizes the ReadTheDocs_ theme.

.. _Sphinx: http://www.sphinx-doc.org/en/stable/
.. _Intersphinx: http://www.sphinx-doc.org/en/stable/ext/intersphinx.html
.. _autodoc: http://www.sphinx-doc.org/en/stable/ext/autodoc.html
.. _Napoleon: http://sphinxcontrib-napoleon.readthedocs.io/en/latest/index.html
.. _ReadTheDocs: https://github.com/rtfd/sphinx_rtd_theme

Writing documentation
---------------------
Writing documentation is split into two parts;

#. Writing code documentation.
   
    When writing code documentation, the primary way is within the python files
    themselves, using python :code:`docstrings`.
    
    The format utilized for python docstrings in this project, is the
    `Google Style` of `Python Docstrings`. The standard for this can be found
    `here`__.

    It is however not enough to just document the code. Sphinx needs a way to
    find it too, for this purpose several files exist within the
    :code:`docs/modules/` folder.

    All of these files heavily utilize the :code:`autodoc` extension, so one
    should either just follow the presented style, or read the documentation
    provided above for the extension.

    Links to other documentations can be done via. the :code:`Intersphinx`
    extension.

    .. _GoogleStyle: http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
    __ GoogleStyle_

#. Writing generic documentation.

    While writing code documentation should be done at all times, this kind of
    documentation mainly serves as an API or lookup reference, while real solid
    documentation should be written by hand.

    Hand written documentation alike the :ref:`Quick Start` and this site,
    should be added to the :code:`docs/pages` folder.

    These files just utilize the reStructuredText_ language, and a nice lookup
    reference for the language can be found `here`__.

    .. _reStructuredText: http://docutils.sourceforge.net/rst.html
    .. _SphinxReST: http://www.sphinx-doc.org/en/stable/rest.html
    __ SphinxReST_

Generating documentation
------------------------
This documentation can be generated quite easily, after having setup the
developer environment described :ref:`previously <Installation>`

This can be done, by running: :code:`make html` inside :code:`docs`.

.. code:: console

    $ make html

    Running Sphinx v1.5.3
    making output directory...
    loading pickled environment... not yet created
    loading intersphinx inventory from http://python.readthedocs.org/en/v2.7.2/objects.inv...
    ...
    ...
    ...
    build succeeded, 4 warnings.

    Build finished. The HTML pages are in _build/html.

After which the documentation can be viewed locally by opening
:code:`docs/_build/html/index.html`.

