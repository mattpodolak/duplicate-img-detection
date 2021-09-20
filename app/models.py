from typing import List
from pydantic import BaseModel

class AddResponse(BaseModel):
    added: List[str]