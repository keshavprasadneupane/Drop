from pydantic import BaseModel

class Review(BaseModel):
    product : int
    customer_name : str
    customer_rating : int
    customer_review : str