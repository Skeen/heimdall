# pylint: disable=W9903
"""Data generator."""
import random

from api.models import PublicKey

from api.models.gen import util
from api.models.gen import gen_user


def gen_public_key(user=None, key=None):
    """Generate a randomized public_key."""
    if user is None:
        user = gen_user()

    if key is None:
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.primitives import serialization
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        key = public_key.public_bytes(
            encoding=serialization.Encoding.OpenSSH,
            format=serialization.PublicFormat.OpenSSH
        )

    public_key = PublicKey(
        user=user,
        key=key,
    )
    public_key.full_clean()
    public_key.save()
    return public_key
