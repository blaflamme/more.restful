import morepath


class RestfulApp(morepath.App):
    pass


@RestfulApp.setting_section(section='restful')
def get_setting_section():
    return {
        'debug': False
        }
