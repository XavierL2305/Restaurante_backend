import threading

_request_local = threading.local()


def set_request_actual(request):
    _request_local.request = request


def get_request_actual():
    return getattr(_request_local, 'request', None)


def tomar_cliente_ip(request=None):
    request_obj = request
    if request_obj is None:
        request_obj = get_request_actual()

    if request_obj is None:
        return 'desconocida'

    meta = getattr(request_obj, 'META', {}) or {}
    x_forwarded_for = meta.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()

    return meta.get('REMOTE_ADDR', 'desconocida')