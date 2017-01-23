import abc

from .utils import remerge


class Resource(abc.ABC):

    def __init__(self, obj, request):
        self.obj = obj
        self.request = request


class ViewableResource(abc.ABC):

    @abc.abstractmethod
    def asdict(self):
        raise NotImplemented()  # pragma: no cover


class EditableResource(abc.ABC):

    @abc.abstractmethod
    def validate(self, data, partial):
        raise NotImplemented()  # pragma: no cover

    @abc.abstractmethod
    def update_data(self, data, replace):
        raise NotImplemented()  # pragma: no cover

    def complete_data(self, data):
        return remerge([self.asdict(), data])

    @abc.abstractmethod
    def asdict(self):
        raise NotImplemented()  # pragma: no cover


class DeletableResource(abc.ABC):

    @abc.abstractmethod
    def delete(self):
        raise NotImplemented()  # pragma: no cover


class CollectionResource(abc.ABC):
    def validate_resource(self, data):
        raise NotImplemented()  # pragma: no cover

    def add_resource(self, data):
        raise NotImplemented()  # pragma: no cover
