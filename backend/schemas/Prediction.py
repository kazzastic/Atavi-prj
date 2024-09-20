from pydantic import BaseModel
from typing import Any

class PredictionStore(BaseModel):
    id: int
    data: Any  # This will hold the JSON data

    class Config:
        orm_mode = True
