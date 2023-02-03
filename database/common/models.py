from datetime import datetime

from peewee import *

# Set Database
db = SqliteDatabase('test_base.db')


# Модели это таблицы в базе данных
# Атрибуты и свойства класса это столбцы
# Экземпляр(объект) класса это записи

class BaseModel(Model):
    id = PrimaryKeyField(unique=True)
    created_at = DateField(default=datetime.now())
    tg_id = IntegerField(unique=True, null=False)

    class Meta:
        database = db
        order_by = 'id'


class History(BaseModel):
    number = TextField()
    message = TextField()

    class Meta:
        db_table = 'histories'


class User(BaseModel):
    name = CharField(null=True)
    age = IntegerField(null=True)
    country = CharField(null=True)
    city = CharField(null=True)
    phone_number = CharField(null=True)

    class Meta:
        db_table = 'users'


class Setting(BaseModel):
    tg_id = IntegerField(unique=True, null=False)
    lang = CharField(max_length=2, null=True)
    cur = CharField(max_length=3, null=True)

    class Meta:
        db_table = 'settings'


if __name__ == '__main__':
    db.create_tables([User, History, Setting])
