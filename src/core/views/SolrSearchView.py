"""View for handling Solr service interruptions."""
from django.contrib import messages
from django.utils.translation import ugettext as _
from haystack.generic_views import SearchView
from haystack.generic_views import FacetedSearchView
from haystack.query import RelatedSearchQuerySet

from core.management.util import get_status_code
from webapp.models.util import Searchable


class SolrMixin(object):
    """Mixin for handling Solr service interruptions.

    Args:
        result_type (:obj:`django.models.Model`):
            The model we want our search to return.
        order_by (str):
            The property to order models by.
            Must refer to property available in the search index.
        order_by_fallback (str):
            The property to order models by when solr is not available.
            Must refer to database field using django syntax.
            Example (when result is list of Applicants): 'user__last_name'.

    Note:
        This view handles Solr crashing, and will produce the full list of
        :code:`result_type` models, in that case.
    """

    result_type = None
    order_by = None
    order_by_fallback = None
    queryset = RelatedSearchQuerySet()

    def _handle_solr_down(self):
        if issubclass(self.result_type, Searchable) is False:
            raise ValueError(
                _("Non Searchable model provided to SolrSearchView")
            )

        # pylint: disable=W9903
        # pylint: disable=no-name-in-module
        from heimdall.settings import HAYSTACK_CONNECTIONS
        try:
            solr_host = HAYSTACK_CONNECTIONS['default']['HOST']
            if not get_status_code(solr_host, "/solr/"):
                messages.warning(
                    self.request,
                    _('The Solr search engine is not responding.')
                )
                return True
        except KeyError:
            return True
        return False

    def wrap_handle_solr_down(self, queryset):
        """Handle it when Solr is down, and wrap queryset.

        Helper function.
        * Returns all objects if Solr is down.
        * Orders query sets by :code:`order_by` or :code:`order_by_fallback`.
        * Calls prefetch_queryset on the resulting queryset.
        """
        # Print warnings, if down return everything
        if self._handle_solr_down():
            results = self.prefetch_queryset(
                self.result_type.objects.all().order_by(
                    self.order_by_fallback
                ), None
            )
            # Context: The functionality of returning a fake-result queryset
            # when Solr is down, works in the normal case, but breaks with
            # faceted search, utilizing the below hack removes the error being
            # thrown, but does not produce usable search results.
            # TODO: Ugly hack, to work around a probably much bigger problem
            # TODO: Find a feasible solution to faceted search when down.
            # results.facet_counts = lambda: 0
        else:
            results = queryset
            results = results.order_by(self.order_by)
            results = results.load_all_queryset(
                self.result_type,
                self.prefetch_queryset(self.result_type.objects.all(), results)
            )
        return results

    def get_queryset(self):
        """Handle it when Solr is down, and wrap queryset."""
        return self.wrap_handle_solr_down(
            super(SolrMixin, self).get_queryset()
        )

    def form_valid(self, form):
        """When form is valid, do the search."""
        # Print warnings, if down return everything
        self.queryset = self.wrap_handle_solr_down(
            form.search()
        )
        context = self.get_context_data(**{
            self.form_name: form,
            'query': form.cleaned_data.get(self.search_field),
            'object_list': self.queryset
        })
        return self.render_to_response(context)

    # pylint: disable=no-self-use
    # pylint: disable=unused-argument
    def prefetch_queryset(self, queryset, sqs=None):
        """Method to be overrided by subclasses to implement prefetching."""
        return queryset


class SolrSearchView(SolrMixin, SearchView):
    """Solr Mixin for Haystack SearchView."""

    pass


class SolrFacetedSearchView(SolrMixin, FacetedSearchView):
    """Solr Mixin for Haystack FacetedSearchView."""

    pass
