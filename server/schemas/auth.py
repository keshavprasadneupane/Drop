from pydantic import BaseModel

class UserSignup(BaseModel):
    fullName: str
    email: str
    username: str
    password: str
    
class UserLogin(BaseModel):
    email: str
    password: str