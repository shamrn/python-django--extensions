from dataclasses import dataclass
from typing import Union, TypedDict

from reference.services.enums import GenerateFilterTypeEnum


# Typing for generate filter
# --------------------------------------------------------------------------------------------------
class GenerateFilterOption(TypedDict):
    id: str
    name: str


@dataclass
class GeneratedFilter:
    display_text: str
    query_parameter: str
    selection_type: Union[GenerateFilterTypeEnum.MULTIPLE, GenerateFilterTypeEnum.SINGLE]
    options: list[GenerateFilterOption]
