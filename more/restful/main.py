from dectate import directive
import morepath
from webob.exc import HTTPException

from .directives import ResourceAction
from .errors import (
    generic_exception_view,
    http_exception_view
)


class RestfulApp(morepath.App):

    resource = directive(ResourceAction)


@RestfulApp.setting_section(section='restful')
def get_setting_section():
    return {
        'debug': False
    }


# Setup error views
RestfulApp.json(model=Exception)(generic_exception_view)
RestfulApp.json(model=HTTPException)(http_exception_view)
