from dectate import Query
from webob.exc import (
    HTTPNoContent,
    HTTPUnprocessableEntity
)


def resource_head_view(obj, request, resource, smart=True):
    return HTTPNoContent()


def resource_options_view(obj, request, resource, smart=True):
    methods = set()
    q = Query('json').filter(model=type(obj))
    for action, res in list(q(request.app)):
        if 'request_method' in action.predicates:
            methods.add(action.predicates.get('request_method'))

    @request.after
    def _after(response):
        response.headers.add(
            'Access-Control-Allow-Methods',
            ', '.join(sorted(methods))
        )
    return HTTPNoContent()


def resource_get_view(obj, request, resource, smart=True):
    if not smart:
        return resource.get()
    return resource.asdict()


def resource_post_view(obj, request, resource, smart=True):
    if not smart:
        return resource.post()
    try:
        data = request.json_body
    except ValueError:
        raise HTTPUnprocessableEntity()
    resource.validate_resource(data)

    @request.after
    def _after(response):
        response.status_int = 201
    return resource.add_resource(data)


def resource_put_view(obj, request, resource, smart=True):
    if not smart:
        return resource.put()
    try:
        data = request.json_body
    except ValueError:
        raise HTTPUnprocessableEntity()
    resource.validate(data, partial=False)
    r = resource.update_data(data, replace=True)
    return r if r is not None else resource.asdict()


def resource_patch_view(obj, request, resource, smart=True):
    if not smart:
        return resource.patch()
    try:
        data = request.json_body
    except ValueError:
        raise HTTPUnprocessableEntity()
    resource.validate(data, partial=True)
    r = resource.update_data(data, replace=False)
    return r if r is not None else resource.asdict()


def resource_delete_view(obj, request, resource, smart=True):
    if not smart:
        return resource.delete()
    resource.delete()
    return HTTPNoContent()
