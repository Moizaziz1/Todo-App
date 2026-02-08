from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session
from sqlalchemy.exc import IntegrityError
from ...services.auth_service import AuthService
from ...services.database import get_session
from ...models.user import UserCreate, UserSignIn
from ..schemas.auth import SignUpRequest, SignInRequest, AuthResponse, ErrorResponse
from ..schemas.user import UserRead


router = APIRouter()


@router.post(
    "/signup",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input or email already exists"},
    },
    summary="Register a new user",
    description="Create a new user account with email and password. Returns JWT token on success."
)
async def signup(
    signup_data: SignUpRequest,
    session: Session = Depends(get_session)
) -> AuthResponse:
    """
    Register a new user account.

    Args:
        signup_data: User signup information (email and password)
        session: Database session

    Returns:
        AuthResponse with access token and user information

    Raises:
        HTTPException 400: If email already exists or validation fails
    """
    # Check if user already exists
    existing_user = AuthService.get_user_by_email(session, signup_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create user data model
    user_data = UserCreate(
        email=signup_data.email,
        password=signup_data.password
    )

    try:
        # Create the user
        user = AuthService.create_user(session, user_data)

        # Generate JWT token using external_id (UUID)
        access_token = AuthService.create_access_token(
            user_id=user.external_id,
            email=user.email
        )

        # Return authentication response
        return AuthResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserRead(
                id=user.id,
                external_id=user.external_id,
                email=user.email,
                created_at=user.created_at
            )
        )

    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        )


@router.post(
    "/signin",
    response_model=AuthResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid credentials"},
    },
    summary="Sign in a user",
    description="Authenticate user with email and password. Returns JWT token on success."
)
async def signin(
    signin_data: SignInRequest,
    session: Session = Depends(get_session)
) -> AuthResponse:
    """
    Authenticate a user and return JWT token.

    Args:
        signin_data: User signin information (email and password)
        session: Database session

    Returns:
        AuthResponse with access token and user information

    Raises:
        HTTPException 401: If credentials are invalid
    """
    # Authenticate user
    user = AuthService.authenticate_user(
        session,
        signin_data.email,
        signin_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate JWT token using external_id (UUID)
    access_token = AuthService.create_access_token(
        user_id=user.external_id,
        email=user.email
    )

    # Return authentication response
    return AuthResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserRead(
            id=user.id,
            external_id=user.external_id,
            email=user.email,
            created_at=user.created_at
        )
    )


@router.get(
    "/me",
    response_model=UserRead,
    responses={
        401: {"model": ErrorResponse, "description": "Not authenticated"},
    },
    summary="Get current user",
    description="Get the currently authenticated user's information from the JWT token."
)
async def get_current_user_info(
    session: Session = Depends(get_session)
) -> UserRead:
    """
    Get the currently authenticated user's information.

    This endpoint demonstrates JWT token verification.
    The actual user extraction would use the get_current_user dependency.

    Args:
        session: Database session

    Returns:
        Current user information

    Raises:
        HTTPException 401: If not authenticated
    """
    # Note: In a real implementation, you would use:
    # current_user: CurrentUser = Depends(get_current_user)
    # Then fetch the full user data from the database using current_user.user_id

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Endpoint requires authentication middleware integration"
    )
