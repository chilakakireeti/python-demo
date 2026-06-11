from pydantic import BaseModel,EmailStr,Field,field_validator
from enum import Enum
from app.utils import validate_email_domine





class signup(BaseModel):
    email:EmailStr
    username: str=Field(..., min_length=3, max_length=20)
    mobile:int=Field(...,max_length=10)
    

    @field_validator('email')
    @classmethod
    def validate_email(cls,value):
        return validate_email_domine(value)


class otp_validation(BaseModel):
    email:EmailStr
    otp:str    




      
