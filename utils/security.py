import jwt
import os
from jwt.exceptions import InvalidTokenError
from dotenv import load_dotenv
from datetime import timedelta, datetime, timezone
from uuid import uuid4
from models import RefreshToken

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))


def create_JWT_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Create JWT access token with user data and expiration.

    Args:
        data: Dictionary with user info (user_id, email)
        expires_delta: Optional custom expiration time

    """

    to_encode = data.copy()

    # Define token expiration time
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    # Add expiration claim to payload
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_JWT_token(token: str) -> dict:
    """
    Decode and verify JWT token.

    Args:
        token: JWT token string

    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except InvalidTokenError:
        raise


def create_refresh_token(user_id) -> str:
    """
    Generate and store a refresh token for the authenticated user.

    Args:
        user_id: ID of the user for whom the token is created
    """
    token = str(uuid4())
    expires = datetime.now(timezone.utc) + timedelta(days=7)
    RefreshToken.create(token=token, user_id=user_id, expires_at=expires)
    return token
