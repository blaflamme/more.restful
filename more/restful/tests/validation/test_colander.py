import colander
from webtest import TestApp as Client

from more.restful.validation.colander import ColanderSchemaValidation
from more.restful.abc import (
    Resource,
    EditableResource
)
from more.restful import RestfulApp


class AccountSchema(colander.Schema):
    email = colander.SchemaNode(
        colander.String()
    )
    password = colander.SchemaNode(
        colander.String(),
        missing=colander.drop
    )


class App(RestfulApp):
    pass


@App.path(path='')
class Model(object):
    pass


@App.resource(model=Model)
class Default(
    ColanderSchemaValidation,
    Resource,
    EditableResource
    ):

    schema = AccountSchema

    def update_data(self, data, replace):
        pass

    def asdict(self):
        return {}


def test_resource_colander_validation():

    app = App()
    c = Client(app)

    response = c.put_json('/', {'email': 'john@example.com', 'password': 'Jane'})
    assert response.json == {}

    response = c.patch_json('/', {'email': 'john@example.com'})
    assert response.json == {}


def test_resource_colander_validation_error():

    error = {
        'error': {
            'code': 400,
            'message': '400 Bad Request'
        }
    }

    app = App()
    c = Client(app)

    response = c.put_json('/', {'password': 'Jane'}, status=400)
    assert response.json == error

    response = c.patch_json('/', {'password': 'Jane'}, status=400)
    assert response.json == error
