# MICROSERVICE DEMO APP
"""
Чтобы запустить приложение, наберите: gunicorn -b 127.0.0.1:8001 app_student:app
"""
# Implements the old version of contact message storage - to file
# Also sends the same contact message to the main app, which is supposed to store it elsewhere
import os
from datetime import datetime
import requests

from lightweb4py.framework import Framework, url
from lightweb4py.views import View, MinimalView, BaseView, BaseViewLayout
from lightweb4py.request import Request
from lightweb4py.response import Response
from lightweb4py.settings import Environ

URL_FEEDBACK = 'http://127.0.0.1:8000/contact'
import settings

# Page Controller для формы обратной связи
# Состав:
# - файл contact.html шаблона формы обратной связи в папке page controller'ов
# - файл contact_success.html шаблона сообщения об успехе формы обратной связи в папке page controller'ов
# - папка contact_messages/ для файлов сообщений в папке page controller'ов с правами записи в нее,
#   или права на создание такой папки в папке page controller'ов
# Метод GET отображает форму.
# Метод POST записывает данные формы в папку сообщений в файл с именем в формате YYYY-MM-DDTHH-MM-SS_email.
@url('/')
class Contact(View):

    HTML_TEMPLATE_FORM = settings.TEMPLATES_APP + "/contact.html"             # Шаблон формы обратной связи
    HTML_TEMPLATE_SUCCESS = settings.TEMPLATES_APP + "/contact_success.html"  # Шаблон страницы успеха
    QPARAM_NAME = "name"                                                # Параметры POST с полями сообщения
    QPARAM_EMAIL = "email"
    QPARAM_TITLE = "title"
    QPARAM_MESSAGE = "msg"

    def run(self, request: Request, *args, **kwargs) -> Response:
        if request.method == "GET":             # GET: отобразить форму обратной связи
            return BaseView(self.HTML_TEMPLATE_FORM, *args, **kwargs).run(request)

        elif request.method == "POST":          # POST: обработать данные формы обратной связи
                                            # Сформировать строку сообщения
            message = "Имя: {}\nEmail: {}\nЗаголовок: {}\nСообщение: {}"\
                .format(request.query_params.get(self.QPARAM_NAME),
                        request.query_params.get(self.QPARAM_EMAIL),
                        request.query_params.get(self.QPARAM_TITLE),
                        request.query_params.get(self.QPARAM_MESSAGE))
            message_html = message.replace("\n", "<br>")

            try:                            # Создать папку сообщений
                os.mkdir(settings.PATH_CONTACT_MESSAGES)
            except FileExistsError:         # Если уже существует, ОК
                pass

            try:                            # Записать сообщение в файл с именем в формате YYYY-MM-DDTHH-MM-SS_email
                with open(settings.PATH_CONTACT_MESSAGES +
                          datetime.now().strftime("%Y-%m-%dT%H-%M-%S") + "_" +
                          request.query_params.get(self.QPARAM_EMAIL), 'w') as output_file:
                    output_file.write(message)
            except FileNotFoundError:
                return MinimalView(status_code=404,
                                   body="Папка сообщений не найдена - возможно, отсутствуют права доступа.")\
                    .run(request)

            # MICROSERVICE: call the main app URL to store the message in the database
            requests.post(URL_FEEDBACK, data=request.query_params)
                                            # Отобразить страницу успеха
            return BaseView(self.HTML_TEMPLATE_SUCCESS, message=message_html, *args, **kwargs).run(request)

        else:                                                   # Неизвестный метод - ошибка
            return MinimalView(status_code=418, body="Неизвестный метод HTTP: {}".format(request.method)).run(request)


app = Framework([], use_admin=False)                # Create application object
env = Environ(settings.PATH_JINJA_TEMPLATES)        # Create environment object
layout = BaseViewLayout()                                   # Initialize the Base view
