"""
Package: dynata-rex.models
Filename: respondent_gateway.py
Author(s): Grant W

Description: Implementation of dataclasses for Respondent Gateway
"""
# Python Imports
from enum import Enum


class GatewayGenderEnum(Enum):
    MALE = 1
    FEMALE = 2


class GatewayDispositionsEnum(Enum):
    UNKNOWN = 0
    COMPLETE = 1
    TERMINATION = 2
    OVERQUOTA = 3
    DUPLICATE = 4
    QUALITY = 5


class GatewayStatusEnum(Enum):
    """
    Composite status code from Disposition + non-unique status code
    Must call as tuple of Gateway Disposition + Status code
    ie
    >>> disp_code, status_code = 1, 0
    >>> disp = GatewayDispositionsEnum(disp_code)
    >>> status = RespondentGatewayStatusEnum((disp, status_code))
    >>> status.name
    'COMPLETE_DEFAULT`
    >>> status.value
    (<GatewayDispositionsEnum.COMPLETE: 1>, 0)
    """
    UNKNOWN_DEFAULT = GatewayDispositionsEnum.UNKNOWN, 0
    COMPLETE_DEFAULT = GatewayDispositionsEnum.COMPLETE, 0
    COMPLETE_PARTIAL = GatewayDispositionsEnum.COMPLETE, 1
    TERMINATION_DYNATA = GatewayDispositionsEnum.TERMINATION, 1
    TERMINATION_CLIENT = GatewayDispositionsEnum.TERMINATION, 2
    OVERQUOTA_DYNATA = GatewayDispositionsEnum.OVERQUOTA, 1
    OVERQUOTA_CLIENT = GatewayDispositionsEnum.OVERQUOTA, 2
    DUPLICATE_DEFAULT = GatewayDispositionsEnum.DUPLICATE, 0
    QUALITY_ANSWER = GatewayDispositionsEnum.QUALITY, 1
    QUALITY_SPEEDING = GatewayDispositionsEnum.QUALITY, 2
    QUALITY_SUSPENDED = GatewayDispositionsEnum.QUALITY, 3
