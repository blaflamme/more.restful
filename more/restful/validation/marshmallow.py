import abc
from webob.exc import HTTPBadRequest
import marshmallow


def validate(data, schema):
    inst = schema(strict=True)
    try:
        inst.validate(data)
    except marshmallow.ValidationError as e:
        raise HTTPBadRequest(e.messages)


class MarshmallowSchemaValidation(abc.ABC):

    @abc.abstractproperty
    def schema(self):
        raise NotImplemented()  # pragma: no cover

    def validate(self, data, partial=False):
        if partial:
            data = self.complete_data(data)
        validate(data, self.schema)
