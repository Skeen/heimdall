# flake8: noqa # pylint: skip-file

# Create your views here.
from django.views.generic import View
from django.views.generic import DetailView, TemplateView

from core.views.util import ReplyOverride, CompositeHelper


class CompositeSubView(CompositeHelper, View):
    """Default detail view compositor."""

    parent_object = None

    def get(self, request, *args, **kwargs):
        """On get, render all subviews and render our view."""
        try:
            self.parent_object = kwargs['parent']['object']
        except:
            self.parent_object = self.get_object()
        return super(CompositeSubView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """On post, forward post to all subviews, and redirect to ourself."""
        try:
            self.parent_object = kwargs['parent']['object']
        except:
            self.parent_object = self.get_object()
        return super(CompositeSubView, self).post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.parent_object


class CompositeDetailView(CompositeHelper, DetailView):
    """Default detail view compositor."""

    object = None

    def get(self, request, *args, **kwargs):
        """On get, render all subviews and render our view."""
        try:
            self.object = kwargs['parent']['object']
        except:
            self.object = self.get_object()
        try:
            context = super(
                CompositeDetailView,
                self
            ).seed_context(*args, **kwargs)
            return self.render_to_response(context)
        except ReplyOverride as exp:
            return exp.response

    def post(self, request, *args, **kwargs):
        """On post, forward post to all subviews, and redirect to ourself."""
        try:
            self.object = kwargs['parent']['object']
        except:
            self.object = self.get_object()
        try:
            context = super(
                CompositeDetailView,
                self
            ).seed_context(*args, **kwargs)
            return self.render_to_response(context)
        except ReplyOverride as exp:
            return exp.response

    def build_parent_dict(self, *args, **kwargs):
        """Expand the ordinary parent dictionary with parent objects."""
        dic = super(
            CompositeDetailView,
            self
        ).build_parent_dict(*args, **kwargs)
        dic['object'] = self.object
        return dic


class CompositeView(CompositeHelper, TemplateView):
    """Default template view compositor."""

    def get(self, request, *args, **kwargs):
        """On get, render all subviews and render our view."""
        try:
            context = super(CompositeView, self).seed_context(*args, **kwargs)
            return self.render_to_response(context)
        except ReplyOverride as exp:
            return exp.response

    def post(self, request, *args, **kwargs):
        """On post, forward post to all subviews, and redirect to ourself."""
        try:
            # pylint: disable=unused-variable
            context = super(
                CompositeView,
                self
            ).seed_context(*args, **kwargs)
            return self.render_to_response(context)
        except ReplyOverride as exp:
            return exp.response
