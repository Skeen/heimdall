"""Django Model."""
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth import get_user_model

#from django.core.exceptions import ValidationError
#from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as _lazy
from django.db import models
# from django.utils import timezone
#from simple_history.models import HistoricalRecords

from api.models import util


# TODO: Consider logic when public is uploaded after passwords are made


@python_2_unicode_compatible
class PublicKey(models.Model):
    """
    """

    class Meta:  # noqa: D101
        verbose_name = _lazy("public key")
        verbose_name_plural = _lazy("public keys")

    user = models.OneToOneField(
        get_user_model(),
        related_name="public_key",
        on_delete=models.PROTECT
    )

    key = models.CharField(max_length=util.MAX_LENGTH_NUMBER)

    def __str__(self):
        return "WOW"
