"""
Чтобы запустить приложение, наберите: gunicorn -b 127.0.0.1:8000 app_student:app
"""

from pprint import pprint

from lightweb4py.framework import Framework
from lightweb4py.views import BaseViewLayout, BaseViewSection
from lightweb4py.logger import LoggerFabric, Log, LoggerLevel
from lightweb4py.persistence_sqlite import PersistenceSQLite
from lightweb4py.settings import Environ

from urls import app_urls
from logs import loggers, handlers
from category import Category
from course import Course
from student import Student
from feedback import Feedback

import settings

# Прочие константы
EMAIL_ADMIN = "nekidoz@yandex.ru"

logger = LoggerFabric(handlers=handlers, loggers=loggers, default_logger=settings.LOGGER_DEBUG)
log_d = Log(settings.LOGGER_DEBUG, LoggerLevel.DEBUG, 'app')
log_r = Log(settings.LOGGER_RUNTIME, LoggerLevel.INFO, 'app')
log_d("Test debug message")
log_r("Test runtime message")
PersistenceSQLite.register()
app = Framework(app_urls, use_admin=True)           # Create application object
env = Environ(settings.PATH_JINJA_TEMPLATES)        # Create environment object
# Initialize persistence data
if not (Category.register() and Course.register() and Student.register() and Feedback.register()):
    print("Failed to init data sources")
layout = BaseViewLayout()                                   # Initialize the Base view
if layout.status_code != 200:
    print("BaseView layout error: {}: template {} not found".format(layout.status_code, layout.status_message))
layout.render_html_include(BaseViewSection.left_sidebar, settings.TEMPLATES_APP+"/left_sidebar.html",
                           clear_template=True, urls=app.get_clean_urls(for_menu_only=True))
