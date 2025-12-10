from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import os
from jwt.exceptions import InvalidTokenError
from dotenv import load_dotenv
from datetime import timedelta, datetime, timezone
from uuid import uuid4
from models import RefreshToken, User

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))


security = HTTPBearer()


def create_JWT_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create JWT access token with user data and expiration."""
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
    """Decode and verify JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except InvalidTokenError:
        raise


def create_refresh_token(user_id) -> str:
    """Generate and store a refresh token for the authenticated user."""
    token = str(uuid4())
    expires = datetime.now(timezone.utc) + timedelta(days=7)
    RefreshToken.create(token=token, user_id=user_id, expires_at=expires)
    return token


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependency to get current authenticated user from JWT token.

    Args:
        credentials: Bearer token credentials from Authorization header

    """

    token_str = credentials.credentials

    try:
        decoded_token = decode_JWT_token(token_str)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
    except Exception:
        raise HTTPException(status_code=401, detail="Erro ao validar token")

    # Extract user_id from payload
    user_id = decoded_token.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token não contém ID de usuário")

    # Search for user in database
    current_user = User.get_or_none(User.id == user_id)
    if not current_user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    return current_user
