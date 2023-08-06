from jinja2 import Template

from lightweb4py.views import View, BaseView
from lightweb4py.request import Request
from lightweb4py.response import Response
from lightweb4py.persistence import Persistence
from lightweb4py.settings import Environ
from lightweb4py.logger import debug

import lightweb4py.settings


# PARAMS AND PROPERTIES:
# element_class - class of the element to edit
# element_html_class_name - element class name to pass to html template
# element_title - title of the element to pass to html template
# html_template_form - html form to use as a template
# editor_field_template_names - html template names for editor fields
# PROPERTIES:
# editor_fields_template - jinja2 template with all editor fields
# HTML FORM
# element - the element to hold the data passed from this view to the html template
# DEFINE IN SUBCLASS: View parameters:
# class_name - name of the class being edited for page title
# RAISES:
# FileNotFoundError if editor field templates not found ( run() )
class ElementEditView(View):

    def __init__(self, element_class, element_html_class_name: str, element_title: str, html_template_form: str,
                 editor_field_template_names: tuple):
        self.element_class = element_class
        self.element_html_class_name = element_html_class_name
        self.element_title = element_title
        self.html_template_form = html_template_form
        self.editor_field_template_names = editor_field_template_names

    def run(self, request: Request, *args, **kwargs) -> Response:
        element_id = request.path_array[len(request.path_array)-1]
        if request.method == "GET":             # GET: отобразить форму редактирования элемента
            # Get the element with the specified id
            element = Persistence.engine(self.element_class).get(element_id)
            # category not found - create
            if not element or (element == []):
                element = [self.element_class()]
                is_new = True
            else:
                is_new = False

            # Load editor fields if not already loaded
            if not hasattr(self, 'editor_fields_template'):
                editor_fields_html = ""                                 # Create empty field string
                for editor_field in self.editor_field_template_names:   # Cycle through all templates
                    source_html, file_name, up_to_date = \
                        Environ().jinja_env.loader.get_source(Environ().jinja_env, editor_field)
                    editor_fields_html += source_html
                self.editor_fields_template = Environ().jinja_env.from_string(editor_fields_html)

            return BaseView(self.html_template_form,
                            element=element[0], element_class=self.element_html_class_name,
                            element_title=self.element_title, is_new=is_new,
                            editor_fields=self.editor_fields_template,
                            *args, **kwargs).run(request)

        elif request.method == "POST":          # POST: обработать данные формы обратной связи
            # Get button type and delete it to leave only the element properties in the query parameters
            button = request.query_params["button"]
            del request.query_params["button"]
            # Assume all the query parameters in the request are the destination element properties
            if button == "save":
                Persistence.engine(self.element_class).set(self.element_class(id=element_id, **request.query_params))
            elif button == "save_new":
                Persistence.engine(self.element_class).set(self.element_class(**request.query_params))
            elif button == "delete":
                Persistence.engine(self.element_class).delete(element_id)
            else:
                pass
                #pprint("Cancel requested")
            #return MinimalView("OK").run(request)
            return Response(status_code="302 Found", headers={'Location': '/'})


