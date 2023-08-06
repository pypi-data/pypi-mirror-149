from captur_ml_sdk.dtypes.generics import Image, Meta
from pydantic import BaseModel
from typing import List, Optional, Dict

class EvalEventData(BaseModel):
    request_id: str
    webhooks: str
    images: List[Image]
    model_name: str
    model_id: str
    model_type: str
    mapping: Optional[Dict[str, Dict[str, str]]]
