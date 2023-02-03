from database.utils.CRUD import CRUDInterface
from database.common.models import db, User, History, Setting

db.connect()
db.create_tables([User, History, Setting])

crud = CRUDInterface()

if __name__ == "main":
    crud()
