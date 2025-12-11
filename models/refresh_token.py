import datetime
from .base import BaseModel
from .user import User
from peewee import ForeignKeyField, CharField, DateTimeField


class RefreshToken(BaseModel):
    """Refresh token storage for user authentication"""

    token = CharField(unique=True, max_length=36)
    user = ForeignKeyField(model=User, backref="tokens")
    expires_at = DateTimeField()
    created_at = DateTimeField(default=datetime.datetime.now)
