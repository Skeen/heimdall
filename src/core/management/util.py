"""Common utils for core commands."""

import os
import time
import errno
import httplib


def gen_random_id(length=10):
    """Generate a random string."""
    from django.utils.crypto import get_random_string
    # pylint: disable=W9903
    valid_chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    return get_random_string(length, valid_chars)


def process_alive(pid):
    """Test if the process with 'pid' is alive or not."""
    if pid is None:
        return False

    try:
        os.kill(pid, 0)
    except OSError as err:
        if err.errno == errno.ESRCH:
            return False
    return True


def waitpid(pid):
    """Wait until the process with 'pid' is dead."""
    while True:
        if process_alive(pid) is False:
            return
        time.sleep(1)


def get_status_code(host, path="/"):
    """Get the status code of a website.

    This function retreives the status code of a website by requesting HEAD
    data from the host. This means that it only requests the headers.

    If the host cannot be reached or something else goes wrong, it returns
    None instead.

    Note:

        Shamefully stolen from: https://stackoverflow.com/questions/1140661
    """
    try:
        conn = httplib.HTTPConnection(host)
        conn.request("HEAD", path)
        return conn.getresponse().status
    except StandardError:
        return None
    except httplib.BadStatusLine:
        return None
