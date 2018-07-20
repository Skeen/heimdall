"""API endpoint for KeyEntry."""
# pylint: disable=W9903
# TODO: Do translations wherever required.
from __future__ import unicode_literals

from django.forms import widgets
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model
from django.db import transaction

from rest_framework import serializers
from rest_framework import viewsets
from rest_framework import mixins

import django_filters
from django_filters.rest_framework import DjangoFilterBackend

from api.models import KeyEntry
from api.models import Password
from api.views.Password import PasswordSerializer


# Serializers define the API representation.
class KeyEntrySerializer(serializers.HyperlinkedModelSerializer):
    """Serializer to present users (get_user_model())."""

    class Meta:
        model = KeyEntry
        fields = ('__all__')

    passwords = PasswordSerializer(
        read_only=True,
        many=True
    )

    passwords_write = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()    
        ),
        write_only=True,
    )

    def validate(self, data):
        # TODO: Lookup using permission system, or something like that
        # List of users who needs this password
#        users = [
#            user, get_user_model().objects.get(pk=3)
#        ]
        users = get_user_model().objects.filter(public_keys__isnull=False)
        users_set = set([x.pk for x in users])
        passwords = data['passwords_write']
        passwords_keyset = set([int(x['user_pk']) for x in passwords])

        if users_set != passwords_keyset:
            extra = passwords_keyset - users_set
            missing = users_set - passwords_keyset
            raise ValidationError(
                _("Request did not contain required passwords. " + 
                  "Extra passwords: " + str(list(extra)) + " "
                  "Missing passwords: " + str(list(missing))
                )
            )

        # TODO: Check password signatures
        # Load uploaders public key

        user =  self.context['request'].user
        public_key = user.public_key.first().as_key()

        for dicty in passwords:
            user_pk = int(dicty['user_pk'])
            encoded_password = dicty['password']
            encoded_signature = dicty['signature']

            if user_pk not in users_set:
                raise ValidationError(
                    _("Some users could not be looked up.")
                )

            password = Password(
                key_entry=keyentry,
                public_key=key,
                password=encoded_password,
                signature=encoded_signature,
                signing_key = public_key
            )
            password.full_clean()

        return data

    def create(self, validated_data):
        passwords = validated_data['passwords_write']
        del validated_data['passwords_write']
        del validated_data['user']
        with transaction.atomic(savepoint=True):
            keyentry = KeyEntry.objects.create(**validated_data)

            for dicty in passwords:
                user_pk = dicty['user_pk']
                password = dicty['password']
                Password.objects.create(
                    key_entry=keyentry,
                    user=get_user_model().objects.get(pk=user_pk),
                    password=password
                )

            return keyentry


# ViewSets define the view behavior.
class KeyEntryViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """
    """

    queryset = KeyEntry.objects.none()
    serializer_class = KeyEntrySerializer

    def get_queryset_raw(self):
        """Filter the queryset for non-admin users.

        Non admin users can only see themself and staff users.
        """
        user = self.request.user
        # If staff, show everything
        if user.is_staff:
            return KeyEntry.objects.all()
        # If user, only show our own passwords
        return KeyEntry.objects.filter(
            Q(passwords__user__pk=user.pk)
        )

    def get_queryset(self):
        queryset = self.get_queryset_raw()
        return queryset.order_by('pk')

    def perform_create(self, serializer):
        # Send from the current user
        serializer.save(
            user=self.request.user,
        )
