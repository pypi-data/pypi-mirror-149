from lightweb4py.logger import LoggerFabric, LoggerLevel, Log, debug

# ********** Данный раздел в реальном проекте рекомендуется вынести в отдельный файл logs.py *********
handlers = {
    'console': {
        'handler': 'LoggerConsoleHandler',
        'name': 'console',
        'level': 0,
        'default_level': 0,
        'is_on': True,
    },
    'debug_file': {
        'handler': 'LoggerFileHandler',
        'name': 'debug_file',
        'file_name': 'debug.log',
        'level': 0,
        'default_level': 0,
        'is_on': True,
    },
    'app_file': {
        'handler': 'LoggerFileHandler',
        'name': 'app_file',
        'file_name': 'app.log',
        'level': 0,
        'default_level': 0,
        'is_on': True,
    },
}

loggers = {
    'debug': {
        'logger': 'Logger',
        'name': 'debug',
        'handlers': ['console', 'debug_file'],
        'level': 0,
        'default_level': 0,
        'is_on': True,
    },
    'runtime': {
        'logger': 'Logger',
        'name': 'runtime',
        'handlers': ['console', 'app_file'],
        'level': 0,
        'default_level': 0,
        'is_on': True,
    },
}
# ********** Конец раздела файла logs.py **************************************************************


@debug
class Test:
    def __init__(self):
        print("Инициализация класса")

    def __call__(self, *args, **kwargs):
        print("Вызов объекта класса")

    @debug(logger='runtime', level=LoggerLevel.INFO, message_before="Вызов метода", message_after="Метод отработал")
    def do_something(self):
        print("Вызов метода объекта")

# Инициализируем библиотеку
logger = LoggerFabric(turn_on=True,
                      handlers=handlers, loggers=loggers,
                      default_logger="debug", default_level=LoggerLevel.DEBUG)
# Создаем два объекта лога и пишем в них сообщения
log_d = Log('debug', LoggerLevel.DEBUG, 'app')
log_r = Log('runtime', LoggerLevel.INFO, 'app')
log_d("Test debug message")
log_r("Test runtime message")

test = Test()               # Создаем объект декорированного класса Test
test()                      # Неявно вызываем метод __call__()
test.do_something()         # Явно вызываем декорированный метод
