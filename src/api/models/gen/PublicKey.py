# pylint: disable=W9903
"""Data generator."""
import random

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

from api.models import PublicKey

from api.models.gen import util
from api.models.gen import gen_user


def gen_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key


def stringify_public_key(public_key):
    return public_key.public_bytes(
        encoding=serialization.Encoding.OpenSSH,
        format=serialization.PublicFormat.OpenSSH
    )


def gen_public_key(user=None, key=None):
    """Generate a randomized public_key."""
    if user is None:
        user = gen_user()

    if key is None:
        _, public_key = gen_key_pair()
        key = stringify_public_key(public_key)

    public_key = PublicKey(
        user=user,
        key=key,
    )
    public_key.full_clean()
    public_key.save()
    return public_key
