from fastapi import APIRouter, HTTPException
import bcrypt
from schemas.user import UserRegister, UserLogin
from schemas.auth import Token
from models import User, RefreshToken
from utils.security import create_JWT_token, create_refresh_token

router = APIRouter()


@router.post("/register")
def register_user(user_data: UserRegister) -> dict:
    """Register new user with validation and secure password hashing."""

    # Check email uniqueness
    if User.get_or_none(User.email == user_data.email):
        raise HTTPException(
            status_code=409, detail="Esse endereço de e-mail já está sendo utilizado."
        )

    # Check username uniqueness
    if User.get_or_none(User.username == user_data.username):
        raise HTTPException(
            status_code=409, detail="Esse nome de usuário já está sendo utilizado."
        )

    # Hash password with bcrypt
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(user_data.password.encode("utf-8"), salt).decode(
        "utf-8"
    )

    # Create user in database
    User.create(
        username=user_data.username,
        email=user_data.email,
        password_hash=password_hash,
    )

    return {"message": "Usuário criado com sucesso!"}


@router.post("/login", response_model=Token)
def login_user(user_data: UserLogin) -> Token:
    """Login user with validated credentials and return session tokens."""

    # Check user email (or username) in database
    user = User.get_or_none(
        (User.username == user_data.email_or_username)
        | (User.email == user_data.email_or_username)
    )

    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas.")

    # Verify request password
    if not bcrypt.checkpw(
        user_data.password.encode("utf-8"),
        user.password_hash.encode("utf-8"),
    ):
        raise HTTPException(status_code=401, detail="Credenciais inválidas.")

    token_data = {"id": str(user.id), "email": user.email}

    # Create JWT token
    JWT_token = create_JWT_token(data=token_data)

    # Create Refresh token
    refresh_token = create_refresh_token(user.id)

    return Token(
        access_token=JWT_token, refresh_token=refresh_token, token_type="bearer"
    )
