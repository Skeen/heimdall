# flake8: noqa # pylint: skip-file
from __future__ import unicode_literals

from django.apps import AppConfig
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        # Try to set ubs_admin password, this fails under makemigrations.
        try:
            from django.conf import settings
            from core.util import get_user_ubs_admin

            ubsadmin = get_user_ubs_admin()
            ubsadmin.set_password(settings.DEFAULT_ADMIN_PASSWORD)
            ubsadmin.changeReason = 'New admin password'
            ubsadmin.save()
        except Exception as exception:
            # TODO: Log exception
            pass

        # Try to set domain name, this fails under makemigrations.
        try:
            from django.conf import settings
            from django.contrib.sites.models import Site
            current_site = Site.objects.get_current()
            current_site.domain = settings.SITE_URL
            current_site.name = settings.SITE_NAME
            current_site.save()
        except Exception as exception:
            # TODO: Log exception
            pass


old_debug = True

@receiver([pre_save])
def pre_save_full_clean_handler(sender, instance, *args, **kwargs):
    """Force all models to call full_clean before save, when in DEBUG mode."""
    from django.contrib.sessions.models import Session
    if 'raw' in kwargs and kwargs['raw']:
        return

    from django.conf import settings
    global old_debug
    if settings.DEBUG != old_debug:
        print("Debug went from " + str(old_debug) + " to " + str(settings.DEBUG))
        old_debug = settings.DEBUG

    if sender != Session:
        # and settings.DEBUG is True:
        instance.full_clean()
