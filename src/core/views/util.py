"""Util for core.views."""
from django import forms
from django.utils.translation import ugettext as _
from django.http.response import HttpResponse
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from braces.views import GroupRequiredMixin

from core.util import get_http_response


def find_closest_parent_object(dictionary):
    """Search through parents in the dictionary looking for 'object'."""
    # pylint: disable=W9903
    return find_closest_parent_x(dictionary, 'object')


def find_closest_parent_url(dictionary):
    """Search through parents in the dictionary looking for 'url'."""
    # pylint: disable=W9903
    return find_closest_parent_x(dictionary, 'url')


def find_closest_parent_x(dictionary, key):
    """Search through parents in the dictionary looking for 'key'."""
    if key in dictionary and dictionary[key] is not None:
        return dictionary[key]
    elif 'parent' in dictionary:
        return find_closest_parent_x(dictionary['parent'], key)
    else:
        raise ValueError(_("No parent %(key)s found") % {'key': key})


class ReplyOverride(Exception):
    """Exception thrown to override behavior of composite helper."""

    def __init__(self, response):
        """Bind the response to use instead."""
        super(ReplyOverride, self).__init__()
        self.response = response


class CompositeHelper(object):
    """Mixin helper class for CompositeViews.

    Still need further refactoring.
    """

    # Subviews is a dictionary of views to render.
    subviews = {}

    # self_url should be set by the grandest parent of the render chain.
    def self_url(self):
        """The url of this page, i.e. where we return to on post submits."""
        pass

    # request, and get_context_data will be set by some class-based view.

    def render_subviews(self, *args, **kwargs):
        """Call each subview, and render them.

        Output is a dictionary mapping subview name to rendered context.
        """
        subview_content = {}
        for variable, subview in self.subviews.items():
            # pylint: disable=no-member
            response = get_http_response(
                subview, self.request,
                *args, **kwargs
            )
            subview_content[variable] = response.content
            # print variable, response.status_code
            if response.status_code == 302 and response.url != 'None':
                raise ReplyOverride(response=response)
        return subview_content

    # pylint: disable=unused-argument
    def build_parent_dict(self, *args, **kwargs):
        """Build a single layer of the parent recursive dictionary."""
        parent_dict = {}
        parent_dict['url'] = self.self_url()
        return parent_dict

    def setup_parent(self, *args, **kwargs):
        """Build a layer, and move entire stack if required."""
        # Setup parent dictionaries
        parent_dict = self.build_parent_dict(*args, **kwargs)
        if 'parent' in kwargs:
            parent_dict['parent'] = kwargs['parent']
        kwargs['parent'] = parent_dict
        return kwargs

    def seed_context(self, *args, **kwargs):
        """Setup parent dictionary, and render subviews to context."""
        kwargs = self.setup_parent(*args, **kwargs)

        # pylint: disable=no-member
        context = self.get_context_data(**kwargs)
        context.update(self.render_subviews(*args, **kwargs))

        return context


class ComponentFormMixin(object):
    """Should be extended by subviews containing forms."""

    def get_form_identifier(self):
        """Get a unique identifier for this form / view."""
        # TODO: Random generated string?
        return self.__module__ + "." + self.__class__.__name__

    def dispatch(self, request, *args, **kwargs):
        """If we recieve a post, check if it was for us using the identifier.

        If it was indeed for us, proceed with the post, otherwise fire a get.
        """
        # TODO: Utilize as_component marker?
        if request.method.lower() == 'post':

            form_identifier = self.get_form_identifier()

            if form_identifier not in request.POST:
                # pylint: disable=W9903
                request.method = 'GET'
                result = self.get(request, *args, **kwargs)
                # pylint: disable=W9903
                request.method = 'POST'
                return result

        return super(ComponentFormMixin, self).dispatch(
            request, *args, **kwargs
        )

    def get_form(self, form_class=None):
        """Override to add hidden field with identifier."""
        form = super(ComponentFormMixin, self).get_form(form_class=form_class)

        # Add extra hidden input that always submits self.form_identifier as
        # true.
        form_id = self.get_form_identifier()
        form.fields[form_id] = forms.CharField(widget=forms.HiddenInput())
        # TODO: Why should required be false?
        # form.fields[form_id].required = False
        form.fields[form_id].initial = True
        # Set value to field name for debugging, not required for functionality
        # form.fields[form_id].initial =
        #   self.__module__ + "." + self.__class__.__name__
        return form


class UBSAdminRequiredMixin(GroupRequiredMixin):
    """Mixin to check whether the logged-in user is a UBSAdmin."""

    # pylint: disable=W9903
    group_required = "ubsadmin"


def is_ubsadmin(user):
    """Check if the provided `user` is an ubsadmin.

    Param:
        user (:obj:`django.contrib.auth.get_user_model()`):
            The user to check

    Returns:
        bool: Whether the user is an ubsadmin
    """
    return user.groups.filter(name='ubsadmin').exists()


class DummyView(ComponentFormMixin, View):
    """Temporary dummy debug view, showing a string has been rendered."""

    name = None

    def get(self, request, *args, **kwargs):
        """Return the provided name inside an otherwise static string."""
        return HttpResponse("DummyView (" + self.name + ") rendered<br/>")


# pylint: disable=too-few-public-methods
class DebugContext(object):
    """Add DEBUG to template context."""

    def get_context_data(self, **kwargs):  # noqa: D102
        """Seed the debug variable to the context."""
        from heimdall import settings
        # pylint: disable=no-member
        context = super(DebugContext, self).get_context_data(**kwargs)
        # pylint: disable=no-member
        context['DEBUG'] = settings.DEBUG
        return context


# pylint: disable=too-few-public-methods
class PaginationDecoratorMixin(object):
    """Mixin to add pagination to a queryset."""

    pagination_variable = None
    annotate_paginated_only = False
    # paginate_by = 10

    # pylint: disable=no-self-use
    def decorate_paginated(self, object_list):
        """Decorate the queryset if desired.

        Decoration can be done after pagination, by utilizing the
        :code:`annotate_paginated_only` variable.
        """
        return object_list

    def paginate_queryset(self, queryset):
        """Add pagination to the queryset."""
        if self.pagination_variable is None:
            raise ValueError(_("Pagination variable not set!"))

        # paginator = Paginator(queryset, self.paginate_by)
        paginator = Paginator(queryset, 10)

        page_number = self.request.GET.get(self.pagination_variable)
        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            # If page_number is not an integer, deliver first page.
            page = paginator.page(1)
        except EmptyPage:
            # If page_number is out of range (e.g. 9999),
            # deliver last page of results.
            # pylint: disable=no-member
            page = paginator.page(paginator.num_page_numbers)

        if self.annotate_paginated_only:
            # pylint: disable=no-member
            paged_ids = list(page.object_list.values_list('pk', flat=True))
            page.object_list = self.decorate_paginated(
                # pylint: disable=no-member
                page.object_list.model.objects.filter(pk__in=paged_ids)
            )
        else:
            page.object_list = self.decorate_paginated(page.object_list)

        return page
