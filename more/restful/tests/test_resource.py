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

    @App.resource(model=Model)
    class Default(Resource):
        pass

    app = App()
    c = Client(app)

    response = c.head('/')
    assert response.body == b''

    response = c.options('/')
    assert response.headers['Access-Control-Allow-Methods'] == 'HEAD, OPTIONS'

    c.get('/', status=405)
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
    assert response.json == {'method': 'GET'}

    response = c.post('/')
    assert response.json == {'method': 'POST'}

    response = c.put('/')
    assert response.json == {'method': 'PUT'}

    response = c.patch('/')
    assert response.json == {'method': 'PATCH'}

    response = c.delete('/')
    assert response.json == {'method': 'DELETE'}


def test_viewable_resource():

    class App(RestfulApp):
        pass

    @App.path(path='')
    class Model(object):
        def __init__(self):
            self.name = 'test'

    @App.resource(model=Model)
    class Default(Resource, ViewableResource):

        def asdict(self):
            return {
                'name': self.obj.name
            }

    app = App()
    c = Client(app)

    response = c.get('/')
    assert response.json == {'name': 'test'}


def test_editable_resource():

    class App(RestfulApp):
        pass

    @App.path(path='')
    class Model(object):
        def __init__(self):
            self.name = 'test'

    @App.resource(model=Model)
    class Default(Resource, EditableResource):

        def validate(self, data, partial):
            if partial:
                data = self.complete_data(data)
            return data

        def update_data(self, data, replace):
            self.name = data.get('name', 'test')
            return data

        def asdict(self):
            return {
                'name': self.obj.name
            }

    app = App()
    c = Client(app)

    response = c.put_json('/', {'name': 'test2'})
    assert response.json == {'name': 'test2'}
    c.put_json('/', status=422)

    response = c.patch_json('/', {'name': 'test3'})
    assert response.json == {'name': 'test3'}
    c.patch_json('/', status=422)


def test_deletable_resource():

    class App(RestfulApp):
        pass

    @App.path(path='')
    class Model(object):
        def __init__(self):
            pass

    @App.resource(model=Model)
    class Default(Resource, DeletableResource):

        def delete(self):
            pass

    app = App()
    c = Client(app)

    c.delete_json('/', status=204)


def test_collection_resource():

    class App(RestfulApp):
        pass

    @App.path(path='')
    class Model(object):
        def __init__(self):
            self.name = None

    @App.resource(model=Model)
    class Default(Resource, CollectionResource):

        def asdict(self):
            return {
                'name': self.obj.name
            }

        def validate_resource(self, data):
            pass

        def add_resource(self, data):
            self.obj.name = data.get('name', 'test')
            return self.asdict()

    app = App()
    c = Client(app)

    response = c.post_json('/', {'name': 'test4'}, status=201)
    assert response.json == {'name': 'test4'}
    c.post_json('/', status=422)
