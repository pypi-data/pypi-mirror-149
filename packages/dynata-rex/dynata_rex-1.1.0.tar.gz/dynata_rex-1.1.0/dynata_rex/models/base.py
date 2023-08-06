"""
Package: src.models
Filename: base.py
Author(s): Grant W

Description: Base models for REX sdk
"""
# Python Imports
import hashlib
from enum import Enum

# Third Party Imports
from pydantic import BaseModel

# Local Imports


class BaseObject:
    def __str__(self):
        return f"<dynata_rex.{self.__class__.__name__}>"


class HashableModel(BaseObject, BaseModel):
    """
    Base class for all objects in the Opportunity Registry
    """
    def __hash__(self):
        try:
            return hash((type(self),) + tuple(self.__dict__.values()))
        except TypeError:
            _json = self.json(sort_keys=True)
            to_hash = str(type(self)) + _json
            digest = hashlib.sha256(to_hash.encode('utf-8')).hexdigest()
            return int(digest, 16) % 10**19


class FallbackEnum(Enum):
    """Override missing prop to return a default if defined"""

    @classmethod
    def _missing_(cls, value):
        if hasattr(cls, 'DEFAULT'):
            return getattr(cls, 'DEFAULT')
        raise ValueError(f"Enum {cls.__name__} does not have a defined "
                         "default value")
