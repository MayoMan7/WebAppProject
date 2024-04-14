import socketserver
from util.request import Request
from util.router import Router
from util.auth import *
from util.multipart import *
from util.websockets import *
from pymongo import MongoClient
import json
import bcrypt
import secrets
import hashlib
import requests
import os
import base64
#import ffmpeg
#import subprocess

mongo_client = MongoClient("mongo")
db = mongo_client["cse312"]
chat_collection = db["chat"]
login_collection = db["logins"]
socket_connections = []
socket_users = {}

router = Router()
def fileSize(path):
    # Open File (read bytes) & Get a List of All Lines of the File
    file = open(path, 'rb')
    list = file.readlines()
    # Read each line and get the length of the bytes
    size = 0 
    for i in range(0, len(list)):
        size += len(list[i])
    # Close File & Return the Size
    file.close() 
    return str(size)

def fileString(path):
    # Open the file 
    file = open(path, 'rb')
    # Get all contents in String
    text = file.read()
    # Close File & Return the Size
    file.close()
    return text
    
def createString(version, code, dict, path):
    # Create String, Add HTTP Version & Response Code
    response = str(version) + " " + str(code)
    if (code == 200):
        response += " OK\r\n"
    elif (code == 404):
        response += " Not Found\r\n"

    # For every header, Add to String
    for key in dict:
        response += key + ": " + dict[key] + "\r\n"
        
    response += "\r\n"
    response = response.encode()
    response += fileString(path)
    return response
    
def escapeHTML(message: str):
    # From Lecture Example HTML Injection Attacks :D
    return message.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def serve_root(request: Request):
    headerDict = { }
    response = ""
    headerDict["Content-Type"] = "text/html; charset=utf-8"
    headerDict["Content-Length:"] = fileSize('public/index.html')
    headerDict["X-Content-Type-Options"] = "nosniff"

    # Handle cookies
    if "visits" not in request.cookies:
        headerDict["Set-Cookie"] = "visits=1; Max-Age=3600"
    else:
        headerDict["Set-Cookie"] = "visits=" + (str(int(request.cookies['visits']) + 1) + "; Max-Age=3600")
    
    response = createString(request.http_version, 200, headerDict, 'public/index.html')

    # Changes HTML for the visits counter
    if "visits" not in request.cookies:
        response = response.replace(b"{{visits}}", b'1')
    else:
        response = response.replace(b"{{visits}}", str(int(request.cookies['visits']) + 1).encode())

    # Changes HTML to have login/register and the logout interchange
    if "token" not in request.cookies.keys() or request.cookies["token"] == "":
        index = response.find(b'"/logout"') + 9
        response = response[:index] + b" hidden" + response[index:]
        response = response.replace(b'Logout:', b'')
    else:
        indexRegister = response.find(b'"/register"') + 11
        indexLogin = response.find(b'"/login"') + 8
        indexSpot = response.find(b'"/spotify"') + 10
        response = response[:indexRegister] + b" hidden" + response[indexRegister:indexLogin] + b" hidden" + response[indexLogin:indexSpot] + b" hidden" + response[indexSpot:]
        response = response.replace(b'Register:', b'').replace(b'Login:', b'').replace(b'Login with Spotify:', b'')

    # XSRF Token
    if "token" in request.cookies.keys():
        login = login_collection.find_one({"authtoken": hashlib.sha256(request.cookies["token"].encode()).hexdigest()})
        # If there is a user is auth then check if there is xsrf token with his login
        if login:
            if "xsrf" not in login.keys() or response.find(b'""'):
                token = secrets.token_urlsafe(24)
                # If user doesn't have one add it into their HTML
                index = response.find(b'"xsrf_token"') + 12
                response = response[:index] + ' value="'.encode() + token.encode() + '" '.encode() + response[index+10:]

                dict = {
                    "username": login["username"],
                    "salt": login["salt"],
                    "hash": login["hash"],
                    "authtoken": login["authtoken"],
                    "xsrf": token
                }
                # Update the DB
                login_collection.update_one({"username": login["username"]}, {"$set": dict})

    # print(response)
    return response

