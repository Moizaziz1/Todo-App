from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserRead(BaseModel):
    """Response model for reading user data"""
    id: int
    external_id: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True
