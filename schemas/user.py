from pydantic import BaseModel, EmailStr, field_validator


class UserRegister(BaseModel):
    """User registration schema with validation"""

    username: str
    email: EmailStr
    password: str

    @field_validator("password")
    def validate_password(cls, v):
        """Validate password: min 8 chars 1 number 1 uppercase"""
        if len(v) < 8:
            raise ValueError("Senha deve ter no mínimo 8 caracteres")

        if not any(char.isdigit() for char in v):
            raise ValueError("Senha deve conter pelo menos 1 número")

        if not any(char.isupper() for char in v):
            raise ValueError("Senha deve conter pelo menos 1 letra maiúscula")

        return v


class UserLogin(BaseModel):
    """User Login schema with validation"""

    email_or_username: str
    password: str
