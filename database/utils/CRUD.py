from typing import Dict, List, TypeVar
from peewee import ModelSelect
from database.common.models import BaseModel
from ..common.models import db

T = TypeVar('T')


def _store_date(db: db, model: T, *data: List[Dict]) -> None:
    """Функция записи в базу"""
    with db.atomic():
        model.insert_many(*data).execute()


def _retrieve_all_data(db: db, model: T, *columns: BaseModel) -> ModelSelect:
    """Функция чтения из базы"""
    with db.atomic():
        response = model.select(*columns)

    return response


def _update_all_data(db: db, model: T, *data: List[Dict]) -> ModelSelect:
    """Функция обновления записей"""
    with db.atomic():
        response = model.update(*data).execute()

    return response


# Проверка на наличие записи id пользователя в базе
def _db_check_tg_id(db: db, model: T, tg_id: str):
    """Функция проверки на наличие записи id пользователя в базе"""
    with db.atomic():
        response = model.select().where(model.tg_id == tg_id)

    return response


class CRUDInterface():
    @staticmethod
    def write():
        return _store_date

    @staticmethod
    def read():
        return _retrieve_all_data

    @staticmethod
    def update():
        return _update_all_data

    @staticmethod
    def check_id():
        return _db_check_tg_id


if __name__ == '__main__':
    _store_date()
    _retrieve_all_data()
    _update_all_data()
    _db_check_tg_id()

    CRUDInterface()
