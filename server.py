import base64
import socketserver

import requests
from util.request import Request
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import json
import html
from util.router import Router
import util.auth as Auth
import bcrypt
import hashlib
import secrets
import urllib
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
                print(f"XSRF TOKEN = {xsrf_token}")
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
        print("image called")
        responce = request.http_version
        responce += " 200 OK\r\n"
        responce +="Content-Type: image/jpeg\r\n"
        responce += "X-Content-Type-Options: nosniff\r\n"
        print(request.path)
        file_name = request.path[14:]
        print(file_name)
        name = "public/image/" + file_name
        with open(name, "rb") as file:
            data = file.read()
            bytes = len(data)
            body = data
        responce +="Content-Length: " + str(bytes) + "\r\n\r\n"
        responce = responce.encode()
        responce += body
        return responce

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
        print(request.cookies)
        data = json.loads(request.body)
        print(data)
        xsrf_token = data.get("xsrf_token")
        print(f"XSRF TOKEN??? = {xsrf_token}")
        username = "guest"
        if "auth_token" in request.cookies:
            token = request.cookies["auth_token"]
            hashed_token = hashlib.sha256(token.encode()).hexdigest()
            account = self.accounts.find_one({"hashed_token": hashed_token})
            if account != None:
                if account["xsrf_token"] == xsrf_token:
                    username = account["username"]
                else:
                    return self.forbiden_response(request)
        print(account)
        data = html.escape(data["message"]) 
        if account["access_token"] != None:
            data += self.get_music(account["access_token"])
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
        print("DELETE WAS CALLED")
        id = request.path[15:]
        print(id)
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

            # responce = request.http_version
            # responce += " 403 Forbidden\r\n"
            # responce +="Content-Type: text/plain\r\n"
            # responce += "X-Content-Type-Options: nosniff\r\n"
            # body = "You cannot delete somone else message"
            # bytes = len(body)
            # responce +="Content-Length: " + str(bytes) + "\r\n\r\n" + body
            # return responce.encode()
 
    def update(self,request):
        id = request.path[15:]
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

    def register(self,request):
        creds = Auth.extract_credentials(request)
        print(creds)
        if Auth.validate_password(creds[1]) == True:
            bytes = creds[1].encode('utf-8')
            salt = bcrypt.gensalt()
            hash = bcrypt.hashpw(bytes,salt)
            print(hash)
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
        print(account)
        if account == None:
            return self.bad_responce(request)
        else:
            bytes = creds[1].encode('utf-8')
            salt = account["salt"]
            hash = bcrypt.hashpw(bytes,salt)
            print(str(hash))
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
        print("--------")
        print("EXTRACT CODE CALLED")
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

        
        
        print(response)
        access_token = json.loads(response.text)["access_token"]
        print(f"token = {access_token}")
        if access_token != None:
            email = self.get_email(access_token)
        
        account = self.accounts.find_one({"username": email})
        print(account)
        token = secrets.token_hex(16)
        hashed_token = hashlib.sha256(token.encode()).hexdigest()
        if account == None:
            print("creating account with spotify")
            data = {"username": email, "access_token": access_token, "hashed_token": hashed_token}
            self.accounts.insert_one(data)
            
        else:
            print("account with spotify exists")
            self.accounts.update_one({"_id": account["_id"]}, {"$set": {"access_token": access_token, "hashed_token" : hashed_token}})

        print(account)

        responce = request.http_version
        responce += " 302 Found redirect\r\n"
        responce +="Content-Type: text/html\r\n"
        responce += "X-Content-Type-Options: nosniff\r\n"
        responce +="Content-Length: 0" + "\r\n"
        responce += "Set-Cookie: auth_token=" + str(token) + "; Max-Age=3600; HttpOnly\r\n"
        responce += "Location: /\r\n\r\n"
        return responce.encode()
    
               
    def get_email(self, access_token):
        # Spotify user profile endpoint
        profile_url = 'https://api.spotify.com/v1/me'

        # Request headers with the access token
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        # Make the request to Spotify API
        response = requests.get(profile_url, headers=headers)

        # Check if request was successful
        if response.status_code == 200:
            # Parse the response to extract user data, including email
            user_data = response.json()
            email = user_data.get('email')
            return email
        else:
            # Handle errors gracefully
            print(f"Error retrieving user email: {response.status_code} - {response.text}")
            return None

    def get_music(self, access_token):
        url = 'https://api.spotify.com/v1/me/player/currently-playing'

        # Request headers
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        # Make GET request to Spotify API
        response = requests.get(url, headers=headers)

        # Check if request was successful
        print(response.text)
        string = " (Currently listening to: Nothing)"
        if response.status_code == 200:
            # Parse JSON response into a dictionary
            data = response.json()

            # Check if the user is currently playing a track
            if data.get('is_playing'):
                # Extract information about the currently playing track
                song = data['item']['name']
                artist = data['item']['artists'][0]['name']
                string = " (Currently listening to: " + str(song) + " by " + str(artist)+ ")"
        
        return string


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
        # TODO: Parse the HTTP request and use self.request.sendall(response) to send your response
        print("--- PATH REQUESTED ---")
        print(f"{request.method} {request.path}")
        self.request.sendall(self.router.route_request(request))


        # CODE TO TEST UPDATE
        # if self.count % 3 == 0:
        #     print("OVERING CODE TRYING TO UPDATE id 25")
        #     request = Request(b'PUT /chat-messages/25 HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\n\r\n{"message": "Welcome to CSE312!", "username": "Jesse"}')
        # self.count += 1



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
        self.router.add_route("GET","^/chat-messages/.$",self.check_message)
        self.router.add_route("DELETE","^/chat-messages/.*$",self.delete)
        self.router.add_route("PUT","^/chat-messages/.$",self.update)
        self.router.add_route("POST","^/register$",self.register)
        self.router.add_route("POST","^/login$",self.login)
        self.router.add_route("POST","^/logout$",self.logout)
        self.router.add_route("POST","^/spotify$",self.login_with_spotify)
        self.router.add_route("GET","^/spotify?.*$",self.extract_code)



def main():
    host = "0.0.0.0"
    port = 8080    
    

    socketserver.TCPServer.allow_reuse_address = True
    # MyTCPHandler.setup_router(MyTCPHandler)
    

    server = socketserver.TCPServer((host, port), MyTCPHandler)

    print("Listening on port " + str(port))

    

    # server.serve_forever()
    server.serve_forever()
    


if __name__ == "__main__":
    main()
