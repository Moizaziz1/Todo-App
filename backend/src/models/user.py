from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid


class UserBase(SQLModel):
    """Base user model with common fields"""
    email: str = Field(unique=True, index=True, max_length=255)


class User(UserBase, table=True):
    """
    User model representing a user in the database.
    Stores user credentials and authentication information.
    """
    __tablename__ = "user"

    id: Optional[int] = Field(default=None, primary_key=True)
    external_id: str = Field(default_factory=lambda: str(uuid.uuid4()), unique=True, index=True)
    email: str = Field(unique=True, index=True, max_length=255)
    hashed_password: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UserRead(SQLModel):
    """Response model for reading user data (excludes password)"""
    id: int
    external_id: str
    email: str
    created_at: datetime


class UserCreate(SQLModel):
    """Model for creating new users"""
    email: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=8, max_length=255)


class UserSignIn(SQLModel):
    """Model for user sign in"""
    email: str
    password: str
