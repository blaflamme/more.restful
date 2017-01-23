import abc

from .utils import remerge


class Resource(abc.ABC):

    def __init__(self, obj, request):
        self.obj = obj
        self.request = request


class ViewableResource(abc.ABC):

    @abc.abstractmethod
    def asdict(self):
        raise NotImplemented()


class EditableResource(abc.ABC):

    @abc.abstractmethod
    def validate(self, data, partial):
        raise NotImplemented()

    @abc.abstractmethod
    def update_data(self, data, replace):
        raise NotImplemented()

    def complete_data(self, data):
        return remerge([self.asdict(), data])

    @abc.abstractmethod
    def asdict(self):
        raise NotImplemented()


class DeletableResource(abc.ABC):

    @abc.abstractmethod
    def delete(self):
        raise NotImplemented()


class CollectionResource(abc.ABC):
    def validate_resource(self, data):
        raise NotImplemented()

    def add_resource(self, data):
        raise NotImplemented()
