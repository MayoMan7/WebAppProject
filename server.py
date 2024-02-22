import socketserver
from util.request import Request


class MyTCPHandler(socketserver.BaseRequestHandler):

    def root_response(self,request):
        responce = request.http_version
        responce += " 200 OK\r\n"
        responce +="Content-Type: text/html\r\n"
        responce += "X-Content-Type-Options: nosniff\r\n"

        if "visits" in request.cookies:
            count = int(request.cookies["visits"])
            count += 1
            responce += "Set-Cookie: visits=" + str(count) + "; Max-Age=3600\r\n"
        else:
            count = 1
            responce += "Set-Cookie: visits=" + str(count) + "; Max-Age=3600\r\n"

        name = "public/index.html"
        with open(name, "rb") as file:
            data = file.read()
            body = data.decode()
            body = body.replace("{{visits}}", str(count))
            print(body)
            body = body.replace("🙂", "&#128578;")
        

        
        bytes = len(body)
        print(responce)
        responce +="Content-Length: " + str(bytes) + "\r\n\r\n" + body
        responce = responce.encode()
        return responce
    
    def eagle_response(self,request):
        responce = request.http_version
        responce += " 200 OK\r\n"
        responce +="Content-Type: image/jpeg\r\n"
        responce += "X-Content-Type-Options: nosniff\r\n"


        name = "public/image/eagle.jpg"
        with open(name, "rb") as file:
            data = file.read()
            bytes = len(data)
            body = data
            
        responce +="Content-Length: " + str(bytes) + "\r\n\r\n"
        responce = responce.encode()
        responce += body
        return responce  

    def cat_response(self,request):
        responce = request.http_version
        responce += " 200 OK\r\n"
        responce +="Content-Type: image/jpeg\r\n"
        responce += "X-Content-Type-Options: nosniff\r\n"


        name = "public/image/cat.jpg"
        with open(name, "rb") as file:
            data = file.read()
            bytes = len(data)
            body = data
            
        responce +="Content-Length: " + str(bytes) + "\r\n\r\n"
        responce = responce.encode()
        responce += body
        return responce

    def dog_response(self,request):
        responce = request.http_version
        responce += " 200 OK\r\n"
        responce +="Content-Type: image/jpeg\r\n"
        responce += "X-Content-Type-Options: nosniff\r\n"


        name = "public/image/dog.jpg"
        with open(name, "rb") as file:
            data = file.read()
            bytes = len(data)
            body = data
            
        responce +="Content-Length: " + str(bytes) + "\r\n\r\n"
        responce = responce.encode()
        responce += body
        return responce

    def e_small_response(self,request):
        responce = request.http_version
        responce += " 200 OK\r\n"
        responce +="Content-Type: image/jpeg\r\n"
        responce += "X-Content-Type-Options: nosniff\r\n"


        name = "public/image/elephant-small.jpg"
        with open(name, "rb") as file:
            data = file.read()
            bytes = len(data)
            body = data
            
        responce +="Content-Length: " + str(bytes) + "\r\n\r\n"
        responce = responce.encode()
        responce += body
        return responce

    def e_response(self,request):
        responce = request.http_version
        responce += " 200 OK\r\n"
        responce +="Content-Type: image/jpeg\r\n"
        responce += "X-Content-Type-Options: nosniff\r\n"


        name = "public/image/elephant.jpg"
        with open(name, "rb") as file:
            data = file.read()
            bytes = len(data)
            body = data
            
        responce +="Content-Length: " + str(bytes) + "\r\n\r\n"
        responce = responce.encode()
        responce += body
        return responce

    def flamingo_response(self,request):
        responce = request.http_version
        responce += " 200 OK\r\n"
        responce +="Content-Type: image/jpeg\r\n"
        responce += "X-Content-Type-Options: nosniff\r\n"

        name = "public/image/flamingo.jpg"
        with open(name, "rb") as file:
            data = file.read()
            bytes = len(data)
            body = data
            
        responce +="Content-Length: " + str(bytes) + "\r\n\r\n"
        responce = responce.encode()
        responce += body
        return responce

    def kitten_response(self,request):
        responce = request.http_version
        responce += " 200 OK\r\n"
        responce +="Content-Type: image/jpeg\r\n"
        responce += "X-Content-Type-Options: nosniff\r\n"


        name = "public/image/kitten.jpg"
        with open(name, "rb") as file:
            data = file.read()
            bytes = len(data)
            body = data
            
        responce +="Content-Length: " + str(bytes) + "\r\n\r\n"
        responce = responce.encode()
        responce += body
        return responce
    
    def favico_response(self,request):
        responce = request.http_version
        responce += " 200 OK\r\n"
        responce +="Content-Type: image/x-icon\r\n"
        responce += "X-Content-Type-Options: nosniff\r\n"


        name = "public/favicon.ico"
        with open(name, "rb") as file:
            data = file.read()
            bytes = len(data)
            body = data
        
            
        responce +="Content-Length: " + str(bytes) + "\r\n\r\n" 
        responce = responce.encode()
        responce += body
        return responce
        
    def webrtc_response(self,request):
        responce = request.http_version
        responce += " 200 OK\r\n"
        responce +="Content-Type: text/javascript\r\n"
        responce += "X-Content-Type-Options: nosniff\r\n"

        name = "public/webrtc.js"
        with open(name, "rb") as file:
            data = file.read()
            bytes = len(data)
            body = data.decode()
        
        
        responce +="Content-Length: " + str(bytes) + "\r\n\r\n" + body
        return responce
    
    def js_response(self,request):
        responce = request.http_version
        responce += " 200 OK\r\n"
        responce +="Content-Type: text/javascript\r\n"
        responce += "X-Content-Type-Options: nosniff\r\n"

        name = "public/functions.js"
        with open(name, "rb") as file:
            data = file.read()
            body = data.decode()
            body = body.replace("😀", "&#128512;")
            bytes = len(body)
        
            
        responce +="Content-Length: " + str(bytes) + "\r\n\r\n" + body
        return responce
    
    def css_response(self,request):
        responce = request.http_version
        responce += " 200 OK\r\n"
        responce +="Content-Type: text/css\r\n"
        responce += "X-Content-Type-Options: nosniff\r\n"

        name = "public/style.css"
        with open(name, "rb") as file:
            data = file.read()
            bytes = len(data)
            body = data.decode()
                    
        responce +="Content-Length: " + str(bytes) + "\r\n\r\n" + body
        return responce
    
    def bad_responce(self,request):
        responce = request.http_version
        responce += " 404 Not Found\r\n"
        responce +="Content-Type: text/plain\r\n"
        responce += "X-Content-Type-Options: nosniff\r\n"
        body = "The requested content does not exist"
        bytes = len(body)
        responce +="Content-Length: " + str(bytes) + "\r\n\r\n" + body
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

        request.cookies.get("visits")


        if request.path == "/":
            response = self.root_response(request)
            self.request.sendall(response)

        if request.path == "/public/style.css":
            response = self.css_response(request).encode()
            self.request.sendall(response)

        if request.path == "/public/functions.js":
            response = self.js_response(request).encode()
            self.request.sendall(response)

        if request.path == "/public/webrtc.js":
            response = self.webrtc_response(request).encode()
            self.request.sendall(response)

        if request.path == "/public/image/eagle.jpg":
            response = self.eagle_response(request)
            self.request.sendall(response)

        if request.path == "/public/image/cat.jpg":
            response = self.cat_response(request)
            self.request.sendall(response)

        if request.path == "/public/image/dog.jpg":
            response = self.dog_response(request)
            self.request.sendall(response)
        
        if request.path == "/public/image/elephant-small.jpg":
            response = self.e_small_response(request)
            self.request.sendall(response)

        if request.path == "/public/image/elephant.jpg":
            response = self.e_response(request)
            self.request.sendall(response)
        
        if request.path == "/public/image/flamingo.jpg":
            response = self.flamingo_response(request)
            self.request.sendall(response)

        if request.path == "/public/image/kitten.jpg":
            response = self.kitten_response(request)
            self.request.sendall(response)

        if request.path == "/public/favicon.ico":
            response = self.favico_response(request)
            self.request.sendall(response)
        else:
            response = self.bad_responce(request).encode()
            self.request.sendall(response)





def main():
    host = "0.0.0.0"
    port = 8080

    socketserver.TCPServer.allow_reuse_address = True

    server = socketserver.TCPServer((host, port), MyTCPHandler)

    print("Listening on port " + str(port))

    # server.serve_forever()
    server.serve_forever()
    


if __name__ == "__main__":
    main()
