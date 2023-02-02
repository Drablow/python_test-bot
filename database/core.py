from database.utils.CRUD import CRUDInterface
from database.common.models import db, User, History

db.connect()
db.create_tables([User, History])

crud = CRUDInterface()

if __name__ == "main":
    crud()
