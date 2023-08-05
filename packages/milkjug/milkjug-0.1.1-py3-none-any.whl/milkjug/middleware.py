class Middleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        environ = self.modify_request(environ)
        status, response_headers, response_body = self.handle_request(environ)
        status, response_headers, response_body = self.modify_response(status, response_headers, response_body)
        start_response(status, response_headers)
        return [response_body]
    
    def modify_request(self, environ):
        return environ
    
    def handle_request(self, environ):
        return self.app.handle_request(environ)

    def modify_response(self, status, response_headers, response_body):
        return status, response_headers, response_body