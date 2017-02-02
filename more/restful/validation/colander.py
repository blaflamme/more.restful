from webob.exc import HTTPBadRequest
import colander

from ..utils import remerge


def validate_schema(data, schema, obj=None, partial=False):
    inst = schema()
    if partial:
        data = remerge([obj, data])
    try:
        inst.deserialize(data)
    except colander.Invalid as e:
        raise HTTPBadRequest(e.msg)
    return (data, inst)
