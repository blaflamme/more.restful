# more.restful

`more.restful` is an extension for [Morepath](http://morepath.readthedocs.io)
that provides a pattern for creating restful web services.

Example usage:

```python
from .app import App
from .abc import (
    Resource,
    ViewableResource
)
from .models import (
    Root,
    Data
)


@App.resource(model=Root)
class RootResource(Resource):

    def get(self):
        return self.obj


@App.resource(model=Data)
class DataResource(Resource, ViewableResource):

    def render(self):
        return self.obj
```
