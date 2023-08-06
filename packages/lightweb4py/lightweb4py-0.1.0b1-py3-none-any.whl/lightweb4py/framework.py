# This is the main framework class
from pprint import pprint
from copy import deepcopy
from functools import wraps

from lightweb4py.request import Request
from lightweb4py.response import Response
from lightweb4py import settings
from lightweb4py.urls import admin_urls, Url
from lightweb4py.singleton import Singleton
from lightweb4py.logger import debug, Log
from lightweb4py.views import View404


# ATTRIBUTES:
# urls - project URL array (initialized at init()
# request - parsed WSGI request (initialized at call()
# PARAMETERS:
# urls - array of user app urls for routing
# use_admin - whether to use admin; if true, its urls from urls.py are appended to user urls
# PROPERTIES:
# get_clean_urls - clean user app urls for navigation (without wildcards)
#
# router processes full URL paths and wildcard (e.g. /someurl/*) URLs (see urls.py for example)
class Framework(Singleton):

    # Initialize app and admin urls
    def __init__(self, urls: [Url] = None, use_admin: bool = False):
        if not hasattr(self, 'urls'):           # Initialize attribute if it doesn't exist
            self.urls = []
        if urls:                                # Refresh urls if any passed
            for url in urls:
                self.set_url(url, replace=True)
        if use_admin:                           # Add admin URLs if requested and if paths not occupied
            for url in admin_urls:
                self.set_url(url, replace=False)

    # PARAMETERS:
    # environ: словарь данных от сервера
    # start_response: функция для ответа серверу
    def __call__(self, environ: dict, start_response, *args, **kwargs):
        self.request = Request(environ)         # Should be done first - protected functions use it
        view = self._get_view()
        if view:
            response = view.run(self.request)
            if not response:
                # Had to somehow untie framework and views files circular reference - invented redirect ))
                #response = Response(status_code=settings.STATUS_NOT_FOUND,
                #                    headers={'Location': settings.URL_NOT_FOUND + f"?page={self.request.path}"})
                response = View404().run(self.request)
        else:
            #response = Response(status_code=settings.STATUS_NOT_FOUND,
            #                    headers={'Location': settings.URL_NOT_FOUND + f"?page={self.request.path}"})
            response = View404().run(self.request)

        # сначала в функцию start_response передаем код ответа и заголовки
        start_response(str(response.status_code), response.headers.items())
        # возвращаем тело ответа в виде списка байтов
        return [response.body.encode(settings.HTML_ENCODING)]

    # Process full URL paths and wildcard (e.g. /someurl/*) URL processing
    def _get_view(self):
        target_url = None
        for url in self.urls:

            # wildcard URL processing
            if len(url.url) >= 2 and url.url[-2:] == "/*":
                # Check for cases like /someurl and /someurl/someotherurl
                if (len(self.request.path) == len(url.url) - 2) or \
                        (len(self.request.path) > len(url.url) - 2 and
                         self.request.path[:(len(url.url)-1)] == url.url[:-1]):
                    target_url = url

            # full URL processing
            else:
                if url.url == self.request.path:
                    target_url = url

            # URL found - init the view class instance and return it to the caller
            if target_url:
                return target_url.viewClass(**target_url.viewParams)

    # Associate a url with a view, replacing existing assignments for the same url if replace is True
    def set_url(self, url: Url, replace: bool = False):
        if not any(existing_url for existing_url in self.urls if existing_url.url == url.url):
            self.urls.append(url)           # if no entry for this url, append
        elif replace:                       # if entry exists, replace if requested
            self.urls = [url if existing_url.url == url.url else existing_url for existing_url in self.urls]

    # return urls list with wildcards removed from urls, optionally - only of menu items
    def get_clean_urls(self, for_menu_only: bool = False):
        clean_urls = []
        for url in self.urls:
            if url.inMenu or not for_menu_only:
                if len(url.url) >= 2 and url.url[-2:] == "/*":
                    # create a copy of the original url for a wildcard url - not to modify the original
                    edited_url = deepcopy(url)
                    edited_url.url = url.url[:-2]    # modify the copy, removing wildcard
                    clean_urls.append(edited_url)
                else:
                    # just pass the link to the original unmodified url
                    clean_urls.append(url)
        """    
        # deepcopy variant - when menu items option was not present
        clean_urls = deepcopy(self.urls)
        for url in clean_urls:
            if len(url.url) >= 2 and url.url[-2:] == "/*":
                url.url = url.url[:-2]
        """
        return clean_urls


# Decorator to enable logging for a function
# May be called in two ways:
# @debug - without parameters
# @debug(logger=logger, level=level) - specifying any or both of the keyword parameters: logger and level
# IDEA:
def url(url: str, name: str = "", in_menu: bool = False, **kwargs):
    def add_url(func):
        Framework().set_url(Url(url, func, {**kwargs}, name, in_menu), replace=True)
        @wraps(func)                # Pass this function's metadata into the nested function
        def view_function(*args, **kwargs):
            return func(*args, **kwargs)
        return view_function
    return add_url
