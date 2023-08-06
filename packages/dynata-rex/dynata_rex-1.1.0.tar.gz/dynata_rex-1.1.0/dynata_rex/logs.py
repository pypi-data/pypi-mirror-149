"""
Package: src.src
Filename: logs
Author(s): Grant W, Nick P

Description: logging
"""
# Python Imports
import logging
import os

# Third Party Imports

# Local Imports

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()


def create_logger(level):
    logger = logging.getLogger(__name__)
    logger.setLevel(level)
    return logger


logger = create_logger(LOG_LEVEL)
