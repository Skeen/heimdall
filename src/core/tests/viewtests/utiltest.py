"""Unit-tests for utils within adminapp.views.util."""
# flake8: noqa pydocstyle:noqa
# TODO: Avoid disabling entire file with noqa ^^

from django.http import HttpResponse
from django.test import TestCase
from django.views.generic import View
from nose_parameterized import parameterized

from adminapp.tests.viewtests.util import url_bypasser
from core.views import ReplyOverride, CompositeView
from core.views.util import find_closest_parent_x


class CompositeExample(CompositeView):
    """Testing stub for CompositeView."""

    def render_to_response(self, context):
        """Testing mock, which check if method was called."""
        return HttpResponse("Hello world")

    def self_url(self):
        return '/RETURN_URL/'


class SubViewExample(View):
    """Testing stub for subviews."""

    override_response = False
    get_called = False
    post_called = False

    def reply_helper(self, request):
        """Common helper used by both get and post.

        Returns:
            str: 'SubViewExample' followed by GET/POST and override if so.
        """
        # Build the text
        text = "SubViewExample" + " " + request.method
        if self.override_response:
            text = text + " " + "(override)"
        # Return the response
        response = HttpResponse(text)
        if self.override_response:
            raise ReplyOverride(response=response)
        else:
            return response

    # pylint: disable=missing-docstring
    # pylint: disable=unused-argument
    def get(self, request, *args, **kwargs):
        SubViewExample.get_called = True
        return self.reply_helper(request)

    # pylint: disable=missing-docstring
    # pylint: disable=unused-argument
    def post(self, request, *args, **kwargs):
        SubViewExample.post_called = True
        return self.reply_helper(request)


class CompositeSubviewExample(CompositeView):
    """Testing stub for CompositeView using subviews."""

    # pylint: disable=W9903
    def self_url(self):
        return '/RETURN_URL/'

    template_name = 'tests/CompositeSubviewExample.html'
    subviews = {
        'subview': SubViewExample.as_view()
    }


class CompositeViewTest(TestCase):
    """Test the CompositeView class."""

    # pylint: disable=missing-docstring
    def setUp(self):
        SubViewExample.override_response = False
        SubViewExample.get_called = False
        SubViewExample.post_called = False

    # pylint: disable=missing-docstring
    def test_get(self):
        response = url_bypasser(CompositeExample.as_view())
        self.assertContains(response, "Hello world")

    # pylint: disable=missing-docstring
    # def test_post(self):
    #    response = url_bypasser(CompositeExample.as_view(),
    #                            request_type='POST')
    #    self.assertRedirects(response,
    #                         '/RETURN_URL/',
    #                         fetch_redirect_response=False)

    # pylint: disable=missing-docstring
    def test_subview_get(self):
        response = url_bypasser(CompositeSubviewExample.as_view())
        self.assertContains(response, "SubViewExample GET")
        self.assertNotContains(response, "(override)")
        self.assertTrue(SubViewExample.get_called)

    # pylint: disable=missing-docstring
    # def test_subview_post(self):
    #    response = url_bypasser(CompositeSubviewExample.as_view(),
    #                            request_type='POST')
    #    self.assertRedirects(response,
    #                         '/RETURN_URL/',
    #                         fetch_redirect_response=False)
    #    self.assertTrue(SubViewExample.post_called)

    # pylint: disable=missing-docstring
    def test_subview_get_override(self):
        SubViewExample.override_response = True
        response = url_bypasser(CompositeSubviewExample.as_view())
        self.assertContains(response, "SubViewExample GET (override)")
        self.assertTrue(SubViewExample.get_called)

    # pylint: disable=missing-docstring
    def test_subview_post_override(self):
        SubViewExample.override_response = True
        response = url_bypasser(CompositeSubviewExample.as_view(),
                                request_type='POST')
        self.assertContains(response, "SubViewExample POST (override)")
        self.assertTrue(SubViewExample.post_called)


# TODO: Test CompositeDetailView and ComponentFormMixin


class FindClosestParentXTest(TestCase):
    """Test the find_closest_parent_x function."""

    # pylint: disable=missing-docstring
    @parameterized.expand([
        # Empty dictionary
        ['key', {}, ValueError],
        ['value', {}, ValueError],
        ['url', {}, ValueError],
        ['object', {}, ValueError],
        [5, {}, ValueError],

        # First layer
        ['key', {'key': 'Hello'}, 'Hello'],
        ['value', {'key': 'Hello'}, ValueError],
        ['url', {'magic': 'wow'}, ValueError],
        ['object', {'object': 'Iceberg'}, 'Iceberg'],
        [5, {5: 'Hello'}, 'Hello'],

        # Multilayer
        ['key', {'key': 'Hello', 'parent': {}}, 'Hello'],
        ['key', {'key': 'Hello', 'parent': {'key': 'Valid'}}, 'Hello'],
        ['key', {'magic': 'Hello', 'parent': {'key': 'Valid'}}, 'Valid'],
        ['key', {'parent': {}}, ValueError],
        ['key', {'parent': {'key': 'Hello'}}, 'Hello'],
        ['key', {'parent': {'parent': {'key': 'Hello'}}}, 'Hello'],
    ])
    def test_first_layer_dict(self, key, dictionary, expected):
        if expected == ValueError:
            self.assertRaises(ValueError,
                              find_closest_parent_x,
                              dictionary,
                              key)
        else:
            value = find_closest_parent_x(dictionary, key)
            self.assertEqual(value, expected)