def serve_funcjs(request: Request):
    headerDict = { }
    response = ""

    headerDict["Content-Type"] = "text/javascript; charset=utf-8"
    headerDict["Content-Length:"] = fileSize('public/functions.js')
    headerDict["X-Content-Type-Options"] = "nosniff"
    response = createString(request.http_version, 200, headerDict, 'public/functions.js')
    
    return response
def serve_css(request: Request):
    headerDict = { }
    response = ""

    headerDict["Content-Type"] = "text/css; charset=utf-8"
    headerDict["Content-Length:"] = fileSize('public/style.css')
    headerDict["X-Content-Type-Options"] = "nosniff"
    response = createString(request.http_version, 200, headerDict, 'public/style.css')
    
    return response
def serve_favicon(request: Request):
    headerDict = { }
    response = ""

    headerDict["Content-Type"] = "image/ico"
    headerDict["Content-Length:"] = fileSize('public/favicon.ico')
    headerDict["X-Content-Type-Options"] = "nosniff"
    response = createString(request.http_version, 200, headerDict, 'public/favicon.ico')
    
    return response
def serve_webjs(request: Request):
    headerDict = { }
    response = ""

    headerDict["Content-Type"] = "text/javascript"
    headerDict["Content-Length:"] = fileSize('public/webrtc.js')
    headerDict["X-Content-Type-Options"] = "nosniff"
    response = createString(request.http_version, 200, headerDict, 'public/webrtc.js')
    
    return response
def serve_eagle(request: Request):
    headerDict = { }
    response = ""

    headerDict["Content-Type"] = "image/jpg"
    headerDict["Content-Length:"] = fileSize('public/image/eagle.jpg')
    headerDict["X-Content-Type-Options"] = "nosniff"
    response = createString(request.http_version, 200, headerDict, 'public/image/eagle.jpg')
    
    return response
def serve_cat(request: Request):
    headerDict = { }
    response = ""

    headerDict["Content-Type"] = "image/jpg"
    headerDict["Content-Length:"] = fileSize('public/image/cat.jpg')
    headerDict["X-Content-Type-Options"] = "nosniff"
    response = createString(request.http_version, 200, headerDict, 'public/image/cat.jpg')
    
    return response
def serve_dog(request: Request):
    headerDict = { }
    response = ""

    headerDict["Content-Type"] = "image/jpg"
    headerDict["Content-Length:"] = fileSize('public/image/dog.jpg')
    headerDict["X-Content-Type-Options"] = "nosniff"
    response = createString(request.http_version, 200, headerDict, 'public/image/dog.jpg')
    
    return response
def serve_elephantS(request: Request):
    headerDict = { }
    response = ""

    headerDict["Content-Type"] = "image/jpg"
    headerDict["Content-Length:"] = fileSize('public/image/elephant-small.jpg')
    headerDict["X-Content-Type-Options"] = "nosniff"
    response = createString(request.http_version, 200, headerDict, 'public/image/elephant-small.jpg')
    
    return response
def serve_elephant(request: Request):
    headerDict = { }
    response = ""

    headerDict["Content-Type"] = "image/jpg"
    headerDict["Content-Length:"] = fileSize('public/image/elephant.jpg')
    headerDict["X-Content-Type-Options"] = "nosniff"
    response = createString(request.http_version, 200, headerDict, 'public/image/elephant.jpg')
    
    return response
def serve_flamingo(request: Request):
    headerDict = { }
    response = ""

    headerDict["Content-Type"] = "image/jpg"
    headerDict["Content-Length:"] = fileSize('public/image/flamingo.jpg')
    headerDict["X-Content-Type-Options"] = "nosniff"
    response = createString(request.http_version, 200, headerDict, 'public/image/flamingo.jpg')
    
    return response
def serve_kitten(request: Request):
    headerDict = { }
    response = ""

    headerDict["Content-Type"] = "image/jpg"
    headerDict["Content-Length:"] = fileSize('public/image/kitten.jpg')
    headerDict["X-Content-Type-Options"] = "nosniff"
    response = createString(request.http_version, 200, headerDict, 'public/image/kitten.jpg')
    
    return response

