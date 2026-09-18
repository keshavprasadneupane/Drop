from enum import Enum
from pydantic import BaseModel

class Gender(str, Enum):
    Male = "male"
    Female = "female"
    Others = "others"
    
class Product(BaseModel):
    itemname: str
    description: str
    availability: str
    gender: Gender
    images: list[str]
    price: float
    ratings: int
    available_sizes: list[str]
    details_and_care: list[str]
    shipping_and_return: list[str]
    