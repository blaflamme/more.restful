import abc
from webob.exc import HTTPBadRequest
import colander


def validate(data, schema):
    inst = schema()
    try:
        inst.deserialize(data)
    except colander.Invalid as e:
        raise HTTPBadRequest(e.msg)


class ColanderSchemaValidation(abc.ABC):

    @abc.abstractproperty
    def schema(self):
        raise NotImplemented()  # pragma: no cover

    def validate(self, data, partial=False):
        if partial:
            data = self.complete_data(data)
        validate(data, self.schema)
