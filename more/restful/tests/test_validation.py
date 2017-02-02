import colander
import marshmallow
from webtest import TestApp as Client
from more.restful import RestfulApp


class ColanderAccountSchema(colander.Schema):
    email = colander.SchemaNode(
        colander.String()
    )
    password = colander.SchemaNode(
        colander.String(),
        missing=colander.drop
    )


class MarshmallowAccountSchema(marshmallow.Schema):
    email = marshmallow.fields.String(required=True)
    password = marshmallow.fields.String()


def test_colander_validation_methods():

    class App(RestfulApp):
        pass

    class Account:
        def __init__(self):
            self.email = 'john@example.com'
            self.password = 'Jane'

    @App.path(model=Account, path='')
    def get_account(request):
        return Account()

    @App.dump_json(model=Account)
    def dump_account_json(self, request):
        return {
            'email': self.email,
            'password': self.password
        }

    with App.resource(model=Account) as resource:

        @resource(request_method='POST', schema=ColanderAccountSchema)
        def post(self, request, schema):
            return request.json

        @resource(request_method='PUT', schema=ColanderAccountSchema)
        def put(self, request, schema):
            return request.json

        @resource(request_method='PATCH', schema=ColanderAccountSchema)
        def patch(self, request, schema):
            return request.json

    app = App()
    c = Client(app)

    response = c.post_json('/', {'email': 'john@example.com', 'password': 'Jane'}, status=201)
    assert response.json == {'email': 'john@example.com', 'password': 'Jane'}
    c.post_json('/', status=422)

    response = c.put_json('/', {'email': 'john@example.com', 'password': 'Jane'}, status=200)
    assert response.json == {'email': 'john@example.com', 'password': 'Jane'}
    c.put_json('/', status=422)

    response = c.patch_json('/', {'email': 'john@example.com', 'password': 'Jane'})
    assert response.json == {'email': 'john@example.com', 'password': 'Jane'}
    c.patch_json('/', status=422)


def test_marshmallow_validation_methods():

    class App(RestfulApp):
        pass

    class Account:
        def __init__(self):
            self.email = 'john@example.com'
            self.password = 'Jane'

    @App.path(model=Account, path='')
    def get_account(request):
        return Account()

    @App.dump_json(model=Account)
    def dump_account_json(self, request):
        return {
            'email': self.email,
            'password': self.password
        }

    with App.resource(model=Account) as resource:

        @resource(request_method='POST', schema=MarshmallowAccountSchema)
        def post(self, request, schema):
            return request.json

        @resource(request_method='PUT', schema=MarshmallowAccountSchema)
        def put(self, request, schema):
            return request.json

        @resource(request_method='PATCH', schema=MarshmallowAccountSchema)
        def patch(self, request, schema):
            return request.json

    app = App()
    c = Client(app)

    response = c.post_json('/', {'email': 'john@example.com', 'password': 'Jane'}, status=201)
    assert response.json == {'email': 'john@example.com', 'password': 'Jane'}
    c.post_json('/', status=422)

    response = c.put_json('/', {'email': 'john@example.com', 'password': 'Jane'}, status=200)
    assert response.json == {'email': 'john@example.com', 'password': 'Jane'}
    c.put_json('/', status=422)

    response = c.patch_json('/', {'email': 'john@example.com', 'password': 'Jane'})
    assert response.json == {'email': 'john@example.com', 'password': 'Jane'}
    c.patch_json('/', status=422)
