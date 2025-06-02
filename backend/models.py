from pydantic import BaseModel
from typing import Optional

class UserIn(BaseModel):
    name: str
    email: str
    password_hash: str
    role: str

class ProductInDB(BaseModel):
    name: str
    price: float
    category: str
    description: Optional[str] = None
    image_url: Optional[str] = None

class ProductOut(BaseModel):
    id: str
    name: str
    price: float
    category: str
    description: Optional[str] = None
    image_url: Optional[str] = None
