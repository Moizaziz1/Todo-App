from pydantic import BaseModel, EmailStr, Field
from ..schemas.user import UserRead


class SignUpRequest(BaseModel):
    """Request model for user signup"""
    email: EmailStr = Field(description="User's email address")
    password: str = Field(min_length=8, max_length=255, description="User's password (min 8 characters)")


class SignInRequest(BaseModel):
    """Request model for user signin"""
    email: EmailStr = Field(description="User's email address")
    password: str = Field(description="User's password")


class AuthResponse(BaseModel):
    """Response model for successful authentication"""
    access_token: str = Field(description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    user: UserRead = Field(description="Authenticated user information")


class ErrorResponse(BaseModel):
    """Response model for errors"""
    detail: str = Field(description="Error message")
