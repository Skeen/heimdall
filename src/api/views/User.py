"""API endpoint for User."""
# pylint: disable=W9903
# TODO: Do translations wherever required.
from __future__ import unicode_literals

from django.forms import widgets
from django.db.models import Q
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework import viewsets

import django_filters
from django_filters.rest_framework import DjangoFilterBackend


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer to present users (get_user_model())."""

    class Meta:
        model = get_user_model()
        exclude = ('groups',)


# ViewSets define the view behavior.
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """Get a list of all users visible to the current user.

    If the current user is staff, all users are visible.

    If the current user is in applicant, only their own user and staff users
    are visible.

    Note: Should not be accessed directly, but rather indirectly via. the links
    provided in messages.
    """

    queryset = get_user_model().objects.none()
    serializer_class = UserSerializer

    def get_queryset_raw(self):
        """Filter the queryset for non-admin users.

        Non admin users can only see themself and staff users.
        """
        user = self.request.user
        # If staff, show everything
        if user.is_staff:
            return get_user_model().objects.all()
        # If user, only show ourself and staff members
        return get_user_model().objects.filter(
            Q(pk=user.pk) |
            Q(is_staff=True)
        )

    def get_queryset(self):
        queryset = self.get_queryset_raw()
        return queryset.order_by('pk')