def serve_chatPost(request: Request):
    response = ""

    jsonString = json.loads(request.body.decode())
    idNum = 0
    all_data = list(chat_collection.find({}))
    if len(all_data) == 0:
        idNum = 1
    else:
        idNum = len(all_data) + 1
    
    authToken = ""
    if "token" in request.cookies.keys():
        authToken = hashlib.sha256(request.cookies["token"].encode()).hexdigest()

    collection = login_collection.find_one({"authtoken": authToken}, {"username": 1, "salt": 1, "hash": 1, "authtoken": 1, "xsrf": 1, "accesstoken": 1, "_id": 0})
    dict = { }
    if collection:
        userXSRF = jsonString["xsrf_token"]
        if "authtoken" in collection and "xsrf" in collection and collection["authtoken"] == authToken and collection["xsrf"] == userXSRF:
            if "accesstoken" in collection and collection["accesstoken"]:
                profile = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers={'Authorization': 'Bearer ' + collection["accesstoken"]})
                print(profile.status_code)
                
                if profile.status_code != 204 or profile.status_code >= 400:
                    print(profile.json())
                    profile = profile.json()
                    
                    # print(song)
                    if "item" in profile and profile["is_playing"]:
                        song = profile["item"]
                        
                        dict = {
                            "message": escapeHTML(jsonString["message"]) + " (Listening to " + song["name"] + " by " + song["artists"][0]["name"] + ")",
                            "username": collection["username"],
                            "id": str(idNum)
                        }
                    else:
                        dict = {
                            "message": escapeHTML(jsonString["message"]) + " (Listening to Nothing)",
                            "username": collection["username"],
                            "id": str(idNum)
                        }
                else:
                    dict = {
                    "message": escapeHTML(jsonString["message"]),
                    "username": collection["username"],
                    "id": str(idNum)
                    }
            else: 
                dict = {
                    "message": escapeHTML(jsonString["message"]),
                    "username": collection["username"],
                    "id": str(idNum)
                }
        else: 
            response = request.http_version
            response += " 403 Forbidden\r\n"
            response += "Content-Type: text/plain\r\n"
            response += "Content-Length: 0" + "\r\n"
            response += "X-Content-Type-Options: nosniff\r\n\r\n"
            response = response.encode()
            return response
    else:
        dict = {
            "message": escapeHTML(jsonString["message"]),
            "username": "Guest",
            "id": str(idNum)
        }

    chat_collection.insert_one(dict)         
    temp = chat_collection.find_one({"id":str(idNum)}, {"_id":0, "message": 1, "username": 1, "id": 1})
    msg = str(json.dumps(temp))
    response += request.http_version
    response += " 201 Created\r\n"
    response += "Content-Type: application/json\r\n"
    response += "Content-Length: " + str(len(msg)) + "\r\n"
    response += "X-Content-Type-Options: nosniff\r\n\r\n"
    response += msg
    response = response.encode()
    return response
def serve_chatGet(request: Request):
    response = ""
    all_data = list(chat_collection.find({}, {"_id":0, "message": 1, "username": 1, "id": 1}))
    msg = json.dumps(all_data)
    response += request.http_version
    response += " 200 OK\r\n"
    response += "Content-Type: application/json\r\n"
    response += "Content-Length: " + str(len(msg)) + "\r\n"
    response += "X-Content-Type-Options: nosniff\r\n\r\n"
    response += msg
    response = response.encode() 
    return response

def serve_chatPut(request: Request):
    response = ""
    look_id = request.path[15:]
    collection = chat_collection.find_one({"id":look_id}, {"_id":0, "message": 1, "username": 1, "id": 1})
    if collection is not None:
        jsonString = json.loads(request.body.decode())
        
        dict = {
            "message": escapeHTML(jsonString["message"]),
            "username": escapeHTML(jsonString["username"]),
            "id": str(look_id)
        }
        chat_collection.update_one({"id": look_id}, {"$set": dict})
        collection = chat_collection.find_one({"id":look_id}, {"_id":0, "message": 1, "username": 1, "id": 1})
        collection = json.dumps(collection)
        response += request.http_version
        response += " 200 OK\r\n"
        response += "Content-Type: application/json\r\n"
        response += "Content-Length: " + str(len(str(collection))) + "\r\n"
        response += "X-Content-Type-Options: nosniff\r\n\r\n"
        response += str(collection)
        response = response.encode()
    else:
        errorMsg = "The requested id does not exist"
        response = request.http_version + " 404 Not Found\r\n"
        response += "Content-Type: text/plain\r\n"
        response += "Content-Length: " + str(len(errorMsg)) + "\r\n"
        response += "X-Content-Type-Options: nosniff\r\n\r\n"
        response += errorMsg
        response = response.encode()
    return response
