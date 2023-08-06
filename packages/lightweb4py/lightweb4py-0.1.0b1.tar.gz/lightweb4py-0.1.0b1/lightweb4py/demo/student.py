import uuid

from lightweb4py.persistence import Persistence, PersistenceSerializable
from lightweb4py.request import Request
from lightweb4py.response import Response

from miscellaneous import build_choice_list
from element_edit import ElementEditView
from course import Course
import settings


class Student(PersistenceSerializable):
    id: uuid.UUID
    first_name: str
    middle_name: str
    last_name: str
    course_id: uuid.UUID

    def __init__(self, id: uuid.UUID = None,
                 first_name: str = None, middle_name: str = None, last_name: str = None,
                 course_id: uuid.UUID = None):
        self.id = id if id else uuid.uuid4()
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.course_id = course_id

    # Register Student's Persistence storage
    @staticmethod
    def register() -> bool:
        return Persistence.register_class(Student, settings.STUDENTS_STORAGE, settings.STUDENTS_DATA_FILE)


class StudentEditView(ElementEditView):

    # Override run(): load the existing courses and
    # build a course list, adding an empty course and placing the student's course at the top of the list
    def run(self, request: Request, *args, **kwargs) -> Response:

        # Rebuild the category list, adding an empty category and placing the course's category at the top of the list
        if request.method == "GET":                         # only processing GET
            # student id is the last element in the wsgi request path array
            courses = build_choice_list(Course, Student, request.path_array[len(request.path_array) - 1], 'course_id')
            return super().run(request, courses=courses, *args, **kwargs)
        else:
            return super().run(request, *args, **kwargs)
