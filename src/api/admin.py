"""Django admin."""
from django.contrib import admin
from api.models import KeyEntry
from api.models import Password
from api.models import PublicKey

admin.site.register(KeyEntry)
admin.site.register(Password)
admin.site.register(PublicKey)
