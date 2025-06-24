from typing import Optional
from pydantic import BaseModel, Field

class LiteLLmAPIConfig(BaseModel):
    model: str
    api_key: str
    api_base: Optional[str] = Field(default=None)
    api_version: Optional[str] = Field(default=None)