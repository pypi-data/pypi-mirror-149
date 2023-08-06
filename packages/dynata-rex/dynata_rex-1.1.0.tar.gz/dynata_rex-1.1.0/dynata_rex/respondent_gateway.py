"""
Package: src.dynata_rex
Filename: respondent_gateway.py
Author(s): Grant W

Description: Respondent Gateway interactions
"""
# Python Import
from urllib.parse import urlparse, parse_qsl, unquote, urlencode
from typing import Union
from copy import copy

# Third Party Imports

# Local Imports
from dynata_rex.models import GatewayDispositionsEnum, GatewayStatusEnum
from .signer import Signer, RexRequest
from .exceptions import SignatureExpiredException, SignatureInvalidException


class RespondentGateway:
    """
    Respondent Gateway interactions
    """

    _BASE_URL = 'https://respondent.rex.dynata.com'

    def __init__(self,
                 access_key: str,
                 secret_key: str,
                 base_url: str = _BASE_URL,
                 default_ttl: int = 10):
        """
        @access_key: liam access key for REX
        @secret_key: liam secret key for REX

        # Optional
        @base_url: url of Gateway
        @ttl: time to live for signature in seconds
        """
        self.access_key = access_key
        self.secret_key = secret_key
        self.default_ttl = default_ttl
        self.base_url = base_url

        # MR for API requests
        self.make_request = RexRequest(access_key,
                                       secret_key,
                                       default_ttl=default_ttl)
        # Signer for signing/verifying URLs
        self.signer = Signer(access_key, secret_key, default_ttl=default_ttl)

    def create_respondent_url(self,
                              url: str,
                              birth_date: str,
                              gender: str,
                              postal_code: str,
                              respondent_id: str,
                              additional_params: dict = None,
                              ttl: Union[int, None] = None,
                              url_quoting: bool = False) -> str:
        """
        Creates a url from the url of an opportunity + the required
        parameters for entry into the respondent gateway.

        @url: live/test url of an opportunity
        @birth_date: birth date in ISO8601 (YYYY-MM-DD) format
        @gender: 'male' / 'female'
        @postal: postal code as string
        @respondent_id : unique identifier for the respondent

        @additional_params: additional parameters that will be included
            on the return back from the survey
        @ttl: time to live for signature in seconds
        @url_quoting: whether to URL quote the returned URL
        """
        parsed = urlparse(url)
        base_params = dict(parse_qsl(parsed.query))
        if additional_params:
            base_params = dict(base_params, **additional_params)
        required_params = {
            'birth_date': birth_date,
            'gender': gender,
            'postal_code': postal_code,
            'respondent_id': respondent_id
        }
        final_params = dict(base_params, **required_params)
        updated_query = urlencode(final_params, doseq=True)
        parsed = parsed._replace(query=updated_query)
        return self.sign_url(parsed.geturl(), ttl=ttl, url_quoting=url_quoting)

    def sign_url(self,
                 url,
                 ttl: Union[int, None] = None,
                 url_quoting: bool = False) -> str:
        """
        Sign a URL with the given access and secret keys

        @url: URL to sign
        @ttl: time to live for signature in seconds
        @url_quoting: whether to URL quote the returned URL
        """
        if not ttl:
            ttl = self.default_ttl
        parsed = urlparse(url)
        query_parameters = dict(parse_qsl(parsed.query))
        signed_params = self.signer.sign_query_parameters_from_ttl(
            query_parameters, ttl=ttl)
        updated = parsed._replace(query=signed_params).geturl()
        if url_quoting:
            return updated
        return unquote(updated)

    def verify_query_parameters(self,
                                query_parameters: dict,
                                access_key: str = None,
                                secret_key: str = None) -> bool:
        """
        Verify a signature on query parameters match the expected output
        from a pair of access and secret keys. Returns True if the signature
        matches, False otherwise.

        @query_parameters: dictionary of query parameters

        Optional
        @access_key: liam access key for signing
        @secret_key: liam secret key for signing
        """
        parameters = copy(query_parameters)
        if access_key is None:
            access_key = self.access_key
        if secret_key is None:
            secret_key = self.secret_key
        expiration_date_str = parameters.pop('expiration')
        if self.signer.is_expired(expiration_date_str):
            raise SignatureExpiredException
        original_signature = parameters.pop('signature')
        signed = self.signer.sign_query_params_from_expiration_date(
            parameters, expiration_date_str, access_key, secret_key,
            as_dict=True
        )
        if original_signature != signed['signature']:
            raise SignatureInvalidException
        return True

    def verify_url(self,
                   url,
                   access_key: str = None,
                   secret_key: str = None) -> bool:
        """
        Verify a URL's signature matches for the given access and secret keys
        @url: URL to verify

        Optional
        @access_key: liam access key for signing
        @secret_key: liam secret key for signing
        """
        if access_key is None:
            access_key = self.access_key
        if secret_key is None:
            secret_key = self.secret_key
        parsed = urlparse(url)
        query_parameters = dict(parse_qsl(parsed.query))
        try:
            return self.verify_query_parameters(query_parameters,
                                                access_key=access_key,
                                                secret_key=secret_key)
        except (KeyError,
                SignatureExpiredException,
                SignatureInvalidException):
            return False

    def get_respondent_disposition(
            self, url) -> Union[GatewayDispositionsEnum, None]:
        """
        Get the disposition of a respondent from a URL

        @url: URL to get disposition from
        """
        parsed = urlparse(url)
        query_parameters = dict(parse_qsl(parsed.query))
        try:
            disposition = int(query_parameters['disposition'])
            return GatewayDispositionsEnum(disposition)
        except KeyError:
            return None

    def get_respondent_status(
            self, url) -> Union[GatewayStatusEnum, None]:
        """
        Get the status of a respondent from a URL

        @url: URL to get status from
        """
        parsed = urlparse(url)
        query_parameters = dict(parse_qsl(parsed.query))
        disposition = self.get_respondent_disposition(url)
        if not disposition:
            return None
        try:
            status = int(query_parameters['status'])
            return GatewayStatusEnum((disposition, status))
        except KeyError:
            return None

    def create_context(self, context_id: str, context_data: dict) -> int:
        """
        Create a context with the given context_id and context_data

        @context_id: unique identifier for the context
        @context_data: dictionary of context data ie:
            {
                "ctx": "a987dsglh34t435jkhsdg98u",
                "gender": "male",
                "postal_code": "60081",
                "birth_date": "1959-10-05",
                "country": "US"
            }
        """
        endpoint = f"{self.base_url}/create-context"
        data = {
            "id": context_id,
            "items": context_data
        }
        response = self.make_request.post(endpoint, data)
        return response['id']

    def expire_context(self, context_id: str) -> None:
        """
        Expire a context with the given context_id and account_id

        @context_id: identifier for the context
        """
        endpoint = f"{self.base_url}/expire-context"
        data = {"id": context_id}
        res = self.make_request.post(endpoint, data)
        return res if res else None

    def get_context(self, context_id: int) -> dict:
        """
        Get specific opportunity from SMOR

        @context_id: identifier for the context
        """
        endpoint = f"{self.base_url}/get-context"
        data = {"id": context_id}
        return self.make_request.post(endpoint, data)

    def get_attribute_info(self, attribute_id: int) -> dict:
        """
        Get parameter info about a specific attribute id

        @attribute_id: specific singular id for a parameter item
        """
        endpoint = f"{self.base_url}/get-attribute-info"
        data = {"id": attribute_id}
        return self.make_request.post(endpoint, data)

    def get_attributes(self,
                       country: str,
                       page_number: int,
                       page_size: int) -> dict:
        """
        Get a list of attribute id's and their statuses

        @country: Country code for which you would like attributes

        @page_number: What page number you are requesting (for pagination)

        @page_size: How many id's you would like returned in each page
        """
        endpoint = f"{self.base_url}/get-attributes"
        data = {
            "country": country,
            "page_number": page_number,
            "page_size": page_size
        }
        return self.make_request.post(endpoint, data)
