import socketserver
from util.request import Request
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import json
import html



class MyTCPHandler(socketserver.BaseRequestHandler):

    mongo_client = MongoClient("mongo")
    db = mongo_client["cse312"]
    chat_collection = db["chat"]
    message_id = 0
    count = 0


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
            body = body.replace("🙂", "&#128578;")
        

        
        bytes = len(body)
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
        return responce.encode()
        
    def recive_messaege(self,request):
        data = json.loads(request.body)
        print(data)
        data = html.escape(data["message"])
        temp = int(self.message_id) + 1 
        data = {"message": data,"username": "guest","id": temp}

        self.chat_collection.insert_one(data)

        data.pop("_id")

        body = json.dumps(data)
        bytes = len(body)
        
        responce = request.http_version
        responce += " 201 Created\r\n"
        responce +="Content-Type: application/json\r\n"
        responce += "X-Content-Type-Options: nosniff\r\n"

        responce +="Content-Length: " + str(bytes) + "\r\n\r\n"
        responce += body
        return responce.encode()
    
   

    def send_mesages(self,request):
        all_data = self.chat_collection.find({})
        body = []
        for entry in all_data:
            dict = {}
            dict["message"] = entry["message"]
            dict["username"] = entry["username"]
            dict["id"] = entry["id"]
            body.append(dict) 

        body = json.dumps(body)
        bytes = len(body)
        
        responce = request.http_version
        responce += " 200 OK\r\n"
        responce +="Content-Type: application/json\r\n"
        responce += "X-Content-Type-Options: nosniff\r\n"

        responce +="Content-Length: " + str(bytes) + "\r\n\r\n" + body
            
        return responce.encode()
    
    def check_message(self,request,id):
        message = self.chat_collection.find_one({"id": int(id)})
        
        if(message == None):
            return self.bad_responce(request)
        
        body = {}
        body["message"] = message["message"]
        body["username"] = message["username"]
        body["id"] = message["id"]

        body = json.dumps(body)
        bytes = len(body)
        
        responce = request.http_version
        responce += " 200 OK\r\n"
        responce +="Content-Type: application/json\r\n"
        responce += "X-Content-Type-Options: nosniff\r\n"

        responce +="Content-Length: " + str(bytes) + "\r\n\r\n" + body
            
        return responce.encode()
    
    def delete(self,request,id):
        message = self.chat_collection.find_one({"id": int(id)})

        if(message == None):
            return self.bad_responce(request)

        self.chat_collection.delete_one({"id": int(id)})

        responce = request.http_version
        responce += " 204 No Content\r\n"
        responce += "X-Content-Type-Options: nosniff\r\n"

        responce +="Content-Length: " + str(0) + "\r\n\r\n"
            
        return responce.encode()
    
    def update(self,request,id):
        message = self.chat_collection.find_one({"id": int(id)})
        print(f"ORINGINAL MESSAGE = {message}")

        if(message == None):
            return self.bad_responce(request)
        
        new_message = json.loads(request.body)
        print(f"what im getting from request = {new_message}")

        update = {
            "$set": {
            "message":html.escape(new_message["message"]),
            "username":html.escape(new_message["username"])
            }
        }
        self.chat_collection.update_one({"id":int(id)},update)

        message = self.chat_collection.find_one({"id": int(id)})
        print(f"NEW MESSAGE = {message}")

        message.pop("_id")

        body = json.dumps(message)
        bytes = len(body)
        
        responce = request.http_version
        responce += " 200 OK\r\n"
        responce +="Content-Type: application/json\r\n"
        responce += "X-Content-Type-Options: nosniff\r\n"

        responce +="Content-Length: " + str(bytes) + "\r\n\r\n"
        responce += body
        return responce.encode()

    
    def handle(self):
        all_data = list(MyTCPHandler.chat_collection.find({}))
        if(len(all_data)  > 0):
            temp = all_data[len(all_data)-1]
            self.message_id = int(temp["id"])
        else:
            self.message_id = 0
    


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

        # CODE TO TEST UPDATE
        # if self.count % 3 == 0:
        #     print("OVERING CODE TRYING TO UPDATE id 25")
        #     request = Request(b'PUT /chat-messages/25 HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\n\r\n{"message": "Welcome to CSE312!", "username": "Jesse"}')
        # self.count += 1

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
        if request.path == "/register":
            temp = request.method + request.path + request.http_version + str(request.headers) + str(request.cookies) + str(request.body)
            print(temp)
        if request.path == "/login":
            print(request)

        if request.path == "/chat-messages":
            if request.method == "POST":
                response = self.recive_messaege(request)
                self.request.sendall(response)
            if request.method == "GET":
                self.request.sendall(self.send_mesages(request))
        
        
        if request.path[:15] == "/chat-messages/":
            id = request.path[15:]
            if request.method == "GET":
                return  self.request.sendall(self.check_message(request,id))
            if request.method == "DELETE":
                return self.request.sendall(self.delete(request,id))
            if request.method == "PUT":
                return self.request.sendall(self.update(request,id))

        else:
            response = self.bad_responce(request)
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
