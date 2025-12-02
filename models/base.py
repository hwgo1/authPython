from peewee import SqliteDatabase, Model

db = SqliteDatabase("auth.db")


class BaseModel(Model):
    class Meta:
        database = db
