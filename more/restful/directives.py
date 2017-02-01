from dectate import Composite
from morepath.directive import JsonAction

from .views import (
    resource_head_view,
    resource_options_view,
    resource_get_view,
    resource_post_view,
    resource_put_view,
    resource_patch_view,
    resource_delete_view,
)


def resource_view_handler(view, schema, func):

    def handle_resource(obj, request):
        return view(obj, request, schema, func)

    return handle_resource


def resource_composite_action(
    obj,
    model,
    schema,
    permission,
    internal,
    **predicates
    ):
    views = {
        'HEAD': resource_head_view,
        'OPTIONS': resource_options_view,
        'GET': resource_get_view,
        'PUT': resource_put_view,
        'PATCH': resource_patch_view,
        'POST': resource_post_view,
        'DELETE': resource_delete_view
    }
    method = predicates['request_method']
    view = resource_view_handler(views.get(method), schema, obj)
    action = JsonAction(
        model,
        permission=permission,
        internal=internal,
        **predicates
    )
    return (action, view)


class ResourceAction(Composite):

    query_classes = [JsonAction]

    def __init__(
        self,
        model,
        schema=None,
        defaults=False,
        permission=None,
        internal=None,
        **predicates
        ):
        self.model = model
        self.schema = schema
        self.defaults = defaults
        self.permission = permission
        self.internal = internal
        self.predicates = predicates

    def actions(self, obj):
        views = []

        if 'request_method' not in self.predicates:
            self.predicates['request_method'] = 'GET'

        if self.defaults:
            for method in ('HEAD', 'OPTIONS'):
                predicates = self.predicates.copy()
                predicates['request_method'] = method
                views.append(
                    resource_composite_action(
                        obj,
                        self.model,
                        self.schema,
                        self.permission,
                        self.internal,
                        **predicates
                    )
                )
        views.append(
            resource_composite_action(
                obj,
                self.model,
                self.schema,
                self.permission,
                self.internal,
                **self.predicates
            )
        )

        return views
