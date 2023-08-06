import uuid

from lightweb4py.persistence import Persistence, PersistenceSerializable
from lightweb4py.request import Request
from lightweb4py.response import Response

from miscellaneous import build_choice_list
from element_edit import ElementEditView
from category import Category
import settings


class Course(PersistenceSerializable):
    id: uuid.UUID
    name: str
    category_id: uuid.UUID

    def __init__(self, id: uuid.UUID = None, name: str = None, category_id: uuid.UUID = None):
        self.id = id if id else uuid.uuid4()
        self.name = name
        self.category_id = category_id

    # Register Course's Persistence storage
    @staticmethod
    def register() -> bool:
        return Persistence.register_class(Course, settings.COURSES_STORAGE, settings.COURSES_DATA_FILE)


class CourseEditView(ElementEditView):

    # Override run(): load the existing course categories and
    # build a category list, adding an empty category and placing the course's category at the top of the list
    def run(self, request: Request, *args, **kwargs) -> Response:

        # Rebuild the category list, adding an empty category and placing the course's category at the top of the list
        if request.method == "GET":                         # only processing GET
            # Get the categories list - needed anyway by the form
            categories = build_choice_list(Category, Course, request.path_array[len(request.path_array) - 1],
                                           'category_id')

            return super().run(request, categories=categories, *args, **kwargs)
        else:
            return super().run(request, *args, **kwargs)
