import socketserver
from util.request import Request


class MyTCPHandler(socketserver.BaseRequestHandler):

    def root_response(self,request):
        responce = request.http_version
        responce += " 200 OK\r\n"
        responce +="Content-Type: text/html\r\n"

        name = "public/index.html"
        with open(name, "rb") as file:
            data = file.read()
            bytes = len(data)
            body = data.decode()
        
        body = body.replace("{{visits}}", "HEY")
        
            
        responce +="Content-Length: " + str(bytes) + "r\n\r\n" + body
        return responce
    
    def eagle_response(self,request):
        responce = request.http_version
        responce += " 200 OK\r\n"
        responce +="Content-Type: image/jpeg\r\n"


        name = "public\image\eagle.jpg"
        with open(name, "rb") as file:
            data = file.read()
            bytes = len(data)
            body = data
        
            
        responce +="Content-Length: " + str(bytes) + "r\n\r\n" + body
        return responce
    
    def favico_response(self,request):
        responce = request.http_version
        responce += " 200 OK\r\n"
        responce +="Content-Type: image/x-icon\r\n"


        name = "public/favicon.ico"
        with open(name, "rb") as file:
            data = file.read()
            bytes = len(data)
            body = data
        
            
        responce +="Content-Length: " + str(bytes) + "r\n\r\n" + str(body)
        return responce
        
    def webrtc_response(self,request):
        responce = request.http_version
        responce += " 200 OK\r\n"
        responce +="Content-Type: text/js\r\n"

        name = "public/webrtc.js"
        with open(name, "rb") as file:
            data = file.read()
            bytes = len(data)
            body = data.decode()
        
            
        responce +="Content-Length: " + str(bytes) + "r\n\r\n" + body
        return responce
    
    def js_response(self,request):
        responce = request.http_version
        responce += " 200 OK\r\n"
        responce +="Content-Type: text/js\r\n"

        name = "public/function.js"
        with open(name, "rb") as file:
            data = file.read()
            bytes = len(data)
            body = data.decode()
        
            
        responce +="Content-Length: " + str(bytes) + "r\n\r\n" + body
        return responce
    
    def css_response(self,request):
        responce = request.http_version
        responce += " 200 OK\r\n"
        responce +="Content-Type: text/css\r\n"

        name = "public/style.css"
        with open(name, "rb") as file:
            data = file.read()
            bytes = len(data)
            body = data.decode()
                    
        responce +="Content-Length: " + str(bytes) + "r\n\r\n" + body
        return responce

        
    def handle(self):
        received_data = self.request.recv(2048)
        print(self.client_address)
        # print("--- received data ---")
        # print(received_data)
        # print("--- end of data ---\n\n")
        request = Request(received_data)
        # TODO: Parse the HTTP request and use self.request.sendall(response) to send your response
        print("--- PATH REQUESTED ---")
        print(request.path)


        if request.path == "/":
            response = self.root_response(request).encode()
            self.request.sendall(response)
        if request.path == "/public/style.css":
            response = self.css_response(request).encode()
            self.request.sendall(response)
        if request.path == "/public/function.js":
            response = self.js_response(request).encode()
            self.request.sendall(response)
        if request.path == "/public/webrtc.js":
            response = self.webrtc_response(request).encode()
            self.request.sendall(response)
        if request.path == "/public/image/eagle.jpg":
            response = self.eagle_response(request).encode()
            self.request.sendall(response)
        if request.path == "/public/favicon.ico":
            response = self.favico_response(request).encode()
            self.request.sendall(response)
            




def main():
    host = "0.0.0.0"
    port = 8080

    socketserver.TCPServer.allow_reuse_address = True

    server = socketserver.TCPServer((host, port), MyTCPHandler)

    print("Listening on port " + str(port))

    # server.serve_forever()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Server is shutting down...") 
        server.server_close()


if __name__ == "__main__":
    main()
