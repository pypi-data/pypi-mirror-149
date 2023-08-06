from typing import List, Optional

from pydantic import BaseModel

from .base_wrapper import BaseWrapper
from .JSONType import JSONType


class KernelVariable(BaseModel):
    name: str
    type: Optional[str]
    value: JSONType
    summary: Optional[str]


class KernelVariablesWrapper(BaseWrapper):
    vars: List[KernelVariable]
