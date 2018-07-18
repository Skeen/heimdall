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
from api.models import KeyEntry


@python_2_unicode_compatible
class Password(models.Model):
    """
    """

    class Meta:
        verbose_name = _lazy("password")
        verbose_name_plural = _lazy("passwords")
        unique_together = ("key_entry", "user")

    # history = HistoricalRecords()

    password = models.CharField(max_length=util.MAX_LENGTH_NUMBER)
    """
    """

    key_entry = models.ForeignKey(
        KeyEntry,
        related_name='passwords',
        on_delete=models.PROTECT
    )
    """
    """

    user = models.ForeignKey(
        get_user_model(),
        related_name="passwords",
        on_delete=models.PROTECT
    )
    """
    """

    def __str__(self):
        return ("Password: " + self.user.username)
