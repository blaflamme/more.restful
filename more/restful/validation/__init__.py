from colander import Schema as ColanderSchema
from marshmallow import Schema as MarshmallowSchema

from .colander import validate_schema as validate_colander_schema
from .marshmallow import validate_schema as validate_marshmallow_schema


def get_validate_schema(schema):
    if issubclass(schema, ColanderSchema):
        return validate_colander_schema
    elif issubclass(schema, MarshmallowSchema):
        return validate_marshmallow_schema
    else:
        return None
