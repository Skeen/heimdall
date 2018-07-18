{
    ##------------------------##
    ## Git included libraries ##
    ##------------------------##
    # Dual licensing - AND or OR?
    # See: https://github.com/rory/django-template-i18n-lint/issues/23
    'django-template-i18n-lint': {
        'licence': [
            {
                'SPDX': 'BSD-3-Clause',
                'link': 'https://github.com/Skeen/django-template-i18n-lint/blob/master/LICENCE.BSD',
            },
            {
                'SPDX': "GPL-3.0",
                'link': 'https://github.com/Skeen/django-template-i18n-lint/blob/master/LICENCE.GPLv3',
            }
        ],
        'homepage': 'https://www.technomancy.org/python/django-template-i18n-lint/',
        'version' : 'forked',
    },

    'django_coverage_plugin': {
        'licence': [{
            'SPDX': 'Apache-2.0',
            'link': 'https://github.com/Skeen/django_coverage_plugin/blob/master/LICENSE.txt',
        }],
        'homepage': 'https://github.com/nedbat/django_coverage_plugin',
        'version' : 'forked',
    },

    'python-pylint-i18n': {
        'licence': [{
            'SPDX': 'GPL-3.0',
            'link': 'https://github.com/Skeen/python-pylint-i18n/blob/master/LICENCE',
        }],
        'homepage': 'https://www.technomancy.org/python/pylint-i18n-lint-checker/',
        'version' : 'forked',
    },

    ##------------------##
    ## Non git included ##
    ##------------------##
    'coverage': {
        'licence': [{
            'SPDX': 'Apache-2.0',
            'link': 'https://github.com/nedbat/coveragepy/blob/coverage-4.4.1/LICENSE.txt',
        }],
        'homepage': 'https://coverage.readthedocs.io',
        'version': '4.4.1',
    },

    'django-debug-toolbar': {
        'licence': [{
            'SPDX': 'BSD-3-Clause',
            'link': 'https://github.com/jazzband/django-debug-toolbar/blob/1.8/LICENSE'
        }],
        'homepage': 'https://django-debug-toolbar.readthedocs.io',
        'version': '1.8',
    },

    'django-slowtests': {
        'licence': [{
            'SPDX': 'MIT',
            'link': 'https://github.com/realpython/django-slow-tests/blob/dee5dfd34b21206e2df3e0e67ced99322efcc72b/LICENSE'
        }],
        'homepage': 'https://github.com/realpython/django-slow-tests',
        'version': '0.5.1',
    },

    'flake8-docstrings': {
        'licence': [{
            'SPDX': 'MIT',
            'link': 'https://gitlab.com/pycqa/flake8-docstrings/blob/1.0.3/LICENSE',
        }],
        'homepage': 'https://gitlab.com/pycqa/flake8-docstrings',
        'version': '1.0.3',
    },

    # See: https://github.com/PyCQA/flake8/pull/12
    'flake8': {
        'licence': [{
            'SPDX': 'MIT',
            'link': 'https://github.com/PyCQA/flake8/blob/3.3.0/LICENSE',
        }],
        'homepage': 'http://flake8.pycqa.org/en/latest/',
        'version': '3.3.0',
    },

    'freezegun': {
        'licence': [{
            'SPDX': 'Apache-2.0',
            'link': 'https://github.com/spulec/freezegun/blob/0.3.9/LICENSE',
        }],
        'homepage': 'https://github.com/spulec/freezegun',
        'version': '0.3.9',
    },

    # Was UNKNOWN: https://github.com/testing-cabal/mock/issues/414
    'mock': {
        'licence': [{
            'SPDX': 'BSD-2-Clause',
            'link': 'https://github.com/testing-cabal/mock/blob/2.0.0/LICENSE.txt',
        }],
        'homepage': 'https://github.com/testing-cabal/mock',
        'version': '2.0.0',
    },

    # Was UNKNOWN: https://github.com/wolever/parameterized/issues/45
    # TODO: Fix licence link, see: https://github.com/wolever/parameterized/issues/46
    'nose-parameterized': {
        'licence': [{
            'SPDX': 'BSD-2-Clause',
            'link': 'https://github.com/wolever/parameterized/blob/master/LICENSE.txt',
        }],
        'homepage': 'https://github.com/wolever/parameterized',
        'version': '0.5.0',
    },

    'pydocstyle': {
        'licence': [{
            'SPDX': 'MIT',
            'link': 'https://github.com/PyCQA/pydocstyle/blob/1.1.1/LICENSE-MIT',
        }],
        'homepage': 'http://www.pydocstyle.org',
        'version': '1.1.1',
    },

    'pylint-django': {
        'licence': [{
            'SPDX': 'GPL-2.0',
            'link': 'https://github.com/landscapeio/pylint-django/blob/0.7.2/LICENSE',
        }],
        'homepage': 'https://github.com/landscapeio/pylint-django',
        'version': '0.7.2',
    },

    'pylint': {
        'licence': [{
            'SPDX': 'GPL-2.0',
            'link': 'https://github.com/PyCQA/pylint/blob/pylint-1.6.5/COPYING',
        }],
        'homepage': 'https://www.pylint.org/',
        'version' : '1.6.5',
    },

    'selenium': {
        'licence': [{
            'SPDX': 'Apache-2.0',
            'link': 'https://github.com/SeleniumHQ/selenium/blob/selenium-3.4.0/LICENSE',
        }],
        'homepage': 'http://www.seleniumhq.org/',
        'version': '3.4.0',
    },

    'sphinx-rtd-theme': {
        'licence': [{
            'SPDX': 'MIT',
            'link': 'https://github.com/rtfd/sphinx_rtd_theme/blob/0.2.4/LICENSE',
        }],
        'homepage': 'https://github.com/rtfd/sphinx_rtd_theme',
        'version': '0.2.4',
    },

    'sphinx': {
        'licence': [
            {
                'SPDX': 'BSD-2-Clause',
                'link': 'https://github.com/sphinx-doc/sphinx/blob/1.5.3/LICENSE',
            },
            {
                'SPDX': 'Python-2.0',
                'link': 'https://github.com/sphinx-doc/sphinx/blob/1.5.3/LICENSE',
            },
            {
                'SPDX': 'BSD-3-Clause',
                'link': 'https://github.com/sphinx-doc/sphinx/blob/1.5.3/LICENSE',
            },
            {
                'SPDX': 'UNKNOWN',
                'name': 'Standard PIL License',
                'link': 'https://github.com/sphinx-doc/sphinx/blob/1.5.3/LICENSE',
            },
            {
                'SPDX': 'MIT',
                'link': 'https://github.com/sphinx-doc/sphinx/blob/1.5.3/LICENSE',
            },
        ],
        'homepage': 'http://www.sphinx-doc.org',
        'version': '1.5.3',
    },

    'sphinxcontrib-napoleon': {
        'licence': [{
            'SPDX': 'BSD-2-Clause',
            'link': 'https://bitbucket.org/birkenfeld/sphinx-contrib/src/napoleon/LICENSE?at=seqdiag-0.6.1'
        }],
        'homepage': 'https://sphinxcontrib-napoleon.readthedocs.io/',
        'version': '0.6.1',
    },
}
