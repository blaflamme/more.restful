from dectate import directive
import morepath

from .directives import ResourceAction


class RestfulApp(morepath.App):

    resource = directive(ResourceAction)


@RestfulApp.setting_section(section='restful')
def get_setting_section():
    return {
        'debug': False
    }
