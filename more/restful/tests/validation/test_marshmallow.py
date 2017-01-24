import marshmallow
from webtest import TestApp as Client

from more.restful.validation.marshmallow import MarshmallowSchemaValidation
from more.restful.abc import (
    Resource,
    EditableResource
)
from more.restful import RestfulApp


class AccountSchema(marshmallow.Schema):
    email = marshmallow.fields.String(required=True)
    password = marshmallow.fields.String()


class App(RestfulApp):
    pass


@App.path(path='')
class Model(object):
    pass


@App.resource(model=Model)
class Default(
    MarshmallowSchemaValidation,
    Resource,
    EditableResource
    ):

    schema = AccountSchema

    def update_data(self, data, replace):
        pass

    def asdict(self):
        return {}


def test_resource_marshmallow_validation():

    app = App()
    c = Client(app)

    response = c.put_json('/', {'email': 'john@example.com', 'password': 'Jane'})
    assert response.json == {}

    response = c.patch_json('/', {'email': 'john@example.com'})
    assert response.json == {}


def test_resource_marshmallow_validation_error():

    error = {
        'error': {
            'code': 400,
            'message': {
                'email': ['Missing data for required field.']
            }
        }
    }

    app = App()
    c = Client(app)

    response = c.put_json('/', {'password': 'Jane'}, status=400)
    assert response.json == error

    response = c.patch_json('/', {'password': 'Jane'}, status=400)
    assert response.json == error
