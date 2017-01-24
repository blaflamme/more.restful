# more.restful

`more.restful` is an extension for [Morepath](http://morepath.readthedocs.io) inspired by [rest-toolkit](https://github.com/wichert/rest_toolkit) that provides simple patterns for creating restful web services.

### Quickstart

The minimal usage when deriving from `more.restful.abc.Resource` simply maps HTTP methods to class functions of the same name if they exist. `HEAD` and `OPTIONS` methods are automatically added for the resource and `OPTIONS` sets `Allowed-Methods` header for methods defined on the resource.

```python
from more.restful import RestfulApp
from more.restful.abc import Resource


class App(RestfulApp):
    pass


@App.path(path='')
class Root(object):
    pass


@App.resource(model=Root)
class Default(Resource):
    def get(self):
        return {
            'hello': 'world'
        }


if __name__ == '__main__':
    morepath.run(App())

```

The flow is:

| Method | Class | Function |
| ------ | ----- | -------- |
| GET | Resource | get |
| POST | Resource | post |
| PUT | Resource | put |
| PATCH | Resource | patch |
| DELETE | Resource | delete |

### Default Resources

If your resource derives from `more.restful.abc.Resource` and one or more of the `default` resources like `more.restful.abc.ViewableResource`, then default views are provided, HTTP statuses and headers are set and another flow is used to help reduce boilerplate code like validation and data update.

As an example, for `more.restful.abc.ViewableResource` just implements the `asdict` method and you automatically get a `GET` view registered which returns the data returned by that method

```python
from more.restful import RestfulApp
from more.restful.abc import (
    Resource,
    ViewableResource
)


class App(RestfulApp):
    pass


@App.path(path='')
class Root(object):
    pass


@App.resource(model=Root)
class Default(Resource, ViewableResoure):
    def asdict(self):
        return {
            'hello': 'world'
        }


if __name__ == '__main__':
    morepath.run(App())

```

The flow is:

| Method | Classes | Functions |
| ------ | ----- | -------- |
| GET | Resource, ViewableResource | asdict |
| POST | Resource, CollectionResource | validate_resource -> add_resource |
| PUT | Resource, EditableResource | validate -> update_data -> asdict |
| PATCH | Resource, EditableResource | validate -> update_data -> asdict |
| DELETE | Resource, DeletableResource | delete |

### Schema Validation

`Colander` and `Marshmallow` are supported for resource validation against a schema and they provides an implementation for `validate()` as required by `more.restful.abc.EditableResource`.

Using `more.restful.validation.colander.ColanderSchemaValidation`:

```python
import colander
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


if __name__ == '__main__':
    morepath.run(App())

```

Using `more.restful.validation.marshmallow.MarshmallowSchemaValidation`:

```python
import marshmallow
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


if __name__ == '__main__':
    morepath.run(App())
```
