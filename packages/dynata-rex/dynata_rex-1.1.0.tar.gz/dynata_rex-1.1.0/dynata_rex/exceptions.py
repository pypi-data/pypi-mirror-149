"""
Package: dynata-rex
Filename: exceptions.py
Author(s): Grant W

Description: Exceptions for the dynata-rex package.
"""
# Python Imports

# Third Party Imports

# Local Imports


class RexClientException(Exception):
    """
    Base Exception for all RexClient exceptions.
    """
    pass


class RexServiceException(RexClientException):
    """
    Base Exception for all RexServer exceptions.
    """
    pass


class InvalidShardException(RexClientException):
    pass


class HttpTimeoutException(RexServiceException):
    pass


class InvalidCredentialsException(RexServiceException):
    pass


class SignatureExpiredException(RexClientException):
    pass


class SignatureInvalidException(RexClientException):
    pass
