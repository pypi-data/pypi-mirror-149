"""
Package: src.src
Filename: helpers.py
Author(s): Grant W

Description: General helpers
"""
# Python Imports
import os
import random
import time

# Third Party Imports
import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import ReadTimeout, ConnectionError

# Local Imports
from .exceptions import HttpTimeoutException, RexServiceException


DEFAULT_TIMEOUT = int(os.environ.get('DEFAULT_TIMEOUT', '60'))
DEFAULT_RETRIES = int(os.environ.get('DEFAULT_RETRIES', '3'))


class TimeoutHTTPAdapter(HTTPAdapter):

    def _wait(self, try_number):
        interval = (2 ** try_number) + (random.randint(0, 1000) / 1000)
        time.sleep(interval)
        return

    def __init__(self, *args, **kwargs):
        _kwargs = {k: v for k, v in kwargs.items() if k != 'request_timeout'}
        super().__init__(*args, **_kwargs)
        self.maximum_retries = DEFAULT_RETRIES

    def send(self, request, try_count=1, **kwargs):
        if "request_timeout" in kwargs:
            request_timeout = kwargs["request_timeout"]
            del kwargs["request_timeout"]
        else:
            request_timeout = DEFAULT_TIMEOUT
        kwargs["timeout"] = request_timeout
        try:
            return super().send(request, **kwargs)
        except ReadTimeout as e:
            raise HttpTimeoutException(e)
        except ConnectionError as e:
            try_count += 1
            if try_count > self.maximum_retries:
                raise RexServiceException from e
            self._wait(try_count)
            return self.send(request, try_count=try_count, **kwargs)


def make_session(request_timeout=DEFAULT_TIMEOUT):
    """Make a session and mount the TimeoutHTTPAdapter"""
    session = requests.Session()
    adapter = TimeoutHTTPAdapter(request_timeout=request_timeout)
    # TODO: Set dynata_rex.__version__ and use instead of 0.0.1
    session.headers["User-Agent"] = 'rex-sdk-python/0.0.1'
    session.mount('https://', adapter)
    session.mount('http://', adapter)
    return session
