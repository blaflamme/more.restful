from dectate import Query
from webob.exc import HTTPNoContent


def resource_head_view(obj, request, resource):
    return HTTPNoContent()


def resource_options_view(obj, request, resource):
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


def resource_get_view(obj, request, resource):
    return resource.get()


def resource_post_view(obj, request, resource):
    return resource.post()


def resource_put_view(obj, request, resource):
    return resource.put()


def resource_patch_view(obj, request, resource):
    return resource.patch()


def resource_delete_view(obj, request, resource):
    return resource.delete()
