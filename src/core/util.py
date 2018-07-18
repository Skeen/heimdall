"""Common utils for multiple places."""

import signal
import threading
from contextlib import contextmanager

# TODO: Combine implementations of set_interval and set_timeout
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import signals
from django.http import HttpResponse
from django.template.response import SimpleTemplateResponse
from django.utils import timezone
from django.utils.translation import ugettext as _


# pylint: disable=too-few-public-methods
import core
import webapp


class Empty(object):
    """Empty class, that can be dynamically expanded."""

    pass


class FakeDict(dict):
    """Dictionary to fake the webapp.models.Dictionary class."""

    def as_py_dict(self):
        """Return self, as we are already a python dict."""
        return self


def set_interval(func, sec):
    """Call the function 'func' every 'sec' seconds.

    Similar to JavaScripts setInterval function.
    """
    def func_wrapper():
        """Wrapper function, called after 'func' seconds."""
        # Reschedule calling, with the set_interval function
        set_interval(func, sec)
        # Call the function
        func()
    # Setup our timer
    timer = threading.Timer(sec, func_wrapper)
    timer.daemon = True
    timer.start()
    return timer


def set_timeout(func, sec):
    """Call the function 'func' after 'sec' seconds.

    Similar to JavaScripts setTimeout function.
    """
    def func_wrapper():
        """Wrapper function, called after 'func' seconds."""
        # Call the function
        func()
    # Setup our timer
    timer = threading.Timer(sec, func_wrapper)
    timer.daemon = True
    timer.start()
    return timer


class TimeoutException(Exception):
    """Exception thrown when a timeout has occured."""

    pass


@contextmanager
def time_limit(seconds):
    """Runs the with block for 'seconds' seconds, before firing an exception.

    Examples:
        .. code:: python

            try:
                with time_limit(5):
                    print "This code has 5 seconds to complete."
                    # ...
            except TimeoutException:
                print "The code didn't complete in 5 seconds."

    Note:
        Heavily inspired by:
        * http://stackoverflow.com/questions/366682/

    """
    def signal_handler(_1, _2):
        """Signal handler, which fires our exception."""
        raise TimeoutException
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


class time_limited(object):
    # pylint: disable=invalid-name
    # pylint: disable=too-few-public-methods
    """Runs the function for 'timeout' seconds, before firing an exception.

    Examples:
        .. code:: python

            @time_limited(5)
            def hurryup():
                print "This function has 5 seconds to complete."
                # ...

            def callee():
                try:
                    hurryup()
                except TimeoutException:
                    print "The function didn't complete in 5 seconds."

    Note:
        Implemented using :code:`with time_limit(x):`.

    """

    def __init__(self, timeout):
        """Constructor, saves timeout for use inside __call__."""
        self.timeout = timeout

    def __call__(self, function):
        """The function decorator implementing the annotation."""
        def wrapped_function(*args):
            """The function which is returned in place of the original."""
            with time_limit(self.timeout):
                return function(*args)
        return wrapped_function


def get_http_response(view, request, *args, **kwargs):
    """Render a view using the provided request.

    Handles view functions and class-based views.
    """
    response = view(request, *args, **kwargs)
    if isinstance(response, SimpleTemplateResponse):
        return response.render()
    elif isinstance(response, HttpResponse):
        return response
    else:
        raise ValueError(_('Unknown subview type'))


def get_user_message_admin():
    """Lookup or create message admin user.

    Used as catch-all recipient for messages from Applicants.
    """
    # pylint: disable=W9903
    try:
        return get_user_model().objects.get(username='message_admin')
    except get_user_model().DoesNotExist:
        user = get_user_model()(
            username="message_admin", is_active=True,
            is_superuser=False, is_staff=True,
            last_login=timezone.now()
        )
        user.first_name = 'Message admin'
        user.set_unusable_password()
        user.changeReason = 'Created'
        # pylint: disable=protected-access
        user._history_user = get_user_ubs_admin()
        user.save()

        group, _ = Group.objects.get_or_create(name='ubsadmin')
        group.user_set.add(user)
        group.save()

        return user


def get_user_unimported():
    """Get or create dummy user to represent unimported user."""
    # pylint: disable=W9903
    username = 'unimported_user'
    try:
        return get_user_model().objects.get(username=username)
    except get_user_model().DoesNotExist:
        user = get_user_model()(
            username=username,
            is_active=True,
            is_superuser=False,
            is_staff=True,
            last_login=timezone.now()
        )
        user.first_name = 'Ikke-importeret bruger'
        user.set_unusable_password()
        user.changeReason = 'Created'
        # pylint: disable=protected-access
        user._history_user = get_user_ubs_admin()
        user.save()

        return user


def get_applicant_unimported():
    """Get or create dummy applicant to represent unimported applicant."""
    applicant, _ = webapp.models.Applicant.objects.get_or_create(
        applicant_number='00000000',
        user=get_user_unimported()
    )
    return applicant


def get_user_ubs_admin():
    """Lookup or create ubs admin user."""
    # pylint: disable=W9903
    try:
        return get_user_model().objects.get(username='ubsadmin')
    except get_user_model().DoesNotExist:
        return _create_ubs_admin()


def _create_ubs_admin():
    # pylint: disable=W9903
    from django.conf import settings

    username = 'ubsadmin'
    user = get_user_model()(
        username=username,
        is_active=True,
        is_superuser=True,
        is_staff=True,
        email=username + "@system.com",
        first_name=username,
        last_login=timezone.now()
    )
    user.set_password(settings.DEFAULT_ADMIN_PASSWORD)
    user.changeReason = 'Created'

    # Disable pre_save to prevent full_clean, which will cause
    # ValidationError if no _history_user is set.
    # We cannot set any user as the one we are creating is the very first.

    # Disable full_clean (which checks for changeReason and user)
    signals.pre_save.disconnect(core.apps.pre_save_full_clean_handler)
    # Disable setting change user, since we are creating first
    signals.pre_save.disconnect(
        webapp.models.util_historical.pre_save_model_historical,
        get_user_model()
    )

    user.save()

    signals.pre_save.connect(core.apps.pre_save_full_clean_handler)
    signals.pre_save.connect(
        webapp.models.util_historical.pre_save_model_historical,
        get_user_model()
    )

    group, _ = Group.objects.get_or_create(name='ubsadmin')
    group.user_set.add(user)
    group.save()
    return user
