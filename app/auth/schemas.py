from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr = Field(description="Valid email address")
    password: str = Field(
        min_length=8,
        max_length=50,
        description="Password must be between 8 and 50 characters",
    )
    fullname: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=255,
        description="Full name, between 3 and 255 characters",
    )

class UserResponse(BaseModel):
    id: int
    email: str
    fullname: Optional[str]
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr = Field(description="Registered email address")
    password: str = Field(min_length=8, max_length=50, description="Account password")

class Token(BaseModel):
    access_token: str = Field(description="JWT access token")
    token_type: str = Field(description="Token type, typically 'bearer'")
    
