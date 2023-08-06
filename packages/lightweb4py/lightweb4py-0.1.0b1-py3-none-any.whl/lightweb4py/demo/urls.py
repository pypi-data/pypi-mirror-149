# REFERENCE STRUCTURE
from lightweb4py.urls import Url

from views import Index
from feedback import FeedbackView, FeedbackListView
from element_edit import ElementEditView
from category import Category
from course import Course, CourseEditView
from student import Student, StudentEditView


import settings

app_urls = [
    Url('/', Index, {}, "Главная страница", True),
    Url('/category/edit/*', ElementEditView,
        {'element_class': Category,
         'element_html_class_name': "Category",
         'element_title': "Категория учебного курса",
         'html_template_form': settings.TEMPLATES_APP + "/element_edit.html",
         'editor_field_template_names': (settings.TEMPLATES_APP + "/element_edit_name_field.html",
                                        ),
         },
        "Категории курсов", False),
    Url('/course/edit/*', CourseEditView,
        {'element_class': Course,
         'element_html_class_name': "Course",
         'element_title': "Учебный курс",
         'html_template_form': settings.TEMPLATES_APP + "/element_edit.html",
         'editor_field_template_names': (settings.TEMPLATES_APP + "/element_edit_name_field.html",
                                         settings.TEMPLATES_APP + "/element_edit_category_field.html", ),
         },
        "Курсы", False),
    Url('/student/edit/*', StudentEditView,
        {'element_class': Student,
         'element_html_class_name': "Student",
         'element_title': "Студент",
         'html_template_form': settings.TEMPLATES_APP + "/element_edit.html",
         'editor_field_template_names': (settings.TEMPLATES_APP + "/element_edit_person_fields.html",
                                         settings.TEMPLATES_APP + "/element_edit_course_field.html", ),
         },
        "Курсы", False),
    Url('/contact', FeedbackView, {}, "Обратная связь", True),
    Url('/feedback', FeedbackListView, {}, "Блог", True)
]
