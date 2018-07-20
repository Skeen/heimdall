"""Common utils for multiple places."""

import signal
import threading
from contextlib import contextmanager

from django.http import HttpResponse
from django.template.response import SimpleTemplateResponse
from django.utils import timezone
from django.utils.translation import ugettext as _


class Empty(object):
    """Empty class, that can be dynamically expanded."""

    pass


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


# TODO: Combine implementations of set_interval and set_timeout
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
