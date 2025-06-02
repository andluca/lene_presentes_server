from pydantic import BaseModel
from typing import Optional

class UserIn(BaseModel):
    name: str
    email: str
    password_hash: str
    role: str

class ProductIn(BaseModel):
    name: str
    price: float
    category: str
    description: Optional[str] = None