def serve_chatGetIndividual(request: Request):
    response = ""
    look_id = request.path[15:]
    collection = chat_collection.find_one({"id":look_id}, {"_id":0, "message": 1, "username": 1, "id": 1})
    
    if collection is not None:
        collection = json.dumps(collection)
        response += request.http_version
        response += " 200 OK\r\n"
        response += "Content-Type: application/json\r\n"
        response += "Content-Length: " + str(len(str(collection))) + "\r\n"
        response += "X-Content-Type-Options: nosniff\r\n\r\n"
        response += str(collection)
        response = response.encode()
    else:
        errorMsg = "The requested id does not exist"
        response = request.http_version + " 404 Not Found\r\n"
        response += "Content-Type: text/plain\r\n"
        response += "Content-Length: " + str(len(errorMsg)) + "\r\n"
        response += "X-Content-Type-Options: nosniff\r\n\r\n"
        response += errorMsg
        response = response.encode()
    return response
def serve_chatDelete(request: Request):
    response = ""
    look_id = request.path[15:]
    print(look_id)
    collection = chat_collection.find_one({"id":look_id}, {"_id":0, "message": 1, "username": 1, "id": 1})
    print(collection)
    user = collection["username"]
    aToken = ""
    userToken = " "
    if user != "Guest" and "token" in request.cookies.keys() and request.cookies["token"]:
        userToken = hashlib.sha256(request.cookies["token"].encode()).hexdigest()
        # print(userToken)
        aToken = login_collection.find_one({"username": user})
        # print(aToken)
        aToken = aToken["authtoken"]
    
    if collection is not None:
        # For authenticated users delete
        if userToken == aToken: 
            chat_collection.delete_one({"id": look_id})
            response += request.http_version
            response += " 204 No Content\r\n"
            response += "Content-Type: text/plain\r\n"
            response += "Content-Length: 0" + "\r\n"
            response += "X-Content-Type-Options: nosniff\r\n\r\n"
            response = response.encode()
        # Forbidden if they try to delete others
        else:
            response += request.http_version
            response += " 403 Forbidden\r\n"
            response += "Content-Type: text/plain\r\n"
            response += "Content-Length: 0" + "\r\n"
            response += "X-Content-Type-Options: nosniff\r\n\r\n"
            response = response.encode()
    else:
        errorMsg = "The requested id does not exist"
        response = request.http_version + " 404 Not Found\r\n"
        response += "Content-Type: text/plain\r\n"
        response += "Content-Length: " + str(len(errorMsg)) + "\r\n"
        response += "X-Content-Type-Options: nosniff\r\n\r\n"
        response += errorMsg
        response = response.encode()

    return response

def serve_register(request: Request):
    response = ""
    info = extract_credentials(request)
    if validate_password(info[1]):
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(info[1].encode(), salt)
        dict = {
            "username": info[0],
            "salt": salt,
            "hash": hash,
            "authtoken": ""
        }
        login_collection.insert_one(dict)
        response += request.http_version + " 302 Found redirect\r\n"
        response += "Content-Type: text/html\r\n"
        response += "Content-Length: 0\r\n"
        response += "X-Content-Type-Options: nosniff\r\n"
        response += "Location: /\r\n\r\n" 

    else:
        errorMsg = "Not a valid username/password"
        response += request.http_version + " 401 Unauthorized\r\n"
        response += "Content-Type: text/plain\r\n"
        response += "Content-Length: " + str(len(errorMsg)) + "\r\n"
        response += "X-Content-Type-Options: nosniff\r\n\r\n"
        response += errorMsg

    response = response.encode()
    return response

