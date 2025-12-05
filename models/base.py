from peewee import SqliteDatabase, Model

db = SqliteDatabase("auth.db", pragmas={"foreign_keys": 1})


class BaseModel(Model):
    class Meta:
        database = db
