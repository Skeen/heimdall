"""Django Model."""
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

#from django.core.exceptions import ValidationError
#from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as _lazy
from django.db import models
# from django.utils import timezone
#from simple_history.models import HistoricalRecords

from api.models import util


@python_2_unicode_compatible
class KeyEntry(models.Model):
    """
    """

    class Meta:
        verbose_name = _lazy("key entry")
        verbose_name_plural = _lazy("key entries")

    # history = HistoricalRecords()

    title = models.CharField(max_length=util.MAX_LENGTH_NUMBER, blank=True)
    """
    """

    username = models.CharField(max_length=util.MAX_LENGTH_NUMBER, blank=True)
    """
    """

    url = models.CharField(max_length=util.MAX_LENGTH_NUMBER, blank=True)
    """
    """

    notes = models.CharField(max_length=util.MAX_LENGTH_NUMBER, blank=True)
    """
    """

    def __str__(self):
        return ("KeyEntry: " + self.title + " for " + self.username + " @ " + self.url)
