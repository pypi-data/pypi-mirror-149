from datetime import datetime
import uuid

from lightweb4py.framework import url
from lightweb4py.persistence import Persistence, PersistenceSerializable
from lightweb4py.views import View, MinimalView, BaseView
from lightweb4py.response import Response
from lightweb4py.request import Request

import settings


class Feedback(PersistenceSerializable):
    id: uuid.UUID
    date: datetime
    name: str
    email: str
    title: str
    msg: str

    def __init__(self, id: uuid.UUID = None, date: datetime = None,
                 name: str = None, email: str = None, title: str = None, msg: str = None):
        self.id = id if id else uuid.uuid4()
        self.date = date if date else datetime.now()
        self.name = name
        self.email = email
        self.title = title
        self.msg = msg

    # Register Course's Persistence storage
    @staticmethod
    def register() -> bool:
        return Persistence.register_class(Feedback, settings.FEEDBACK_STORAGE, settings.FEEDBACK_DATA_FILE)


# Page Controller для формы обратной связи
# Состав:
# - файл contact.html шаблона формы обратной связи в папке page controller'ов
# - файл contact_success.html шаблона сообщения об успехе формы обратной связи в папке page controller'ов
# Метод GET отображает форму.
# Метод POST записывает данные формы в базу Persistence.
#@debug(logger='runtime', level=LoggerLevel.INFO)
#@url('/kakaka', name="Обратная связь через декоратор", in_menu=True)
class FeedbackView(View):

    HTML_TEMPLATE_FORM = settings.TEMPLATES_APP + "/contact.html"             # Шаблон формы обратной связи
    HTML_TEMPLATE_SUCCESS = settings.TEMPLATES_APP + "/contact_success.html"  # Шаблон страницы успеха
    QPARAM_NAME = "name"                                                # Параметры POST с полями сообщения
    QPARAM_EMAIL = "email"
    QPARAM_TITLE = "title"
    QPARAM_MESSAGE = "msg"

    #@debug(logger='runtime', level=LoggerLevel.INFO)
    def run(self, request: Request, *args, **kwargs) -> Response:
        if request.method == "GET":             # GET: отобразить форму обратной связи
            return BaseView(self.HTML_TEMPLATE_FORM, *args, **kwargs).run(request)

        elif request.method == "POST":          # POST: обработать данные формы обратной связи
            # Сформировать сообщение для отображения пользователю
            message_html = "Имя: {}<br>Email: {}<br>Заголовок: {}<br>Сообщение: {}"\
                .format(request.query_params.get(self.QPARAM_NAME),
                        request.query_params.get(self.QPARAM_EMAIL),
                        request.query_params.get(self.QPARAM_TITLE),
                        request.query_params.get(self.QPARAM_MESSAGE).replace("\n", "<br>"))
            # Сохранить объект сообщения в Persistence
            Persistence.engine(Feedback).append(Feedback(**request.query_params))
            # Отобразить страницу успеха
            return BaseView(self.HTML_TEMPLATE_SUCCESS, message=message_html, *args, **kwargs).run(request)

        else:                                                   # Неизвестный метод - ошибка
            return MinimalView(status_code=418, body="Неизвестный метод HTTP: {}".format(request.method)).run(request)


class FeedbackListView(View):
    HTML_TEMPLATE_FORM = settings.TEMPLATES_APP + "/feedback.html"             # Шаблон списка отзывов

    def run(self, request: Request, *args, **kwargs) -> Response:
        if request.method == "GET":
            # GET: отобразить форму списка отзывов, самый новый отзыв - сверху
            feedback = sorted(Persistence.engine(Feedback).get(), key=lambda item: item.date, reverse=True)
            return BaseView(self.HTML_TEMPLATE_FORM, feedback=feedback, *args, **kwargs).run(request)

