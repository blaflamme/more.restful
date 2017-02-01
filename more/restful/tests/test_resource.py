from webtest import TestApp as Client

from more.restful.abc import (
    Resource,
    ViewableResource,
    CollectionResource,
    EditableResource,
    DeletableResource
)
from more.restful import RestfulApp


def test_default_resource_methods():

    class App(RestfulApp):
        pass

    @App.path(path='')
    class Model(object):
        def __init__(self):
            pass

    with App.resource(model=Model) as resource:

        @resource(defaults=True)
        def get(self, request):
            return {}

    app = App()
    c = Client(app)

    response = c.head('/', status=204)
    assert response.body == b''

    response = c.options('/', status=204)
    assert response.headers['Access-Control-Allow-Methods'] == 'GET, HEAD, OPTIONS'

    response = c.get('/', status=200)
    assert response.json == {}

    c.post('/', status=405)
    c.put('/', status=405)
    c.patch('/', status=405)
    c.delete('/', status=405)


def test_resource_all_methods():

    class App(RestfulApp):
        pass

    @App.path(path='')
    class Model(object):
        def __init__(self):
            pass

    with App.resource(model=Model) as resource:

        @resource(request_method='GET', defaults=True)
        def get(self, request):
            return {'foo': 'bar'}

        @resource(request_method='POST')
        def post(self, request, schema):
            return request.json

        @resource(request_method='PUT')
        def put(self, request, schema):
            return request.json

        @resource(request_method='PATCH')
        def patch(self, request, schema):
            return request.json

        @resource(request_method='DELETE')
        def delete(self, request):
            return {'foo': 'bar'}

    app = App()
    c = Client(app)

    response = c.options('/')
    assert response.headers['Access-Control-Allow-Methods'] == \
        'DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT'

    response = c.get('/', status=200)
    assert response.json == {'foo': 'bar'}

    response = c.post_json('/', {'foo': 'bar'}, status=201)
    assert response.json == {'foo': 'bar'}
    c.post_json('/', status=422)

    response = c.put_json('/', {'foo': 'bar'}, status=200)
    assert response.json == {'foo': 'bar'}
    c.put_json('/', status=422)

    response = c.patch_json('/', {'foo': 'bar'}, status=200)
    assert response.json == {'foo': 'bar'}
    c.patch_json('/', status=422)

    response = c.delete('/', status=204)
    assert response.body == b''
