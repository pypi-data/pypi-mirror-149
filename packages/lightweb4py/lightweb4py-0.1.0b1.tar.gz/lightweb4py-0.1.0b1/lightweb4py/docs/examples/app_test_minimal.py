from lightweb4py.urls import Url
from lightweb4py.framework import Framework
from lightweb4py.views import MinimalView

# !ВАЖНО! Рекомендуется список app_urls выносить в файл приложения urls.py и импортировать его в основное приложение
app_urls = [
    Url('/', MinimalView,
        {'body': 'Это главная страница приложения.<br>' + \
                 '<a href="/about">О компании</a><br>' + \
                 '<a href="/sales">Продажи</a><br>' + \
                 '<a href="/service">Обслуживание</a><br>' + \
                 '<a href="/contact">Контакты</a>',
         'status_code': '200 OK'
         }, "Главная страница", True),
    Url('/about', MinimalView,
        {'body': 'Это страница информации о компании.<br>' + \
                 '<a href="/">Домой</a>',
         'status_code': '200 OK'
         }, "О компании", True),
    Url('/sales', MinimalView,
        {'body': 'Это страница подразделения продаж.<br>' + \
                 '<a href="/">Домой</a>',
         'status_code': '200 OK'
         }, "Продажи", True),
    Url('/service', MinimalView,
        {'body': 'Это страница подразделения обслуживания.<br>' + \
                 '<a href="/">Домой</a>',
         'status_code': '200 OK'
         }, "Обслуживание", True),
    Url('/contact', MinimalView,
        {'body': 'Это страница Контактов.<br>' + \
                 '<a href="/">Домой</a>',
         'status_code': '200 OK'
         }, "Контакты", True),
]

app = Framework(app_urls, use_admin=False)  # Create application object
