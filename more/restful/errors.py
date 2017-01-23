import sys
import traceback
from webob import Response


def generic_exception_view(self, request):
    error = {'code': 500}

    try:
        error['message'] = self.args[0]
    except IndexError:
        error['message'] = 'Unknown error'

    if request.app.settings.restful.debug:
        exc_info = sys.exc_info()
        error['traceback'] = ''.join(
            traceback.format_exception(*exc_info)
        )

    @request.after
    def _after(response):
        response.status_int = error['code']

    return {
        'error': error
    }


def http_exception_view(self, request):
    if isinstance(self, Response) and self.content_type == 'application/json':
        return self
    error = {'code': self.status_int}

    if hasattr(self, 'detail') and self.detail is not None:
        error['message'] = self.detail
    elif hasattr(self, 'message'):
        error['message'] = self.message
    else:
        error['message'] = self.status

    @request.after
    def _after(response):
        response.status_int = error['code']
        response.status = self.status
        for (header, value) in self.headers.items():
            if header in {'Content-Type', 'Content-Length'}:
                continue
            response.headers[header] = value

    return {
        'error': error
    }