def serve_login(request: Request):
    response = ""
    info = extract_credentials(request)
    
    salt_hash = login_collection.find_one({"username": info[0]}, {"username": 1, "salt": 1, "hash": 1, "_id": 0})
    #print(salt_hash)
    if not validate_password(info[1]) or salt_hash is None:
        errorMsg = "Not a valid username/password"
        response += request.http_version + " 401 Unauthorized\r\n"
        response += "Content-Type: text/plain\r\n"
        response += "Content-Length: " + str(len(errorMsg)) + "\r\n"
        response += "X-Content-Type-Options: nosniff\r\n\r\n"
        response += errorMsg
        return response.encode()
    inputHash = bcrypt.hashpw(info[1].encode(), salt_hash["salt"])
    dataHash = salt_hash["hash"]
    #print(inputHash + "   " + dataHash)
    if inputHash == dataHash:
        token = secrets.token_urlsafe(24)
        newDict = {
            "username": info[0],
            "salt": salt_hash["salt"],
            "hash": salt_hash["hash"],
            "authtoken": hashlib.sha256(token.encode()).hexdigest()
        }
        login_collection.update_one({"username": info[0]}, {"$set": newDict})
        response += request.http_version + " 302 Found redirect\r\n"
        response += "Content-Type: text/html\r\n"
        response += "Content-Length: 0\r\n"
        response += "X-Content-Type-Options: nosniff\r\n"
        response += "Set-Cookie: token=" + token + "; Max-Age=3600; HttpOnly;" + "\r\n"
        response += "Location: /\r\n\r\n" 
        
    else: 
        errorMsg = "Not a valid username/password"
        response += request.http_version + " 401 Unauthorized\r\n"
        response += "Content-Type: text/plain\r\n"
        response += "Content-Length: " + str(len(errorMsg)) + "\r\n"
        response += "X-Content-Type-Options: nosniff\r\n\r\n"
        response += errorMsg
        
    
    response = response.encode()
    return response

def serve_logout(request: Request):
    response = ""
    collection = login_collection.find_one({"authtoken": hashlib.sha256(request.cookies["token"].encode()).hexdigest()})
    # print(collection)
    if collection:
        newDict = {
            "username": collection["username"],
            "salt": collection["salt"],
            "hash": collection["hash"],
            "authtoken": "",
            "xsrf": ""
        }
        login_collection.update_one({"authtoken": hashlib.sha256(request.cookies["token"].encode()).hexdigest()}, {"$set": newDict})
    response += request.http_version + " 302 Found redirect\r\n"
    response += "Content-Type: text/html\r\n"
    response += "Content-Length: 0\r\n"
    response += "X-Content-Type-Options: nosniff\r\n"
    response += "Set-Cookie: token=" + "; Max-Age=3600; HttpOnly;" + "\r\n"
    response += "Location: /\r\n\r\n" 
    response = response.encode()
    return response

def login_spotify(req: Request):
    dataOb = {
        "client_id": os.environ.get('CLIENT_ID'),
        "client_secret": os.environ.get('CLIENT_SECRET'),
        "redirect_uri": "http://localhost:8080/spotify",
        "scope": 'user-read-private user-read-email user-read-currently-playing',
        "response_type": 'code'
    }
    
    spotify = requests.get("https://accounts.spotify.com/authorize?", dataOb)
    
    response = req.http_version + " 302 Found redirect\r\n"
    response += "Content-Type: application/x-www-form-urlencoded\r\n"
    response += "Content-Length: 0\r\n"
    response += "X-Content-Type-Options: nosniff\r\n"
    response += "Location: " + spotify.url + "\r\n\r\n" 
    response = response.encode()
    return response

