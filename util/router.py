class Router:

    def __init__(self):
        self.routes = []
        pass

    def add_route(self, method, path, action, exact_path=False):
        self.routes.append((method, path, action, exact_path))
        pass

    def route_request(self, request, handler):
        for route in self.routes:
            method, path, action, exact_path = route
            if request.method == method:
                if exact_path:
                    if request.path == path:
                        return action(request, handler)
                else:
                    if request.path.startswith(path):
                        return action(request, handler) 

        response_404 = ("HTTP/1.1 404 Not Found\r\n""Content-Type: text/plain\r\n""Content-Length: 15\r\n""\r\n""404 Not Found")

        handler.request.sendall(response_404.encode())
