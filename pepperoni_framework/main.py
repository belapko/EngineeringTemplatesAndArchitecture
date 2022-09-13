import json

from pepperoni_framework.requests import Get, Post


class PageNotFound404:
    def __call__(self, request):
        return '404 ERROR', 'WARNING! You have reached a secret page! Leave immediately!'


class Pepperoni:
    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        if not path.endswith('/'):
            path = f'{path}/'

        request = {}
        method = environ['REQUEST_METHOD']
        request['method'] = method
        if method == 'POST':
            data = Post().get_request_params(environ)
            request['data'] = data
            print(f'Получен post-запрос: {Pepperoni.decode_value(data)}')

        elif method == 'GET':
            request_params = Get().get_request_params(environ)
            request['request_params'] = request_params
            print(f'Получены get-параметры: {Pepperoni.decode_value(request_params)}')

        view = self.routes[path] if path in self.routes else PageNotFound404()
        [front(request) for front in self.fronts]
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        new_data = {}
        for key, str_value in data.items():
            while '%' in str_value:
                idx = str_value.index('%')
                hex_part = str_value[idx: idx + 3]
                str_value = str_value.replace(hex_part, bytes.fromhex(hex_part[1:]).decode('utf-8'))
            new_data[key] = str_value
        return new_data


class DebugApplication(Pepperoni):
    def __init__(self, routes, fronts):
        self.application = Pepperoni(routes, fronts)
        super().__init__(routes, fronts)

    def __call__(self, env, start_response):
        print('DEBUG MODE')
        print(env)
        return self.application(env, start_response)
