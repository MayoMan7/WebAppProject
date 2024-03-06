import re

class Router:  
    routes = []
    def __init__(self):
        self.routes = []

    def add_route(self, method, path, function):
        self.routes.append((method, re.compile(path), function))
    

    def route_request(self, request):
        method = request.method
        path = request.path

        for route in self.routes:
            if route[0] == method:
                if re.match(route[1], path):
                    function = route[2]
                    return function(request)
            
        responce = request.http_version
        responce += " 404 Not Found\r\n"
        responce +="Content-Type: text/plain\r\n"
        responce += "X-Content-Type-Options: nosniff\r\n"
        body = "The requested content does not exist"
        bytes = len(body)
        responce +="Content-Length: " + str(bytes) + "\r\n\r\n" + body
        return responce.encode()
    


