from .base import BaseModel
from .user import User
from peewee import ForeignKeyField, UUIDField, DateField


class RefreshToken(BaseModel):
    token = UUIDField()
    user = ForeignKeyField(model=User, backref="tokens")
    expires_at = DateField
    created_at = DateField
