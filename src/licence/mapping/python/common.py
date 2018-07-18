{
    'celery': {
        'licence': [{
            'SPDX': 'BSD-3-Clause', 
            'link': 'https://github.com/celery/celery/blob/v4.1.0/LICENSE',
        }],
        'homepage': 'http://celeryproject.org',
        'version': '4.1.0',
    },

    # TODO: Fix licence link, see: https://github.com/brack3t/django-braces/issues/230
    'django-braces': {
        'licence': [{
            'SPDX': 'BSD-3-Clause',
            'link': 'https://github.com/brack3t/django-braces/blob/master/LICENSE',
        }],
        'homepage': 'https://django-braces.readthedocs.io',
        'version': '1.11.0',
    },

    'django-celery-beat': {
        'licence': [{
            'SPDX': 'BSD-3-Clause',
            'link': 'https://github.com/celery/django-celery-beat/blob/v1.1.0/LICENSE',
        }],
        'homepage': 'http://django-celery-beat.readthedocs.io',
        'version': '1.1.0',
    },

    # TODO: Fix licence link, see: https://github.com/Tivix/django-common/issues/39
    # See: https://github.com/Tivix/django-common/issues/38
    'django-common': {
        'licence': [{
            'SPDX': 'MIT',
            'link': 'https://github.com/Tivix/django-common/blob/master/LICENSE',
        }],
        'homepage': 'https://github.com/Tivix/django-common',
        'version': '0.1.51',
    },

    'django-extensions': {
        'licence': [{
            'SPDX':  'MIT',
            'link': 'https://github.com/django-extensions/django-extensions/blob/1.7.7/LICENSE',
        }],
        'homepage': 'https://django-extensions.readthedocs.io',
        'version': '1.7.7',
    },

    'django-extra-views': {
        'licence': [{
            'SPDX': 'MIT',
            'link': 'https://github.com/AndrewIngram/django-extra-views/blob/0.9.0/LICENSE',
        }],
        'homepage': 'https://django-extra-views.readthedocs.io',
        'version': '0.9.0',
    },

    'django-filter': {
        'licence': [{
            'SPDX': 'BSD-3-Clause',
            'link': 'https://github.com/carltongibson/django-filter/blob/1.0.4/LICENSE',
        }],
        'homepage': 'https://django-filter.readthedocs.io',
        'version': '1.0.4',
    },

    'django-haystack': {
        'licence': [{
            'SPDX': 'BSD-3-Clause',
            'link': 'https://github.com/django-haystack/django-haystack/blob/v2.8.1/LICENSE',
        }],
        'homepage': 'https://django-haystack.readthedocs.io',
        'version' : '2.8.1',
    },

    'django-recaptcha': {
        'licence': [{
            'SPDX': 'BSD-3-Clause',
            'link': 'https://github.com/praekelt/django-recaptcha/blob/1.3.1/LICENSE',
        }],
        'homepage': 'https://github.com/praekelt/django-recaptcha',
        'version': '1.3.1',
    },

    # Was UNKNOWN: https://github.com/treyhunner/django-simple-history/issues/321
    'django-simple-history': {
        'licence': [{
            'SPDX': 'BSD-3-Clause',
            'link': 'https://github.com/treyhunner/django-simple-history/blob/1.9.0/LICENSE.txt',
        }],
        'homepage': 'https://django-simple-history.readthedocs.io',
        'version': '1.9.0',
    },

    'django-split-settings': {
        'licence': [{
            'SPDX': 'BSD-3-Clause',
            'link': 'https://github.com/sobolevn/django-split-settings/blob/v0.3.0/LICENSE.txt',
        }],
        'homepage': 'https://github.com/sobolevn/django-split-settings',
        'version': '0.3.0',
    },

    'django-tinymce': {
        'licence': [{
            'SPDX': 'MIT',
            'link': 'https://github.com/aljosa/django-tinymce/blob/2.6.0/LICENSE.txt',
        }],
        'homepage': 'https://django-tinymce.readthedocs.io',
        'version': '2.6.0',
    },

    # See: https://github.com/django/django/pull/9263
    'django': {
        'licence': [{
            'SPDX': 'BSD-3-Clause',
            'link': 'https://github.com/django/django/blob/1.11.1/LICENSE',
        }],
        'homepage': 'https://www.djangoproject.com/',
        'version': '1.11.1',
    },

    'djangorestframework': {
        'licence': [{
            'SPDX': 'BSD-2-Clause',
            'link': 'https://github.com/encode/django-rest-framework/blob/3.6.3/LICENSE.md',
        }],
        'homepage': 'http://www.django-rest-framework.org/',
        'version': '3.6.3',
    },

    # Was UNKNOWN: https://github.com/docker/docker-py/issues/1779
    'docker': {
        'licence': [{
            'SPDX': 'Apache-2.0',
            'link': 'https://github.com/docker/docker-py/blob/2.2.1/LICENSE',
        }],
        'homepage': 'https://docker-py.readthedocs.io',
        'version': '2.2.1',
    },

    'pika': {
        'licence': [{
            'SPDX': 'BSD-3-Clause',
            'link': 'https://github.com/pika/pika/blob/0.10.0/LICENSE',
        }],
        'homepage': 'https://pika.readthedocs.io/',
        'version': '0.10.0',
    },

    # License seems capatible with MIT
    'pillow': {
        'licence': [{
            'SPDX': 'UNKNOWN',
            'name': 'Standard PIL License',
            'link': 'https://github.com/python-pillow/Pillow/blob/4.1.1/LICENSE',
        }],
        'homepage': 'https://pillow.readthedocs.io',
        'version': '4.1.1',
    },

    'psycopg2': {
        'licence': [
            {
                'SPDX': 'LGPL-3.0',
                'link': 'http://initd.org/psycopg/license/',
            },
            {
                'SPDX': 'UNKNOWN',
                'name': 'BSD / Zope',
                'link': 'http://initd.org/psycopg/license/',
            },
        ],
        'homepage': 'http://initd.org/psycopg/',
        'version': '2.7.1',
    },

    'pysolr': {
        'licence': [{
            'SPDX': 'BSD-3-Clause',
            'link': 'https://github.com/django-haystack/pysolr/blob/v3.6.0/LICENSE',
        }],
        'homepage': 'https://github.com/django-haystack/pysolr',
        'version': '3.6.0',
    },

    'python-dateutil': {
        'licence': [{
            'SPDX': 'BSD-3-Clause',
            'link': 'https://github.com/dateutil/dateutil/blob/2.6.1/LICENSE',
        }],
        'homepage': 'https://dateutil.readthedocs.io',
        'version' : '2.6.1',
    },

    'python-json-logger': {
        'licence': [{
            'SPDX': 'BSD-2-Clause',
            'link': 'https://github.com/madzak/python-json-logger/blob/v0.1.8/LICENSE',
        }],
        'homepage': 'https://github.com/madzak/python-json-logger/',
        'version' : '0.1.8',
    },

    'tblib': {
        'licence': [{
            'SPDX': 'BSD-2-Clause',
            'link': 'https://github.com/ionelmc/python-tblib/blob/v1.3.1/LICENSE',
        }],
        'homepage': 'https://python-tblib.readthedocs.io',
        'version': '1.3.1',
    },

    'tzlocal': {
        'licence': [{
            'SPDX': 'MIT',
            'link': 'https://github.com/regebro/tzlocal/blob/1.4/LICENSE.txt',
        }],
        'homepage': 'https://github.com/regebro/tzlocal',
        'version': '1.4',
    },

    'django-modeltranslation': {
        'licence': [{
            'SPDX': 'BSD-3-Clause',
            'link': 'https://github.com/deschler/django-modeltranslation/blob/0.12.1/LICENSE.txt',
        }],
        'homepage': 'https://github.com/deschler/django-modeltranslation',
        'version': '0.12.1',
    },

    'enum34': {
        'licence': [{
            'SPDX': 'BSD-3-Clause',
            'link': 'https://bitbucket.org/stoneleaf/enum34/raw/58c4cd7174ca35f164304c8a6f0a4d47b779c2a7/enum/LICENSE',
        }],
        'homepage': 'https://pypi.org/project/enum34/',
        'version' : '1.1.6',
    },
}
