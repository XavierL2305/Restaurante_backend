from .utils.utils import set_request_actual


class AuditoriaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        set_request_actual(request)
        try:
            return self.get_response(request)
        finally:
            set_request_actual(None)