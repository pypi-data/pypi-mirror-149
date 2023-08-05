import json
from parse import parse

from .middleware import Middleware
from .utils import dictify_query

class Api:
    def __init__(self):
        self.routes = {}
        self.middleware = Middleware(self)

    def __call__(self, environ, start_response):
        return self.middleware(environ, start_response)

    def handle_request(self, environ):
        kwargs, handler = self.get_handler(environ["PATH_INFO"], environ["REQUEST_METHOD"], environ["QUERY_STRING"])
        print(kwargs)
        if handler is not None:
            response_body = handler(**kwargs)
            if isinstance(response_body, dict) or isinstance(response_body, list):
                response_headers = [("Content-Type", "application/json")]
                response_body = json.dumps(response_body).encode()
            else:
                response_headers = [("Content-Type", "text/plain")]
                response_body = str(response_body).encode()
            return "200 OK", response_headers, response_body
        else:
            return "404 Not Found", [("Content-Type", "text/plain")], b"Page Not Found"

    def get_handler(self, path, method, query):
        for route in self.routes.keys():
            path_params = parse(route, path)
            if path_params is not None:
                kwargs = {**path_params.named, **dictify_query(query)}
                handler = self.routes[route].get(method)
                return kwargs, handler
        return None, None

    def add_handler(self, path, method, handler):
        if self.routes.get(path, {}).get(method) is None:
            self.routes[path] = {**self.routes.get(path, {}), method: handler}
        else:
            raise Exception("Route already exists")
    
    def route(self, path, allowed_methods=None):
        if allowed_methods is None:
            allowed_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
        
        def wrapper(handler):
            for method in allowed_methods:
                self.add_handler(path, method, handler)
        return wrapper
    
    def add_middleware(self, midlleware):
        self.middleware = midlleware(self.middleware)