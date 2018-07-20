# pylint: disable=W9903
"""Data generator."""
import random
import base64

from django.utils.crypto import get_random_string

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from api.models import KeyEntry
from api.models import Password
from api.models import PublicKey

from api.models.gen import util
from api.models.gen import gen_group
from api.models.gen import gen_public_key
from api.models.gen import gen_key_pair
from api.models.gen import stringify_public_key



def encrypt(public_key, message):
    cipher = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return cipher


def decrypt(private_key, ciphertext):
    plain = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plain


def sign(private_key, message):
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature


def gen_key_entry(owner=None):
    """Generate a randomized key_entry."""
    if owner is None:
        owner = gen_group()

    bird = random.choice(util.BIRDS)  
    title = "Login til " + bird + " systemet"
    username = get_random_string(10, util.CHARACTERS)
    url = 'magenta.dk'
    # Generate the *real* password
    raw_password = str(get_random_string(10, util.CHARACTERS))
    notes = 'The password is: ' + raw_password

    key_entry = KeyEntry(
        owner=owner,
        title=title,
        username=username,
        url=url,
        notes=notes,
    )
    key_entry.full_clean()
    key_entry.save()

    # We need to encrypt this with the public keys for every user in 'owner'
    public_keys = PublicKey.objects.filter(
        # Find public keys, whose users are a group, where the group has a 
        # reverse key entry, that is the generated object.
        user__groups__key_entries=key_entry
    )
    # Prepare our keys
    sign_private_key, sign_public_key = gen_key_pair()
    sign_public_key_object = gen_public_key(
        key=stringify_public_key(sign_public_key)
    )

    for user_public_key in public_keys:
        # Encrypt and sign
        encrypted_password = encrypt(user_public_key.as_key(), raw_password)
        signature = sign(sign_private_key, encrypted_password)
        # Base64 encode the binary
        encoded_password = base64.b64encode(encrypted_password)
        encoded_signature = base64.b64encode(signature)

        password = Password(
            password=encoded_password,
            signature=encoded_signature,
            signing_key=sign_public_key_object,
            public_key=user_public_key,
            key_entry=key_entry
        )
        password.full_clean()
        password.save()

    return key_entry
