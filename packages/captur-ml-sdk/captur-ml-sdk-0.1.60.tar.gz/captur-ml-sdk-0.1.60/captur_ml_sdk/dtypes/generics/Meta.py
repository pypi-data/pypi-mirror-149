from pydantic import (
    BaseModel, HttpUrl
)
from typing import Optional


class Meta(BaseModel):
    webhooks: Optional[HttpUrl]


class TrainingMeta(BaseModel):
    webhooks: Optional[HttpUrl]
    budget_milli_node_hours: Optional[int] = 8000
