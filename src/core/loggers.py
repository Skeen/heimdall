# pylint: disable=invalid-name
"""This module contains a list of loggers to be included and used elsewhere."""
import logging

auth_logger = logging.getLogger('authentication')
"""Logger for authentication specific messages."""

celery_logger = logging.getLogger('celery')
"""Logger for asyncroneous computation."""

webapp_logger = logging.getLogger('webapp')
"""Logger for webapp specific messages."""