def loggedin_spotify(req: Request):
    code = req.path[req.path.find('=', 1)+1:]
    # Just Spotify documentation 
    headerOb = {
        "Content-Type": 'application/x-www-form-urlencoded',
        'Authorization': 'Basic ' + base64.b64encode(str(os.environ.get('CLIENT_ID') + ':' + os.environ.get('CLIENT_SECRET')).encode()).decode()
    }
    dataOb = {
        "code": code,
        "grant_type": 'authorization_code',
        "redirect_uri": "http://localhost:8080/spotify"
    }
    spotifyResponse = requests.post("https://accounts.spotify.com/api/token", data=dataOb,headers=headerOb)
    spotifyResponse = spotifyResponse.json()
    accessToken = spotifyResponse['access_token']
    profile = requests.get('https://api.spotify.com/v1/me', headers={'Authorization': 'Bearer ' + accessToken})
    profile = profile.json()
    token = secrets.token_urlsafe(24)
    dic = {
        "username": profile["email"],
        "hash": "",
        "salt": "",
        "authtoken": hashlib.sha256(token.encode()).hexdigest(),
        "xsrf": "",
        "accesstoken": accessToken
    }
    login_collection.insert_one(dic)
    response = req.http_version + " 302 Found redirect\r\n"
    response += "Content-Type: text/html\r\n"
    response += "Content-Length: 0\r\n"
    response += "X-Content-Type-Options: nosniff\r\n"
    response += "Set-Cookie: token=" + token + "; Max-Age=3600; HttpOnly;" + "\r\n"
    response += "Location: /\r\n\r\n" 
    response = response.encode()
    return response

def serve_Uploads(req: Request):
    data = parse_multipart(req)
    folder = "public/image" # Folder for images saved to

    # All file signatures
    file_signatures = {
        b'\xff\xd8\xff': "jpeg",
        b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a': "png",
        b'\x47\x49\x46\x38\x39\x61': "gif",
        b'\x00\x00\x00': "mp4"
    }

    # Check the current file signature
    contents = data.parts[0].content
    file_type = ""
    for sign in file_signatures.keys():
        if contents.startswith(sign):
            file_type = file_signatures[sign]

    print(file_type)
    # If file signature cannot be determined return 400 code
    if file_type == "":
        errorMessage = "File not supported"
        response = req.http_version + " 404 Not Found\r\n"
        response += "Content-Type: text/plain\r\n"
        response += "Content-Length: " + str(len(errorMessage)) + "\r\n"
        response += "X-Content-Type-Options: nosniff\r\n\r\n"
        response += errorMessage
        response = response.encode()
        return response
    
    # Save the file with the right extension
    name = 'file' + str(len(os.listdir(folder))-7)
    if file_type == "jpeg":
        name += '.jpeg'
    elif file_type == "png":
        name += '.png'
    elif file_type == "gif":
        name +=  '.gif'
    else:
        name += '.mp4'
    
    file = os.path.join(folder, name)
    with open(file, 'wb') as file:
        file.write(data.parts[0].content)
        file.close()
    
    #images.append('/' + file.name)
    # Store in chat database with correct tags and username
    # For username
    authToken = ""
    if "token" in req.cookies.keys():
        authToken = hashlib.sha256(req.cookies["token"].encode()).hexdigest()
    collection = login_collection.find_one({"authtoken": authToken}, {"username": 1})
    username = "Guest"
    if collection:
        username = collection["username"]
    # For id
    idNum = 1
    all_data = list(chat_collection.find({}))
    if len(all_data) != 0:
        idNum = len(all_data) + 1
    
    
    # Now store
    if file_type == 'mp4':
        dict = {
                "message": '<video controls><source src="' + file.name + '" type="video/mp4"></video>',
                "username": username,
                "id": str(idNum)
            }
    else:
        dict = {
                "message": '<img src="' + file.name + '">',
                "username": username,
                "id": str(idNum)
            }
    chat_collection.insert_one(dict) 
    
    response = req.http_version + " 302 Found\r\n"
    response += "Content-Type: text/html\r\n"
    response += "Content-Length: 0\r\n"
    response += "X-Content-Type-Options: nosniff\r\n"
    response += "Location: /\r\n\r\n" 
    response = response.encode()
    return response

