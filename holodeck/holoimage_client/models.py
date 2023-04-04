from typing import Any  # noqa
from typing import List, Optional

from pydantic import BaseModel, Field


class HTTPValidationError(BaseModel):
    detail: "Optional[List[ValidationError]]" = Field(None, alias="detail")


class ValidationError(BaseModel):
    loc: "List[Any]" = Field(..., alias="loc")
    msg: "str" = Field(..., alias="msg")
    type: "str" = Field(..., alias="type")
