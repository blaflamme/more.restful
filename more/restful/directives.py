from dectate import Composite
from morepath.directive import JsonAction

from .abc import (
    Resource,
    ViewableResource,
    CollectionResource,
    EditableResource,
    DeletableResource
)
from .views import (
    resource_head_view,
    resource_options_view,
    resource_get_view,
    resource_post_view,
    resource_put_view,
    resource_patch_view,
    resource_delete_view,
)


def resource_view_handler(view, resource, smart=True):

    def handle_resource(obj, request):
        inst = resource(obj, request)
        return view(obj, request, inst, smart)

    return handle_resource


def resource_composite_action(method, obj, model, permission, smart=True):
    views = {
        'HEAD': resource_head_view,
        'OPTIONS': resource_options_view,
        'GET': resource_get_view,
        'POST': resource_post_view,
        'PUT': resource_put_view,
        'PATCH': resource_patch_view,
        'DELETE': resource_delete_view
    }
    view = resource_view_handler(views.get(method), obj, smart)
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
        view_permission=None,
        edit_permission=None,
        add_permission=None,
        delete_permission=None
        ):
        self.model = model
        self.view_permission = view_permission
        self.edit_permission = edit_permission
        self.add_permission = add_permission
        self.delete_permission = delete_permission

    def actions(self, obj):
        views = []
        for method, permission in [
            ('HEAD', self.view_permission),
            ('OPTIONS', self.view_permission)
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
            for method, klass, permission in [
                ('GET', ViewableResource, self.view_permission),
                ('POST', CollectionResource, self.add_permission),
                ('PUT', EditableResource, self.edit_permission),
                ('PATCH', EditableResource, self.edit_permission),
                ('DELETE', DeletableResource, self.delete_permission)
                ]:
                smart = True if issubclass(obj, klass) else False
                if (smart) or (not smart and hasattr(obj, method.lower())):
                    views.append(
                        resource_composite_action(
                            method,
                            obj,
                            self.model,
                            permission,
                            smart=smart
                        )
                    )
        return views
