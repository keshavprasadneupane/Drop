from typing import Optional
from pydantic import BaseModel


class Payment(BaseModel):
    product: Optional[int] = None
    product_name: Optional[str] = "DROPP Order"
    cost: float
    quantity: int = 1
    fullname: str
    email_address: str
    shipping_address: str
    city: str
    postal_code: int
    payment_method: str = "Credit Card"
