from pydantic import BaseModel , EmailStr, Field

class usercreate(BaseModel):
    name : str = Field(..., max_length = 30)
    email:EmailStr = Field(...)
    password:str = Field(..., min_length = 8)
    

class UserLogin(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(..., min_length = 8)