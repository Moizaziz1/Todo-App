from datetime import datetime, timedelta
from typing import Optional
from sqlmodel import Session, select
import bcrypt
import jwt
from ..models.user import User, UserCreate, UserRead
from ..config.settings import settings


class AuthService:
    """
    Service for handling authentication operations:
    - Password hashing and verification using bcrypt
    - JWT token generation and validation
    - User creation and retrieval
    """

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using bcrypt.

        Args:
            password: Plain text password

        Returns:
            Hashed password as string
        """
        # Generate a salt and hash the password
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against a hashed password.

        Args:
            plain_password: Plain text password to verify
            hashed_password: Hashed password from database

        Returns:
            True if password matches, False otherwise
        """
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )

    @staticmethod
    def create_access_token(user_id: str, email: str) -> str:
        """
        Create a JWT access token for a user.

        Args:
            user_id: User's external ID (UUID string)
            email: User's email address

        Returns:
            JWT token as string
        """
        # Calculate expiration time
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)

        # Create token payload with standard JWT claims
        payload = {
            "sub": user_id,  # Subject claim - user identifier
            "email": email,
            "exp": expire,  # Expiration time
            "iat": datetime.utcnow(),  # Issued at time
        }

        # Encode the token using the secret key
        token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
        return token

    @staticmethod
    def get_user_by_email(session: Session, email: str) -> Optional[User]:
        """
        Retrieve a user by email address.

        Args:
            session: Database session
            email: User's email address

        Returns:
            User object if found, None otherwise
        """
        statement = select(User).where(User.email == email)
        return session.exec(statement).first()

    @staticmethod
    def get_user_by_id(session: Session, user_id: int) -> Optional[User]:
        """
        Retrieve a user by internal ID.

        Args:
            session: Database session
            user_id: User's internal ID

        Returns:
            User object if found, None otherwise
        """
        return session.get(User, user_id)

    @staticmethod
    def get_user_by_external_id(session: Session, external_id: str) -> Optional[User]:
        """
        Retrieve a user by external UUID.

        Args:
            session: Database session
            external_id: User's external UUID

        Returns:
            User object if found, None otherwise
        """
        statement = select(User).where(User.external_id == external_id)
        return session.exec(statement).first()

    @staticmethod
    def create_user(session: Session, user_data: UserCreate) -> User:
        """
        Create a new user with hashed password.

        Args:
            session: Database session
            user_data: User creation data with email and plain password

        Returns:
            Created User object
        """
        # Hash the password before storing
        hashed_password = AuthService.hash_password(user_data.password)

        # Create user with hashed password
        user = User(
            email=user_data.email,
            hashed_password=hashed_password
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        return user

    @staticmethod
    def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user by email and password.

        Args:
            session: Database session
            email: User's email address
            password: Plain text password to verify

        Returns:
            User object if authentication successful, None otherwise
        """
        # Get user by email
        user = AuthService.get_user_by_email(session, email)

        if not user:
            return None

        # Verify password
        if not AuthService.verify_password(password, user.hashed_password):
            return None

        return user
