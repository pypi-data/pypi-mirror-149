"""
Package: dynata-rex.models
Filename: opportunity_registry.py
Author(s): Grant W

Description: Implementation of dataclasses for Opportunity Registry opps
"""
# Python Imports
from enum import Enum
from typing import List, Optional, Union
from typing_extensions import Literal

# Third Party Imports
from pydantic import Field, HttpUrl

# Local Imports
from .base import HashableModel, FallbackEnum


class CategoryEnum(FallbackEnum):
    DEFAULT = 0
    AUTOMOTIVE = 550
    BEVERAGES_ALCOHOLIC = 551
    BEVERAGES_NON_ALCOHOLIC = 552
    BUSINESS = 553
    CHILDREN_PARENTING = 554
    LOYALTY_PROGRAMS = 555
    DESTINATIONS_TOURISM = 556
    EDUCATION = 557
    ELECTRICS_COMPUTERS = 558
    ENTERTAINMENT_LEISURE = 559
    FASHION_CLOTHING = 560
    FINANCE = 561
    FOOD = 562
    GAMBLING_LOTTERY = 563
    GOVERNMENT_POLITICS = 564
    HEALTHCARE = 565
    HOME = 566
    MEDIA_PUBLISHING = 567
    PERSONAL_CARE = 568
    RESTAURANTS = 569
    SENSITIVE_CONTENT = 570
    SMOKING = 571
    SOCIAL_RESEARCH = 572
    SPORTS_FITNESS = 573
    TELECOMMUNICATIONS = 574
    TRANSPORTATION = 575
    TRAVEL_AIRLINES = 576
    TRAVEL_HOTELS = 577
    TRAVEL_SERVICES = 578
    CREDIT_CARDS = 581
    VIDEO_GAMES = 582
    FASHION_CLOTHING_DEPARTMENT_STORE = 583
    ADHOC = 587


class StatusEnum(Enum):
    OPEN = "OPEN"
    PAUSED = "PAUSED"
    CLOSED = "CLOSED"


class EvaluationEnum(Enum):
    STARTS = "STARTS"
    COMPLETES = "COMPLETES"


class DevicesEnum(Enum):
    MOBILE = "mobile"
    DESKTOP = "desktop"
    TABLET = "tablet"


class CellTypeEnum(Enum):
    VALUE = "VALUE"
    RANGE = "RANGE"
    LIST = "LIST"
    COLLECTION = "COLLECTION"


class Locale(HashableModel):
    language: str
    country: str


class Range(HashableModel):
    from_: Union[int, None] = Field(alias='from')
    to: Union[int, None] = None


class Cell(HashableModel):
    tag: str
    attribute_id: int
    negate: bool
    kind: CellTypeEnum


class RangeCell(Cell):
    kind: Literal[CellTypeEnum.RANGE.value]
    range_: Range = Field(alias='range')


class ValueCell(Cell):
    kind: Literal[CellTypeEnum.VALUE.value]
    value: str = None


class ListCell(Cell):
    kind: Literal[CellTypeEnum.LIST.value]
    list_: List[str] = Field(alias='list')


class CollectionCell(Cell):
    kind: Literal[CellTypeEnum.COLLECTION.value]
    collection_: str = Field(alias='collection')


class Links(HashableModel):
    live: HttpUrl
    # test: HttpUrl


class Quota(HashableModel):
    id: str
    cells: List[str]
    count: int
    status: StatusEnum


class Filter(HashableModel):
    id: str
    cells: List[str]


class Opportunity(HashableModel):

    class Config:
        allow_population_by_field_name = True
        validate_assignment = True
        allow_mutation = False

    id: int
    status: StatusEnum
    length_of_interview: int
    incidence_rate: int
    cost_per_interview: float
    completes: int
    project_id: int
    group_id: int
    evaluation: EvaluationEnum
    days_in_field: int
    locale: Locale
    links: Links
    client_id: Optional[Union[None, int]]

    project_exclusions: List[int]
    category_exclusions: List[CategoryEnum]
    category_ids: List[CategoryEnum]
    devices: List[DevicesEnum]
    filters: List[List[Filter]]
    cells: List[Union[RangeCell, ListCell, ValueCell, CollectionCell]]
    quotas: List[List[Quota]]
