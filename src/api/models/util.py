from django.contrib.auth import get_user_model

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

MAX_LENGTH_NUMBER=2000

def parse_key(key):
    return serialization.load_ssh_public_key(
        key,
        backend=default_backend()
    )


def get_master_user():
    # Ensure our master key user exists
    user, created = get_user_model().objects.get_or_create(
        username='masterkey',
        defaults={
            'password': 'masterpass'
        }
    )
    # If just created, ensure password is unusable
    if created:
        user.set_unusable_password()
        user.save()

    return user


def get_lock():
    lock = get_user_model().objects.select_for_update().filter(
        username='masterkey'
    )
    return lock
