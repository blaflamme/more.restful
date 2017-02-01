from webtest import TestApp as Client
from webob.exc import (
    HTTPBadRequest,
    HTTPNotFound
)

from more.restful.abc import Resource
from more.restful import RestfulApp


def test_generic_error():

    class App(RestfulApp):
        pass

    @App.path(path='/keyerror')
    class Model(object):
        pass

    @App.resource(model=Model)
    def get(self, request):
        raise KeyError('BOOM!')

    app = App()
    c = Client(app)

    response = c.get('/keyerror', status=500)
    error = response.json.get('error')
    assert error == {
        'code': 500,
        'message': 'BOOM!'
    }
    assert 'traceback' not in error


def test_generic_error_with_traceback():

    class App(RestfulApp):
        pass

    @App.path(path='/keyerror')
    class Model(object):
        pass

    @App.resource(model=Model)
    def get(self, request):
        raise KeyError('BOOM!')

    app = App()
    app.commit()
    app.settings.restful.debug = True
    c = Client(app)

    response = c.get('/keyerror', status=500)
    error = response.json.get('error')
    assert error['traceback'].find("raise KeyError('BOOM!')") >= 0


def test_http_exception_error():

    class App(RestfulApp):
        pass

    @App.path(path='/http-error')
    class Model(object):
        pass

    @App.resource(model=Model)
    def get(self, request):
        raise HTTPBadRequest()

    app = App()
    c = Client(app)

    response = c.get('/http-error', status=400)
    error = response.json.get('error')
    assert error == {
        'code': 400,
        'message': '400 Bad Request'
    }


def test_http_not_found_error():

    class App(RestfulApp):
        pass

    @App.path(path='/http-not-found')
    class Model(object):
        pass

    @App.resource(model=Model)
    def get(self, request):
        raise HTTPNotFound()

    app = App()
    c = Client(app)

    response = c.get('/http-not-found', status=404)
    error = response.json.get('error')
    assert error == {
        'code': 404,
        'message': '404 Not Found'
    }


def test_http_custom_message_error():

    class App(RestfulApp):
        pass

    @App.path(path='/http-custom-message')
    class Model(object):
        pass

    @App.resource(model=Model)
    def get(self, request):
        raise HTTPBadRequest('Custom Error')

    app = App()
    c = Client(app)

    response = c.get('/http-custom-message', status=400)
    error = response.json.get('error')
    assert error == {
        'code': 400,
        'message': 'Custom Error'
    }


def test_http_custom_json_error():

    class App(RestfulApp):
        pass

    @App.path(path='/http-custom-json')
    class Model(object):
        pass

    @App.resource(model=Model)
    def get(self, request):
        raise HTTPBadRequest(json={'foo': 'bar'})

    app = App()
    c = Client(app)

    response = c.get('/http-custom-json', status=400)
    assert response.json == {'foo': 'bar'}
