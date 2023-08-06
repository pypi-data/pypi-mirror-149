from captur_ml_sdk.dtypes.generics import Image, Meta, Model
from pydantic import BaseModel
from typing import List, Optional, Dict


class ModelEvaluateRequest(BaseModel):
    data: List[Image]
    meta: Optional[Meta] = None
    models: List[Model]
    mapping: Optional[Dict[str, Dict[str, str]]]
