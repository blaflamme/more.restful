import abc


class Resource(abc.ABC):

    def __init__(self, obj, request):
        self.obj = obj
        self.request = request
