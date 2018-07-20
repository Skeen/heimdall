# flake8: noqa # pylint: skip-file
from __future__ import unicode_literals

from django.db import transaction
from django.apps import AppConfig



class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        from django.conf import settings

        from api.models.util import get_master_user
        from api.models.util import get_lock
        from api.models.util import parse_key
        from api.models import PublicKey
        # Try to set up our master user, this fails under makemigrations.
        try:
            master_key = settings.MASTER_PUBLIC_KEY
            # Try to parse the master key (exception if invalid)
            parse_key(master_key)

            with transaction.atomic(savepoint=True):
                # Ensure our master key user exists
                user = get_master_user()
                # Acquire lock on master key user
                lock = get_lock()
                # Delete all keys, which aren't the master key
                deleted_count, del_dict = PublicKey.objects.filter(
                    user=user
                ).exclude(key=master_key).delete()
                key, created = PublicKey.objects.get_or_create(
                    user=user,
                    key=master_key
                )
                if deleted_count != 0:
                    print "Deleted spurious master key(s)"
                if created:
                    print "Created master key"
        except Exception as exception:
            print str(exception)
            # TODO: Log exception
            pass
