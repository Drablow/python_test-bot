from typing import Dict, List, TypeVar

from peewee import ModelSelect

from database.common.models import BaseModel
from ..common.models import db

T = TypeVar('T')


# write in base
def _store_date(db: db, model: T, *data: List[Dict]) -> None:
    with db.atomic():
        model.insert_many(*data).execute()


# read on base
def _retrieve_all_data(db: db, model: T, *columns: BaseModel) -> ModelSelect:
    with db.atomic():
        response = model.select(*columns)

    return response


def _update_all_data(db: db, model: T, *colums: BaseModel) -> ModelSelect:
    with db.atomic():
        response = model.update(*colums)

    return response


class CRUDInterface():
    @staticmethod
    def create():
        return _store_date

    @staticmethod
    def retrieve():
        return _retrieve_all_data

    @staticmethod
    def update():
        return _update_all_data


if __name__ == '__main__':
    _store_date()
    _retrieve_all_data()
    CRUDInterface()
