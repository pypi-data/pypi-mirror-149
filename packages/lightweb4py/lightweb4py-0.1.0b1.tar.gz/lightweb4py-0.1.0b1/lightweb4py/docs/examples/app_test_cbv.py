from lightweb4py.framework import Framework, url
from lightweb4py.urls import Url
from lightweb4py.views import View, SimpleView
from lightweb4py.request import Request
from lightweb4py.response import Response
from lightweb4py.settings import Environ


class MainView(View):

    def __init__(self, *args, template_name: str, **kwargs):
        self.template_name = template_name

    def run(self, request: Request, *args, **kwargs) -> Response:
        return SimpleView(template_name=self.template_name).run(request)


@url('/contact', name="Обратная связь", in_menu=True)
class ContactView(View):
    TEMPLATE_NAME = "app/contact.html"

    def run(self, request: Request, *args, **kwargs) -> Response:
        return SimpleView(template_name=self.TEMPLATE_NAME).run(request)


# !ВАЖНО! Рекомендуется список app_urls выносить в файл приложения urls.py и импортировать его в основное приложение
app_urls = [
    Url('/', MainView, {'template_name': 'app/index.html'}, "Главная страница", True),
]

app = Framework(app_urls, use_admin=True)           # Create application object
env = Environ('templates')                          # Create environment object
