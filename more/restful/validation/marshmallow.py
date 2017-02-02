from webob.exc import HTTPBadRequest
import marshmallow

from ..utils import remerge


def validate_schema(data, schema, obj=None, partial=False):
    inst = schema(strict=True)
    if partial:
        data = remerge([obj, data])
    try:
        inst.validate(data)
    except marshmallow.ValidationError as e:
        raise HTTPBadRequest(e.messages)
    return (data, inst)
