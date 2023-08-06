import codefast as cf
from flask import request
from dofast.data.dynamic import TOKEN


def make_response(code: int, msg: str):
    return {'code': code, 'message': msg}


# AUTH off for URL shortener
_ALLOWED_PATHS = ['/s', '/bark', '/uploladed', '/hanlp',
                  '/hello', '/public', '/open_url_on_linux']


def authenticate_flask(app):
    @app.before_request
    def _():
        try:
            def unpack_header(h): return ', '.join("{}:{}".format(k, v)
                                                   for k, v in h.items())
            cf.info(
                '[INPUT]: request data is: {}, json: {}, args: {}, headers: {}'
                .format(request.data, request.json, request.args,
                        unpack_header(request.headers)))

            _path = request.path
            if any(map(lambda x: _path.startswith(x), _ALLOWED_PATHS)):
                return

            token = request.args.get('token', '')
            if token == TOKEN:
                cf.info('Authentication SUCCESS.')
                return

            cf.error(
                'Authentication failed. request data is: {}, json: {}, args: {}, headers{}'
                .format(request.data, request.json, request.args,
                        request.headers))

            return make_response(401, 'Authentication failed.')
        except BaseException as e:
            cf.error('Authentication exception', str(e))
            return make_response(401, 'Authentication failed.')
