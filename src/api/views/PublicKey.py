"""API endpoint for PublicKey."""
# pylint: disable=W9903
# TODO: Do translations wherever required.
from __future__ import unicode_literals

from django.forms import widgets
from django.core.exceptions import ValidationError
from django.db.models import Q

from rest_framework import serializers
from rest_framework import viewsets
from rest_framework import mixins

import django_filters
from django_filters.rest_framework import DjangoFilterBackend

from api.models import PublicKey
from api.models import util


# Serializers define the API representation.
class PublicKeySerializer(serializers.HyperlinkedModelSerializer):
    """
    """

    class Meta:
        model = PublicKey
        fields = ('__all__')
        read_only_fields = ('user',)

    def validate_key(self, value):
        """Ensure that only valid ssh public keys can be uploaded."""
        key_string = str(value)
        # Check if parsing throws an exception
        try:
            util.parse_key(key_string)
        except ValueError as value_error:
            raise ValidationError(str(value_error))
        return key_string


# ViewSets define the view behavior.
class PublicKeyViewSet(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    """All public keys are by their nature, public.

    Keys on the standard OpenSSH format can be uploaded and added to your own
    user account. It is not possible to add keys to other users via the REST 
    API.
    """

    queryset = PublicKey.objects.all().order_by('pk')
    serializer_class = PublicKeySerializer

    def perform_create(self, serializer):
        # Send from the current user
        serializer.save(
            user=self.request.user,
        )
