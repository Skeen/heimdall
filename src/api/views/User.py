"""API endpoint for User."""
from __future__ import unicode_literals

from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework import viewsets


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer to present users (get_user_model())."""

    class Meta:
        model = get_user_model()
        fields = '__all__'


# ViewSets define the view behavior.
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
