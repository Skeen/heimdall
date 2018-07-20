"""Django Model."""
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

#from django.core.exceptions import ValidationError
#from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as _lazy
from django.db import models
# from django.utils import timezone
#from simple_history.models import HistoricalRecords

import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from api.models import util
from api.models import KeyEntry
from api.models import PublicKey


@python_2_unicode_compatible
class Password(models.Model):
    """Encrypted individual password for a keyentry."""

    class Meta:
        verbose_name = _lazy("password")
        verbose_name_plural = _lazy("passwords")
        unique_together = ("key_entry", "public_key")

    password = models.CharField(max_length=util.MAX_LENGTH_NUMBER)
    """The encrypted password itself (base64 encoded)"""

    key_entry = models.ForeignKey(
        KeyEntry,
        related_name='passwords',
        on_delete=models.PROTECT
    )
    """Key entry this pasword is associated to."""

    public_key = models.ForeignKey(
        'PublicKey',
        related_name="passwords",
        on_delete=models.PROTECT
    )
    """Public key this password was encrypted under."""

    signature = models.CharField(max_length=util.MAX_LENGTH_NUMBER)
    """Signature that was made by the encrypter."""

    signing_key = models.ForeignKey(
        'PublicKey',
        related_name="signatures",
        on_delete=models.PROTECT
    )
    """Key that was used to sign this password."""

    def clean(self):
        """Check that the signature checks out."""
        binary_password = base64.b64decode(self.password)
        binary_signature = base64.b64decode(self.signature)
        public_key.verify(
            binary_signature,
            binary_password,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

    def __str__(self):
        return ("Password for: " + smart_text(self.key_entry) + 
                " encrypted by: " + self.signing_key.user.username + 
                " for: " + self.public_key.user.username)
