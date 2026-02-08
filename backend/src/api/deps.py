from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from typing import Generator, Annotated
from ..services.database import get_session
from ..config.settings import settings
from pydantic import BaseModel
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError


# OAuth2 scheme for Bearer token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)


class TokenData(BaseModel):
    """Data extracted from JWT token."""
    user_id: str
    email: str | None = None


class CurrentUser(BaseModel):
    """Authenticated user information from JWT token."""
    user_id: str
    email: str | None = None


def get_db() -> Generator[Session, None, None]:
    """
    Get database session dependency.
    """
    with Session() as session:
        yield session


async def get_current_user(
    token: str | None = Depends(oauth2_scheme)
) -> CurrentUser:
    """
    Verify JWT token and extract user information.

    Args:
        token: Bearer token from Authorization header

    Returns:
        CurrentUser with user_id and email

    Raises:
        HTTPException 401: If token is missing, invalid, or expired
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if token is None:
        raise credentials_exception

    try:
        # Decode the JWT token using shared secret
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )

        # Extract user_id from 'sub' claim (standard JWT subject)
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception

        # Extract email if present
        email: str | None = payload.get("email")

        return CurrentUser(user_id=user_id, email=email)

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError:
        raise credentials_exception


async def get_optional_user(
    token: str | None = Depends(oauth2_scheme)
) -> CurrentUser | None:
    """
    Optionally verify JWT token - returns None if not authenticated.
    Useful for endpoints that work with or without authentication.
    """
    if token is None:
        return None

    try:
        return await get_current_user(token)
    except HTTPException:
        return None


def verify_user_access(current_user: CurrentUser, user_id: str) -> None:
    """
    Verify that the current user has access to the requested user_id's resources.

    Args:
        current_user: The authenticated user from JWT
        user_id: The user_id from the URL path

    Raises:
        HTTPException 404: If user_id doesn't match (prevents enumeration)
    """
    if current_user.user_id != user_id:
        # Return 404 instead of 403 to prevent resource enumeration
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found",
        )


# Type alias for dependency injection
AuthenticatedUser = Annotated[CurrentUser, Depends(get_current_user)]
OptionalUser = Annotated[CurrentUser | None, Depends(get_optional_user)]
DBSession = Annotated[Session, Depends(get_session)]
