from webtest import TestApp as Client

from more.restful.abc import Resource
from more.restful import RestfulApp
from more.restful.tests.fixtures.base import (
    TestApp as App,
    TestModel as Model
)


def test_default_resource_methods():

    class App(RestfulApp):
        pass

    @App.path(path='')
    class Model(object):
        def __init__(self):
            pass

    @App.resource(model=Model)
    class Default(Resource):
        pass

    app = App()
    c = Client(app)

    response = c.head('/')
    assert response.body == b''

    response = c.options('/')
    assert response.headers['Access-Control-Allow-Methods'] == 'HEAD, OPTIONS'

    response = c.get('/', status=405)
    response = c.post('/', status=405)
    response = c.put('/', status=405)
    response = c.patch('/', status=405)
    response = c.delete('/', status=405)


def test_resource_all_methods():

    class App(RestfulApp):
        pass

    @App.path(path='')
    class Model(object):
        def __init__(self):
            pass

    @App.resource(model=Model)
    class Default(Resource):

        def get(self):
            return {
                'method': 'GET'
            }

        def post(self):
            return {
                'method': 'POST'
            }

        def put(self):
            return {
                'method': 'PUT'
            }

        def patch(self):
            return {
                'method': 'PATCH'
            }

        def delete(self):
            return {
                'method': 'DELETE'
            }

    app = App()
    c = Client(app)

    response = c.options('/')
    assert response.headers['Access-Control-Allow-Methods'] == \
        'DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT'

    response = c.get('/')
    assert response.json_body == {'method': 'GET'}

    response = c.post('/')
    assert response.json_body == {'method': 'POST'}

    response = c.put('/')
    assert response.json_body == {'method': 'PUT'}

    response = c.patch('/')
    assert response.json_body == {'method': 'PATCH'}

    response = c.delete('/')
    assert response.json_body == {'method': 'DELETE'}
