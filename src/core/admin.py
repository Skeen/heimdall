"""Django admin."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model


# pylint: disable=too-few-public-methods
class ReturnURLMixin(object):
    """Add support for 'next' return urls in when linking a django admin page.

    Note:

        Adds support for 'next', if no such field is provided, simply utilizes
        the default behavior.

    Example:

        Making a page link back to the URL updating the model:

        .. code: python

            <a href="{% url 'admin:webapp_pointvalue_change' point_value.pk %}
                     ?next={{ URL }}">

    Returns:

        HttpResponse: Either a redirect to 'next' or whatever normally happens
    """

    def response_add(self, request, obj, url_cont=None):
        """Check for 'next' are redirect to it, if it exists."""
        from django.utils.http import is_safe_url
        from django.http.response import HttpResponseRedirect

        res = super(ReturnURLMixin, self).response_add(request, obj, url_cont)
        # TODO: Handle POST requests too
        if "next" in request.GET and is_safe_url(request.GET['next']):
            return HttpResponseRedirect(request.GET['next'])
        else:
            return res

    def response_change(self, request, obj):
        """Check for 'next' are redirect to it, if it exists."""
        from django.utils.http import is_safe_url
        from django.http.response import HttpResponseRedirect

        res = super(ReturnURLMixin, self).response_change(request, obj)
        # TODO: Handle POST requests too
        if "next" in request.GET and is_safe_url(request.GET['next']):
            return HttpResponseRedirect(request.GET['next'])
        else:
            return res


class ReturnURLAdmin(ReturnURLMixin, admin.ModelAdmin):  # noqa: D101
    # pylint: disable=missing-docstring
    pass


class CustomUserAdmin(ReturnURLMixin, UserAdmin):  # noqa: D101
    # pylint: disable=missing-docstring
    pass


admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), CustomUserAdmin)
