from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=50, description="Password must be minimum 8 characters")
    fullname: Optional[str] = Field(None, min_length=3, max_length=255, description="Name should be between 3 and 255 characters")
    
class UserResponse(BaseModel):
    id: int 
    email: str
    fullname: str
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
