# flake8: noqa # pylint: skip-file
from django.conf.urls import url, include
from rest_framework import routers

from . import views

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'user',
                views.UserViewSet,)
router.register(r'group',
                views.GroupViewSet,)
router.register(r'password',
                views.PasswordViewSet,)
router.register(r'keyentry',
                views.KeyEntryViewSet,)
router.register(r'public_key',
                views.PublicKeyViewSet,)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
]