def serve_Files(req: Request):
    # Security Check
    name = req.path[14:]
    name.replace("/", "")
    image_directory = 'public/image/' + name

    response = req.http_version + " 200 OK\r\n"
    if '.jpeg' in req.path:
        response += "Content-Type: img/jpeg\r\n"
    elif '.png' in req.path:
        response += "Content-Type: img/png\r\n"
    elif '.gif' in req.path:
        response += "Content-Type: img/gif\r\n"
    elif '.mp4' in req.path:
        response += "Content-Type: video/mp4\r\n"
    else: 
        errorMessage = "File not found"
        response = req.http_version + " 404 Not Found\r\n"
        response += "Content-Type: text/plain\r\n"
        response += "Content-Length: " + str(len(errorMessage)) + "\r\n"
        response += "X-Content-Type-Options: nosniff\r\n\r\n"
        response += errorMessage
        response = response.encode()
        return response

    response += "Content-Length: " + fileSize(image_directory) + "\r\n"
    response += "X-Content-Type-Options: nosniff\r\n\r\n"
    response = response.encode()
    response += fileString(image_directory)
    
    return response

def websocket_protocol(req: Request):
    user_key = req.headers['Sec-WebSocket-Key']
    accept_response = compute_accept(user_key)

    response = req.http_version + " 101 Switching Protocols\r\n"
    response += "Connection: Upgrade\r\n"
    response += "Upgrade: websocket\r\n"
    response += "Sec-WebSocket-Accept: " + accept_response + "\r\n"
    response += "X-Content-Type-Options: nosniff\r\n\r\n"
    response = response.encode()

    return response

# Serve Files
router.add_route("GET", "^/$", serve_root)
#router.add_route("GET", "^/public/index.html$", serve_root)
router.add_route("GET", "^/public/functions.js$", serve_funcjs)
router.add_route("GET", "^/public/style.css$", serve_css)
router.add_route("GET", "^/public/favicon.ico$", serve_favicon)
router.add_route("GET", "^/public/webrtc.js$", serve_webjs)
# Serve Images
router.add_route("GET", "^/public/image/eagle.jpg$", serve_eagle)
router.add_route("GET", "^/public/image/cat.jpg$", serve_cat)
router.add_route("GET", "^/public/image/dog.jpg$", serve_dog)
router.add_route("GET", "^/public/image/elephant-small.jpg$", serve_elephantS)
router.add_route("GET", "^/public/image/elephant.jpg$", serve_elephant)
router.add_route("GET", "^/public/image/flamingo.jpg$", serve_flamingo)
router.add_route("GET", "^/public/image/kitten.jpg$", serve_kitten)
# Serve Chat
router.add_route("POST", "^/chat-messages$", serve_chatPost)
router.add_route("GET", "^/chat-messages$", serve_chatGet)
router.add_route("PUT", "^/chat-messages/.", serve_chatPut)
router.add_route("GET", "^/chat-messages/.", serve_chatGetIndividual)
router.add_route("DELETE", "^/chat-messages/.", serve_chatDelete)
# Login/Reg
router.add_route("POST", "^/register$", serve_register)
router.add_route("POST", "^/login$", serve_login)
router.add_route("POST", "^/logout$", serve_logout)
router.add_route("POST", "^/spotify$", login_spotify)
router.add_route("GET", "^/spotify?", loggedin_spotify)
# Post images
router.add_route("POST", "^/chat-files$", serve_Uploads)
router.add_route("GET", "^/public/image/file.*$", serve_Files)
# WebSocket
router.add_route("GET", "^/websocket$", websocket_protocol)

def database_id():
    idNum = 0
    all_data = list(chat_collection.find({}))
    if len(all_data) == 0:
        idNum = 1
    else:
        idNum = len(all_data) + 1

    return idNum

