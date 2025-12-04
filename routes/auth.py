from fastapi import APIRouter, HTTPException
import bcrypt
from schemas.user import UserRegister
from models import User

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
