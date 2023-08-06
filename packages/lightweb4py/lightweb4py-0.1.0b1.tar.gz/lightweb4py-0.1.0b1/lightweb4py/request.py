# REFERENCE STRUCTURE
from urllib.parse import unquote
#from urllib.parse import parse_qs      # парсит query string

from lightweb4py import settings

# Ключи и константы для парсинга параметров запроса
ENV_PATH_KEY = "PATH_INFO"          # Ключ словаря параметра с полным путем текущей страницы
ENV_PATH_SEP = "/"                  # Разделитель URL (напр. /about/company)
ENV_QUERY_KEY = "QUERY_STRING"      # Ключ словаря параметра со строкой запроса
ENV_QUERY_SEP = "&"                 # Разделитель параметров запроса (напр. a=2&c=3)
ENV_QUERY_KV_SEP = "="              # Разделитель ключей и значений в параметрах запроса (напр. a=2)
ENV_REQ_METHOD = "REQUEST_METHOD"   # Ключ словаря с методом запроса
ENV_REQ_GET = "GET"                 # Значение параметра для запроса GET
ENV_REQ_POST = "POST"               # Значение параметра для запроса POST
ENV_CONTENT_LEN_KEY = "CONTENT_LENGTH"  # Ключ параметра с длиной контента для запроса POST
ENV_WSGI_INPUT_KEY = "wsgi.input"   # Ключ параметра со входными данными WSGI для запроса POST
ENV_HTTP_PREFIX = "HTTP_"           # Префикс параметров HTTP запроса


# environ - application call environment passed by WSGI server
# path_array - array of path tokens
# path - path without trailing slash; '/' for root
# method - http request method ('GET', 'POST', ...)
# query_params - dictionary of query parameters for GET or POST method
# headers - HTTP headers
class Request:

    def __init__(self, environ: dict):
        self.environ = environ                              # Save environment first - needed by protected functions

        # Получить массив токенов пути страницы и словарь с параметрами запроса
        self.path_array = self._parse_page_path()           # Получить массив токенов пути для страницы
        # Page path without trailing slash; '/' for root
        self.path = "/".join(self.path_array) if len(self.path_array) > 1 else "/"
        self.method = environ[ENV_REQ_METHOD]           # Request method

        if self.method == ENV_REQ_GET:
            query_str = environ[ENV_QUERY_KEY]          # Строка запроса уже содержится в словаре метода GET
        elif self.method == ENV_REQ_POST:
            query_str = self._fetch_post_query_parameters() # Получить строку запроса из тела метода POST
        else:
            query_str = ""                                  # Неизвестный метод - и строки запроса нет
        #self.query_params = parse_qs(query_str)            # already created own parser
        self.query_params = self._parse_query_params(query_str)    # Получить массив параметров запроса GET/POST
        self.headers = self._get_http_headers()

    # Делит путь path на токены и удаляет последний токен, если он пустой (т.е. если URL кончается на /)
    # Возвращает массив токенов пути
    def _parse_page_path(self) -> [str]:
        path_array = self.environ[ENV_PATH_KEY].split(ENV_PATH_SEP)
        if path_array[len(path_array) - 1].strip() == '':
            del path_array[len(path_array) - 1]
        return path_array

    # Возвращает строку запроса из тела запроса POST
    def _fetch_post_query_parameters(self) -> str:
        content_length_data = self.environ.get(ENV_CONTENT_LEN_KEY)  # Получаем длину тела
        # Приводим к int
        content_length = int(content_length_data) if content_length_data else 0
        content = self.environ[ENV_WSGI_INPUT_KEY].read(content_length) if content_length > 0 else b''
        query_str = content.decode(encoding=settings.HTML_ENCODING) if content else ""
        return query_str

    # Делит строку запроса на отдельные параметры
    # Возвращает словарь параметров
    def _parse_query_params(self, query: str) -> dict:
        param_dict = {}
        if query:
            # Перед раскодированием избавимся от знаков '+', которыми заменены пробелы
            query = query.replace('+', ' ')
            params = query.split(ENV_QUERY_SEP)  # Получение списка параметров запроса
            for param in params:
                key, value = param.split(ENV_QUERY_KV_SEP)  # Получение ключа и значения для каждого параметра
                param_dict[key] = unquote(value)
        return param_dict

    # Get HTTP headers
    def _get_http_headers(self):
        headers = {}
        for key, value in self.environ.items():
            if key.startswith(ENV_HTTP_PREFIX):
                headers[key[len(ENV_HTTP_PREFIX):]] = value
        return headers