def load_prev(self):
    all_data = list(chat_collection.find({}, {"_id":0, "message": 1, "username": 1, "id": 1}))
    # If there is no data in the chat collection then just move on
    if all_data:
        msg = json.dumps(all_data)
        sending = generate_ws_frame(msg)
        self.request.sendall(sending)

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        received_data = self.request.recv(2048)
        if len(received_data) == 0:
            return
        # print(self.client_address)
        # print("--- received data ---")
        # print(received_data)
        # print("--- end of data ---\n\n")
        # TODO: Parse the HTTP request and use self.request.sendall(response) to send your response
        request = Request(received_data)
        reqlength = 0
        if "Content-Length" in request.headers:
            reqlength = int(request.headers["Content-Length"])

            while len(request.body) < reqlength:
                received_data = self.request.recv(2048)
                request.body += received_data

        # print(request.body) # Show whole content body
        response = router.route_request(request)

        # Send response after each request
        self.request.sendall(response)

        # Get authentication if there is one
        authToken = ""
        if "token" in request.cookies.keys():
            authToken = hashlib.sha256(request.cookies["token"].encode()).hexdigest()

        collection = login_collection.find_one({"authtoken": authToken}, {"username": 1, "salt": 1, "hash": 1, "authtoken": 1, "xsrf": 1, "accesstoken": 1, "_id": 0})
                
        # Websocket stuff
        if request.path == '/websocket':
            # # if user is using websocket, then load all chats stored in database
            # load_prev(self)
            # # Store the user websocket in a global variable list
            # socket_connections.append(self.request)

            # # For each user already in socket, display for user
            # for users in socket_users.values():
            #     print(users)
            #     dict = {
            #             "messageType": 'addUserList',
            #             "username": users,
            #         }
            #     jsonDict = json.dumps(dict)
            #     mess = generate_ws_frame(jsonDict)
            #     self.request.sendall(mess)
            
            # # if the current user is authenticated and has websocket then update the list
            # if collection:
            #         socket_users[self.request] = collection['username']
            #         # if there is a new user then send update all users
            #         dict = {
            #                     "messageType": 'addUserList',
            #                     "username": collection["username"],
            #                 }
            #         jsonDict = json.dumps(dict)
            #         mess = generate_ws_frame(jsonDict)
            #         for client in socket_connections:
            #             client.sendall(mess)
            save = b''
            # Keep the websocket open
            while True:
                # Getting message data
                data = self.request.recv(2048)
                read = 2048
                frame = parse_ws_frame(data)
                if save != b'':
                    data = save + data
                    save = b''

                if frame.opcode == 8:
                    # # Remove it from the dictionary of usernames
                    # if collection: 
                    #     u = socket_users.pop(self.request)
                    # # Remove from list of socket connections
                    # socket_connections.remove(self.request)
                    # if collection:
                    #     # Send a webframe to all sockets that I've disconnected
                    #     dict = {
                    #                 "messageType": 'removeUserList',
                    #                 "username": u,
                    #             }
                    #     jsonDict = json.dumps(dict)
                    #     mess = generate_ws_frame(jsonDict)
                    #     for client in socket_connections:
                    #         client.sendall(mess)
                    
                    break
                else:
                    # Buffer Frames
                    print(read)
                    print(len(data))
                    if read < frame.payload_length:
                        print('Buffered')
                        while frame.payload_length >= len(data):
                            data += self.request.recv(2048)
                            read += 2048
                        frame = parse_ws_frame(data)

                    # Back to back
                    if read > len(data):
                        print('Saved')
                        save = data[frame.payload_length+8:]
                        print(save)

                    print(frame.payload)

                    # # Data was parsed and now extracted
                    # msg = frame.payload.decode()
                    # msg = json.loads(msg)
                    # msg['message'] = escapeHTML(msg['message'])

                
                    # # Store the data in the database and send to other sockets
                    # idNum = database_id()
                    # dict = { }
                    # if collection:
                    #     dict = {
                    #         "messageType": 'chatMessage',
                    #         "username": collection["username"],
                    #         "id": str(idNum)
                    #     }
                    # else:
                    #     dict = {
                    #         "messageType": 'chatMessage',
                    #         "username": 'Guest',
                    #         "id": str(idNum)
                    #     }
                    # # Store the data extracted into a dictionary to be stored
                    # dict['message'] = msg['message']
                    # j = json.dumps(dict)

                    # chat_collection.insert_one(dict)
                    # print(j)
                    # print(socket_connections)
                    # # For each message in the database
                    # # Send it to the user in websocket
                    # message = generate_ws_frame(j)
                    # print(message)

                    # for client in socket_connections:
                    #     client.sendall(message)

            

def main():
    host = "0.0.0.0"
    port = 8080

    socketserver.TCPServer.allow_reuse_address = True
    server = socketserver.ThreadingTCPServer((host, port), MyTCPHandler)
    print("Listening on port " + str(port))
    server.serve_forever()


if __name__ == "__main__":
    main()