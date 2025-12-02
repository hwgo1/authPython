import datetime
import uuid
from peewee import UUIDField, CharField, DateField
from .base import BaseModel


class User(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    username = CharField(unique=True, max_length=100)
    email = CharField(unique=True, max_length=255)
    password_hash = CharField(max_length=255)
    created_at = DateField(default=datetime.datetime.now)
