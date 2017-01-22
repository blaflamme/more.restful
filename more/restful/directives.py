from dectate import Composite
from morepath.directive import JsonAction

from .abc import Resource
from .views import (
    resource_head_view,
    resource_options_view,
    resource_get_view,
    resource_post_view,
    resource_put_view,
    resource_patch_view,
    resource_delete_view,
)


def resource_view_handler(view, resource):

    def handle_resource(obj, request):
        inst = resource(obj, request)
        return view(obj, request, inst)

    return handle_resource


def resource_composite_action(method, obj, model, permission):
    views = {
        'HEAD': resource_head_view,
        'OPTIONS': resource_options_view,
        'GET': resource_get_view,
        'POST': resource_post_view,
        'PUT': resource_put_view,
        'PATCH': resource_patch_view,
        'DELETE': resource_delete_view
    }
    view = resource_view_handler(views.get(method), obj)
    action = JsonAction(
        model,
        permission=permission,
        request_method=method
    )
    return (action, view)


class ResourceAction(Composite):

    def __init__(
        self,
        model,
        permission=None
        ):
        self.model = model
        self.permission = permission

    def actions(self, obj):
        views = []
        for method, permission in [
            ('HEAD', self.permission),
            ('OPTIONS', self.permission)
            ]:
            views.append(
                resource_composite_action(
                    method,
                    obj,
                    self.model,
                    permission
                )
            )
        if issubclass(obj, Resource):
            for method, permission in [
                ('GET', self.permission),
                ('POST', self.permission),
                ('PUT', self.permission),
                ('PATCH', self.permission),
                ('DELETE', self.permission)
                ]:
                if hasattr(obj, method.lower()):
                    views.append(
                        resource_composite_action(
                            method,
                            obj,
                            self.model,
                            permission
                        )
                    )
        return views
