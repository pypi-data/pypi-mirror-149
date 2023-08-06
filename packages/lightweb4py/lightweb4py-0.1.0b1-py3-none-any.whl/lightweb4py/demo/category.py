import uuid

from lightweb4py.persistence import Persistence, PersistenceSerializable
from lightweb4py.request import Request
from lightweb4py.response import Response

from element_edit import ElementEditView
import settings


class Category(PersistenceSerializable):
    id: uuid.UUID
    name: str

    def __init__(self, id: uuid.UUID = None, name: str = None):
        self.id = id if id else uuid.uuid4()
        self.name = name

    # Register Category's Persistence storage
    @staticmethod
    def register() -> bool:
        return Persistence.register_class(Category, settings.CATEGORIES_STORAGE, settings.CATEGORIES_DATA_FILE)
