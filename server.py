import base64
import socketserver

import requests
from util.request import Request
from util.multipart import parse_multipart
import util.websockets
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import json
import html
from util.router import Router
import util.auth as Auth
import bcrypt
import hashlib
import secrets
import os

class MyTCPHandler(socketserver.BaseRequestHandler):

    router = Router()
    mongo_client = MongoClient("mongo")
    db = mongo_client["cse312"]
    chat_collection = db["chat"]
    accounts = db["accounts"]
    message_id = 0
    count = 0

    redirect_uri = os.getenv("REDIRECT_URI")
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    
    websocket_users = []



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

        if "auth_token" in request.cookies:
            token = request.cookies["auth_token"]
            hashed_token = hashlib.sha256(token.encode()).hexdigest()
            account = self.accounts.find_one({"hashed_token": hashed_token})
            if account != None:
                print("authenitcated account")
                #creating a new xsrf token if user does not have one
                if "xsrf_token" not in account:
                    print("account did not have token")
                    xsrf_token = secrets.token_hex(16)
                    self.accounts.update_one({"_id": account["_id"]}, {"$set": {"xsrf_token": xsrf_token}})
                # if user has an xsrf token
                else:
                    print("account did have token")
                    xsrf_token = account["xsrf_token"]
                # injecting token into html
                body = body.replace("{{INSERT TOKEN}}", xsrf_token)
                
                # channging visability of login buttons
                index = body.find('"/login"') + len('"/login"')
                body = body[:index] + " hidden " + body[index:]
                index = body.find('"/register"') + len('"/register"')
                body = body[:index] + " hidden " + body[index:]
                index = body.find('"/spotify"') + len('"/spotify"')
                body = body[:index] + " hidden " + body[index:]
        else:
            print("no valid auth token")
            index = body.find('"/logout"') + len('"/logout"')
            body = body[:index] + " hidden " + body[index:]


                
        

        
        bytes = len(body)
        responce +="Content-Length: " + str(bytes) + "\r\n\r\n" + body
        responce = responce.encode()
        return responce
    
    def image_response(self,request):

        file_name = request.path[14:]
        print(file_name)
        file_name = file_name.replace("/","")
        file_extension = file_name.split(".")[1]
        name = os.path.join("public", "image", file_name)
        content_types = {
            "jpg" : "image/jpeg",
            "gif": "image/gif",
            "png": "image/png",
            "mp4": "video/mp4",
        }
        content_type = ""
        for file_type in content_types.keys():
            if file_extension == file_type:
                content_type = content_types[file_type]

        try:       
            with open(name, "rb") as file:
                data = file.read()
                bytes = len(data)
                body = data
            print("file sucess")
            responce = request.http_version
            responce += " 200 OK\r\n"
            
            responce +="Content-Type: " + content_type + "\r\n"
            responce += "X-Content-Type-Options: nosniff\r\n"
            responce +="Content-Length: " + str(bytes) + "\r\n\r\n"
            responce = responce.encode()
            responce += body
            return responce
        except:
            return self.bad_responce(request)

    
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
        return responce.encode()
    
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
        return responce.encode()
    
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
        return responce.encode()
    
    def bad_responce(self,request):
        responce = request.http_version
        responce += " 404 Not Found\r\n"
        responce +="Content-Type: text/plain\r\n"
        responce += "X-Content-Type-Options: nosniff\r\n"
        body = "The requested content does not exist"
        bytes = len(body)
        responce +="Content-Length: " + str(bytes) + "\r\n\r\n" + body
        return responce.encode()
    
    def forbiden_response(self,request):
        responce = request.http_version
        responce += " 403 Forbidden\r\n"
        responce +="Content-Type: text/plain\r\n"
        responce += "X-Content-Type-Options: nosniff\r\n"
        body = "Forbiden action"
        bytes = len(body)
        responce +="Content-Length: " + str(bytes) + "\r\n\r\n" + body
        return responce.encode()
       

    def recive_messaege(self,request):
        data = json.loads(request.body)
        xsrf_token = data.get("xsrf_token")
        username = "guest"
        data = html.escape(data["message"])
        if "auth_token" in request.cookies:
            token = request.cookies["auth_token"]
            hashed_token = hashlib.sha256(token.encode()).hexdigest()
            account = self.accounts.find_one({"hashed_token": hashed_token})
            if account != None:
                if account["xsrf_token"] == xsrf_token:
                    username = account["username"]
                    if "access_token" in account:
                        data += self.get_music(account["access_token"])
                else:
                    return self.forbiden_response(request)
        temp = int(self.message_id) + 1 
        data = {"message": data,"username": username,"id": temp}

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
    
    def check_message(self,request):
        id = request.path[15:]
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
    
    def delete(self,request):
        id = request.path[15:]
        message = self.chat_collection.find_one({"id": int(id)})

        if(message == None):
            return self.bad_responce(request)

        username = "guest"
        if "auth_token" in request.cookies:
            token = request.cookies["auth_token"]
            hashed_token = hashlib.sha256(token.encode()).hexdigest()
            account = self.accounts.find_one({"hashed_token": hashed_token})
            username = account["username"]
        temp = message["username"]
        print(f"current user = {username}, message belongs to {temp}")
        if username == message["username"]:
            print("message should be deleted")
            self.chat_collection.delete_one({"id": int(id)})
            responce = request.http_version
            responce += " 204 No Content\r\n"
            responce += "X-Content-Type-Options: nosniff\r\n"
            responce +="Content-Length: " + str(0) + "\r\n\r\n" 
            return responce.encode()
        else:
            print("invalid delete should give me a 403")
            return self.forbiden_response(request)
 
    def update(self,request):
        id = request.path[15:]
        message = self.chat_collection.find_one({"id": int(id)})

        if(message == None):
            return self.bad_responce(request)
        
        new_message = json.loads(request.body)

        update = {
            "$set": {
            "message":html.escape(new_message["message"]),
            "username":html.escape(new_message["username"])
            }
        }
        self.chat_collection.update_one({"id":int(id)},update)

        message = self.chat_collection.find_one({"id": int(id)})

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

    def register(self,request):
        creds = Auth.extract_credentials(request)
        if Auth.validate_password(creds[1]) == True:
            bytes = creds[1].encode('utf-8')
            salt = bcrypt.gensalt()
            hash = bcrypt.hashpw(bytes,salt)
            data = {"username": creds[0],"salt": salt, "hash": hash}
            self.accounts.insert_one(data)
            responce = request.http_version
            responce += " 302 Found redirect\r\n"
            responce +="Content-Type: text/html\r\n"
            responce += "X-Content-Type-Options: nosniff\r\n"
            responce +="Content-Length: 0" + "\r\n"
            responce += "Location: /\r\n\r\n"
            return responce.encode()
        else:
            return self.bad_responce(request)
         
    def login(self,request):
        creds = Auth.extract_credentials(request)
        account = self.accounts.find_one({"username": creds[0]})
        if account == None:
            return self.bad_responce(request)
        else:
            bytes = creds[1].encode('utf-8')
            salt = account["salt"]
            hash = bcrypt.hashpw(bytes,salt)
            if(hash == account["hash"]):
                token = secrets.token_hex(16)
                hashed_token = hashlib.sha256(token.encode()).hexdigest()
                self.accounts.update_one({"_id": account["_id"]}, {"$set": {"hashed_token": hashed_token}})
                responce = request.http_version
                responce += " 302 Found redirect\r\n"
                responce +="Content-Type: text/html\r\n"
                responce += "X-Content-Type-Options: nosniff\r\n"
                responce +="Content-Length: 0" + "\r\n"
                responce += "Set-Cookie: auth_token=" + str(token) + "; Max-Age=3600; HttpOnly\r\n"
                responce += "Location: /\r\n\r\n"
                return responce.encode()
            else:
                return self.bad_responce(request)
        
    def logout(self,request):
        if "auth_token" in request.cookies:
            token = request.cookies["auth_token"]
            hashed_token = hashlib.sha256(token.encode()).hexdigest()
            self.accounts.update_one({"hashed_token": hashed_token}, {"$unset": {"hashed_token": ""}})

        response = request.http_version + " 302 Found redirect\r\n"
        response += "Content-Type: text/html\r\n"
        response += "X-Content-Type-Options: nosniff\r\n"
        response += "Content-Length: 0" + "\r\n"
        response += "Set-Cookie: auth_token=; Max-Age=0; HttpOnly\r\n"
        response += "Location: /\r\n\r\n"  
        return response.encode()

    def login_with_spotify(self,request):
        authorization_url = 'https://accounts.spotify.com/authorize?'
        authorization_params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.redirect_uri,
            'scope': 'user-read-email user-read-private user-read-currently-playing'
        }
        url = requests.get(authorization_url,authorization_params).url

        responce = request.http_version + " 302 Found redirect\r\n"
        responce +="Content-Type: text/html\r\n"
        responce += "X-Content-Type-Options: nosniff\r\n"
        responce +="Content-Length: 0" + "\r\n"
        responce += "Location: " + url + "\r\n\r\n"
        return responce.encode()
    
    def extract_code(self, request):
        authorization_code = request.path[14:]
        
        auth_header = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()

        # Request body parameters
        data = {
            'grant_type': "authorization_code",
            'code': authorization_code,
            'redirect_uri': self.redirect_uri
        }

        # Request headers
        headers = {
            'Authorization': f'Basic {auth_header}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        # POST request
        response = requests.post('https://accounts.spotify.com/api/token', data=data, headers=headers)

        
        
        access_token = json.loads(response.text)["access_token"]
        if access_token != None:
            email = self.get_email(access_token)
        
        account = self.accounts.find_one({"username": email})
        token = secrets.token_hex(16)
        hashed_token = hashlib.sha256(token.encode()).hexdigest()
        if account == None:
            print("creating account with spotify")
            data = {"username": email, "access_token": access_token, "hashed_token": hashed_token}
            self.accounts.insert_one(data)
            
        else:
            print("account with spotify exists")
            self.accounts.update_one({"_id": account["_id"]}, {"$set": {"access_token": access_token, "hashed_token" : hashed_token}})


        responce = request.http_version
        responce += " 302 Found redirect\r\n"
        responce +="Content-Type: text/html\r\n"
        responce += "X-Content-Type-Options: nosniff\r\n"
        responce +="Content-Length: 0" + "\r\n"
        responce += "Set-Cookie: auth_token=" + str(token) + "; Max-Age=3600; HttpOnly\r\n"
        responce += "Location: /\r\n\r\n"
        return responce.encode()
    
               
    def get_email(self, access_token):
        profile_url = 'https://api.spotify.com/v1/me'

        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(profile_url, headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            email = user_data.get('email')
            return email
        else:
            print(f"Error retrieving user email: {response.status_code} - {response.text}")
            return None

    def get_music(self, access_token):
        url = 'https://api.spotify.com/v1/me/player/currently-playing'

        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(url, headers=headers)

        string = " (Currently listening to: Nothing)"
        if response.status_code == 200:
            data = response.json()
            if data.get('is_playing'):
                song = data['item']['name']
                artist = data['item']['artists'][0]['name']
                string = " (Currently listening to: " + str(song) + " by " + str(artist)+ ")"
        
        return string

    def get_filetype(self,part):
        image_signatures = {
        b'\xff\xD8\xff': "image/jpg",
        b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a': "image/png",
        b'\x47\x49\x46\x38\x37\x61': "image/gif",
        b'\x47\x49\x46\x38\x39\x61': "image/gif",
        }
        mp4_signature1 = b'\x00\x00\x00'
        for signature in image_signatures.keys():
            if part.content.startswith(signature):
                return(image_signatures[signature])
        if part.content.startswith(mp4_signature1):
            return "video/mp4"
    
        
        return None

        

    def upload(self, request):
        length = int(request.headers["Content-Length"])
        while len(request.body) < length:
            received_data = self.request.recv(4096)
            request.body += received_data

        multipart_data = parse_multipart(request)


        part = multipart_data.parts[0]
        

        signature = self.get_filetype(part).split("/")
        format = signature[0]
        filetype = signature[1]
        
        if part:
            image_directory = os.path.join("public", "image")
            
            image_content = part.content
            image_count = len(os.listdir(image_directory))
            image_filename = f"{format}{image_count + 1}.{filetype}"
            
            
            if(format == "image"):
                with open(os.path.join(image_directory, image_filename), "wb") as f:
                    f.write(image_content)
                data = '<img width="400" src="' + os.path.join(image_directory, image_filename) +'" alt="Image">'
            
            if format == "video":
                with open(os.path.join(image_directory, image_filename), "wb") as f:
                    f.write(image_content)
                data = '<video width="400" controls autoplay muted><source src="' + os.path.join(image_directory, image_filename) +'" type="video/mp4"></video>'
            username = "guest"
            if "auth_token" in request.cookies:
                token = request.cookies["auth_token"]
                hashed_token = hashlib.sha256(  token.encode()).hexdigest()
                account = self.accounts.find_one({"hashed_token": hashed_token})
                if account != None:
                    username = account["username"]
            temp = int(self.message_id) + 1 
            data = {"message": data,"username": username,"id": temp}

            self.chat_collection.insert_one(data)

            data.pop("_id")
            
            responce = request.http_version
            responce += " 302 Found redirect\r\n"
            responce +="Content-Type: text/html\r\n"
            responce += "X-Content-Type-Options: nosniff\r\n"
            responce +="Content-Length: 0" + "\r\n"
            responce += "Location: /\r\n\r\n"
            return responce.encode()

            
    def handshake(self, request):
        username = "Guest"
        if "auth_token" in request.cookies:
            token = request.cookies["auth_token"]
            hashed_token = hashlib.sha256(token.encode()).hexdigest()
            account = self.accounts.find_one({"hashed_token": hashed_token})
            if account != None:
                username = account["username"]

        
        print(request)
        key = request.headers["Sec-WebSocket-Key"]
        key = util.websockets.compute_accept(key)
        
        responce = request.http_version
        responce += " 101 Switching Protocols\r\n"
        responce +="Connection: Upgrade\r\n"
        responce +="Upgrade: websocket\r\n"
        responce +=f"Sec-WebSocket-Accept: {key}\r\n"
        responce += "X-Content-Type-Options: nosniff\r\n\r\n"
        self.request.sendall(responce.encode())
        self.websocket_users.append(self.request)
        if username != "Guest":
            for users in self.websocket_users:
                login_msg = {}
                login_msg["messageType"] = "logon"
                login_msg["username"] = username
                login_msg = json.dumps(login_msg)
                frame = util.websockets.generate_ws_frame(login_msg.encode())
                users.sendall(frame)
            

        self.websocket_loop(request,username)



    def websocket_loop(self,request, username):
        extra_data = b""
        while True:
            bytes_read = 0
            received_data = extra_data
            received_data += self.request.recv(2048)
            bytes_read += 2048

            is_end = False
            final = b""
            
            while not is_end:
                frame = util.websockets.parse_ws_frame(received_data)
                opcode = frame.opcode

                if opcode == 0x08:
                    self.websocket_users.remove(self.request)
                    if(username != "Guest"):
                        for users in self.websocket_users:
                            login_msg = {}
                            login_msg["messageType"] = "logout"
                            login_msg["username"] = username
                            login_msg = json.dumps(login_msg)
                            frame = util.websockets.generate_ws_frame(login_msg.encode())
                            users.sendall(frame)
                    return()

                fin = frame.fin_bit
                length = frame.payload_length
                payload = frame.payload
                if frame.opcode == 0x8:
                    self.websocket_users.remove(self.request)
                    break

                # this is where we buffer
                if bytes_read < len(payload):
                    while len(payload) < length:
                        additional_data = self.request.recv(2048)
                        bytes_read += 2048
                        received_data += (additional_data)
                        frame = util.websockets.parse_ws_frame(received_data)
                        fin = frame.fin_bit
                        length = frame.payload_length
                        payload = frame.payload
                    
                    # we read too much and we have to save
                frameLength = length + 6 # To account for the first few headers
                if frameLength >= 126 and frameLength < 65536:
                    frameLength += 2
                elif frameLength >= 65536:
                    frameLength += 6

                if bytes_read > (frameLength):
                    print(f"frame length = {frameLength}")
                    print(f"recived data = {received_data}")
                    extra_data = received_data[frameLength:]
                    print(f"extra data = {extra_data}")
                
                print(f"payload : {payload}")

                final += payload
                if(fin == 1):
                    is_end = True
            
            decoded = final.decode()
            dict = json.loads(decoded.replace("'", '"'))
            if dict.get('messageType') == "chatMessage":
                self.ws_send_mesage(dict,username)

            message_type = dict.get('messageType')
            message = dict.get('message')
            print(f"message = {message}")
            print(f"messsage type = {message_type}")
            print(f"username = {username}")


    def ws_send_mesage(self,dict,username):
        message = html.escape(dict.get('message'))
        all_data = list(MyTCPHandler.chat_collection.find({}))
        if(len(all_data)  > 0):
            temp = all_data[len(all_data)-1]
            self.message_id = int(temp["id"])
        else:
            self.message_id = 0

        temp = int(self.message_id) + 1 
        data = {"message": message,"username": username,"id": temp}

        self.chat_collection.insert_one(data)

        data.pop("_id")

        dict = {}
        dict["messageType"] = "chatMessage"
        dict["username"] = username
        dict["message"] = message
        dict["id"] = temp
        dict = json.dumps(dict)
        frame = util.websockets.generate_ws_frame(dict.encode())

        for users in self.websocket_users:
            print(f"{message} sent to {users}")
            users.sendall(frame)
                    

    def handle(self):
        self.setup_router()
        all_data = list(MyTCPHandler.chat_collection.find({}))
        if(len(all_data)  > 0):
            temp = all_data[len(all_data)-1]
            self.message_id = int(temp["id"])
        else:
            self.message_id = 0

        received_data = self.request.recv(2048)
        request = Request(received_data)
        print("--- PATH REQUESTED ---")
        print(f"{request.method} {request.path}")
        if request.path == "/websocket":
            self.handshake(request)
        else:
            self.request.sendall(self.router.route_request(request))
    




    def setup_router(self):
        self.router = Router()
        self.router.add_route("GET","^/$",self.root_response)
        self.router.add_route("GET","^/public/style.css$",self.css_response)
        self.router.add_route("GET","^/public/functions.js$",self.js_response)
        self.router.add_route("GET","^/public/webrtc.js$",self.webrtc_response)
        self.router.add_route("GET","^/public/image/.*$",self.image_response)
        self.router.add_route("GET","^/public/favicon.ico$",self.favico_response)
        self.router.add_route("GET","^/chat-messages$",self.send_mesages)
        self.router.add_route("POST","^/chat-messages$",self.recive_messaege)
        self.router.add_route("POST","^/chat-messages/$",self.recive_messaege)
        self.router.add_route("GET","^/chat-messages/.$",self.check_message)
        self.router.add_route("DELETE","^/chat-messages/.*$",self.delete)
        self.router.add_route("PUT","^/chat-messages/.$",self.update)
        self.router.add_route("POST","^/register$",self.register)
        self.router.add_route("POST","^/login$",self.login)
        self.router.add_route("POST","^/logout$",self.logout)
        self.router.add_route("POST","^/spotify$",self.login_with_spotify)
        self.router.add_route("GET","^/spotify?.*$",self.extract_code)
        self.router.add_route("POST","^/upload$",self.upload)

    



def main():
    host = "0.0.0.0"
    port = 8080    
    

    socketserver.TCPServer.allow_reuse_address = True
    # MyTCPHandler.setup_router(MyTCPHandler)
    

    server = socketserver.ThreadingTCPServer((host, port), MyTCPHandler)

    print("Listening on port " + str(port))

    

    # server.serve_forever()
    server.serve_forever()
    


if __name__ == "__main__":
    main()
