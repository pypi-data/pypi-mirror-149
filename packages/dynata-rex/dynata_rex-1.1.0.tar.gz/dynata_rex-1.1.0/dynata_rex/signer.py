"""
Package: src
Filename: auth.py
Author(s): Grant W
"""
# Python Imports
import hashlib
import hmac
from datetime import datetime, timedelta
import json
from typing import Union
from urllib.parse import urlencode

# Third Party Imports

# Local Imports
from .logs import logger
from .helpers import make_session
from .exceptions import HttpTimeoutException, RexServiceException


class Signer:
    """
    Create signatures for requests to the Rex Registry API and Gateway
    """
    def __init__(self,
                 access_key: str,
                 secret_key: str,
                 signing_string: str = '',
                 default_ttl: int = 10):
        self.access_key = access_key
        self.secret_key = secret_key
        self.signing_string = signing_string
        self.default_ttl = default_ttl

    def is_expired(self, expiration_date_str: str) -> bool:
        """Check if the expiration date is in the past
        """
        expiration_date = datetime.strptime(expiration_date_str,
                                            '%Y-%m-%dT%H:%M:%S.%fZ')
        return expiration_date < datetime.utcnow()

    @staticmethod
    def digest(signing_key: str, message: str, encoding='utf-8') -> str:
        """
        Create a digest from signing_key & message
        """
        _hmac = hmac.new(
            key=bytes(signing_key, encoding=encoding),
            msg=bytes(message, encoding=encoding),
            digestmod=hashlib.sha256
        )
        return _hmac.hexdigest()

    @staticmethod
    def create_expiration_date(ttl: int) -> str:
        """
        Create a formatted date string from now + ttl in seconds
        - expected format:         "2021-03-30T14:17:29.208Z"
        - python isoformat outputs '2021-03-30T14:17:29.208292', so we have to
        strip the last 3, and append the Z.
        :ttl : int - seconds
        """
        return (datetime.utcnow() + timedelta(seconds=ttl)) \
            .isoformat(timespec="milliseconds") + "Z"

    @classmethod
    def sign_from_ttl(cls,
                      access_key,
                      secret_key,
                      ttl,
                      signing_string: str = '') -> (str, str):
        expiration_date_str = cls.create_expiration_date(ttl)
        first = cls.digest(expiration_date_str, signing_string)
        second = cls.digest(access_key, first)
        final = cls.digest(secret_key, second)
        return final, expiration_date_str

    @classmethod
    def sign_from_expiration_date(cls,
                                  access_key,
                                  secret_key,
                                  expiration_date_str,
                                  signing_string: str = ''
                                  ) -> (str, str):
        first = cls.digest(expiration_date_str, signing_string)
        second = cls.digest(access_key, first)
        final = cls.digest(secret_key, second)
        return final, expiration_date_str

    def _create_query_params_signing_string(self, parameters: dict) -> str:
        """Create a signing string for use in Gateway from query parameters
        """
        if 'signing_string' in parameters:
            del parameters['signing_string']
        if 'signature' in parameters:
            del parameters['signature']
        sorted_params = sorted(parameters.items())
        encoded_params = urlencode(sorted_params)
        return hashlib.sha256(encoded_params.encode('utf-8')).hexdigest()

    def _create_request_body_signing_string(self, request_body: str) -> str:
        """SHA256 digest of the request body as a hexidecimal string
        in lowercase
        """
        return hashlib.sha256(request_body.encode('utf-8')).hexdigest()

    def sign_query_params_from_expiration_date(self,
                                               parameters: dict,
                                               expiration_date_str: str,
                                               access_key: str = None,
                                               secret_key: str = None,
                                               as_dict=False) -> str:
        if access_key is None:
            access_key = self.access_key
        if secret_key is None:
            secret_key = self.secret_key
        parameters['access_key'] = access_key
        parameters['expiration'] = expiration_date_str
        signing_string = self._create_query_params_signing_string(parameters)
        parameters['signing_string'] = signing_string
        signature, _ = self.sign_from_expiration_date(access_key,
                                                      secret_key,
                                                      expiration_date_str,
                                                      signing_string)
        parameters['signature'] = signature

        # Remove signing string for smrg
        del parameters['signing_string']
        if as_dict:
            return parameters
        return urlencode(parameters, doseq=True)

    def sign_query_parameters_from_expiration_date(self, *args, **kwargs):
        return self.sign_query_params_from_expiration_date(*args, **kwargs)

    def sign_query_params_from_ttl(self, *args, **kwargs):
        return self.sign_query_parameters_from_ttl(*args, **kwargs)

    def sign_query_parameters_from_ttl(self,
                                       parameters: dict,
                                       ttl: Union[int, None] = None,
                                       access_key: str = None,
                                       secret_key: str = None,
                                       as_dict=False) -> str:
        if ttl is None:
            ttl = self.ttl
        expiration_date_str = self.create_expiration_date(ttl)
        return self.sign_query_params_from_expiration_date(parameters,
                                                           expiration_date_str,
                                                           access_key,
                                                           secret_key,
                                                           as_dict)


class RexRequest:
    """Wrapper for http calls to include our signature"""

    def __init__(self,
                 access_key,
                 secret_key,
                 default_ttl: int = 10):
        self.default_ttl = default_ttl
        self.access_key = access_key
        self.secret_key = secret_key
        self.signer = Signer(access_key, secret_key)
        self.session = make_session()

    def _signature(self, ttl: int = None, signing_string: str = None) -> str:
        if ttl is None:
            ttl = self.default_ttl
        return self.signer.sign_from_ttl(
            self.access_key,
            self.secret_key,
            ttl,
            signing_string=signing_string
        )

    def _create_auth_headers(self,
                             additional_headers={},
                             body=''):
        signing_string = self.signer._create_request_body_signing_string(body)

        signature, expiration = self._signature(signing_string=signing_string)
        base = {
            'dynata-expiration': expiration,
            'dynata-access-key': self.access_key,
            'dynata-signature': signature,
            'dynata-signing-string': signing_string
        }
        return dict(additional_headers, **base)

    def dispatch(self,
                 url,
                 data='',
                 method='GET') -> Union[dict, str]:

        additional_headers = {}
        if data:
            additional_headers = {'Content-type': 'application/json'}
            data = json.dumps(data)

        headers = self._create_auth_headers(additional_headers,
                                            body=data)

        if not hasattr(self.session, method.lower()):
            raise AttributeError('Invalid http method provided.')

        method = getattr(self.session, method.lower())

        res = method(url, data=data, headers=headers)
        if res.status_code > 299:
            if res.status_code == 504:
                raise HttpTimeoutException(res.content)
            if data:
                logger.warning(data)
            logger.warning(res.__dict__)
            raise RexServiceException(res.content.decode('utf-8'))
        try:
            return res.json()
        except json.decoder.JSONDecodeError as e:
            if res.status_code != 204:
                logger.debug(str(e), res.__dict__, exc_info=1)
        return res.content.decode('utf-8')

    def get(self, url: str):
        return self.dispatch(url)

    def post(self, url, data):
        return self.dispatch(url, data=data, method='POST')
