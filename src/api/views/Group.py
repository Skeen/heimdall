"""API endpoint for Group."""
from __future__ import unicode_literals

from django.contrib.auth.models import Group

from rest_framework import serializers
from rest_framework import viewsets


# Serializers define the API representation.
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer to present groups."""

    class Meta:
        model = Group
        fields = '__all__'


# ViewSets define the view behavior.
class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
