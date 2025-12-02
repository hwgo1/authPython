from models import db, User

db.connect()

db.create_tables([User])

print("✅ Table created!")

db.close()
