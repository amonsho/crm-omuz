from pydantic import BaseModel ,EmailStr
from app.models import RoleEnum


class UserCreate(BaseModel):
    full_name : str
    email : EmailStr
    password : str
    role : RoleEnum

class UserLogin(BaseModel):
    email : EmailStr
    password : str

class TokenResponse(BaseModel):
    acess_token : str
    token_type : str = "bearer"

