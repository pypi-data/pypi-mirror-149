import uuid
from datetime import datetime
from dataclasses import dataclass

from lightweb4py.persistence_sqlite import PersistenceSQLite, ENGINE_SQLITE
from lightweb4py.persistence import Persistence, PersistenceSerializable, ENGINE_JSON


# Класс студента наследует PersistenceSerializable для надлежащей обработки библиотекой Persistence
@dataclass
class Personnel(PersistenceSerializable):
    id: uuid.UUID
    name: str
    birth_date: datetime
    course_id: uuid.UUID

    @staticmethod  # Зарегистрировать класс в библиотеке Persistence
    def register() -> bool:
        return Persistence.register_class(Personnel, ENGINE_JSON, 'personnel.json')


PersistenceSQLite.register()  # Зарегистрировать хранилище данных SQLite в библиотеке Persistence
if not Personnel.register():
    print("Не удалось зарегистрировать класс Personnel в базе данных")
else:
    # Создать объект сотрудника
    person = Personnel(id=uuid.uuid4(), name="Мовлатшо Довлатшоевич", birth_date=datetime.now(), course_id=None)
    Persistence.engine(Personnel).set(person)       # Сохранить его
    print(Persistence.engine(Personnel).get())      # Напечатать весь список персонала
