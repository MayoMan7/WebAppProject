from pymongo import MongoClient
import json
from bson import ObjectId
import uuid
from html import escape
import hashlib

client = MongoClient("mongo:27017")
db = client["chat_database"]
chat__collection = db["chat_messages"]

db_client = client["user_database"]
user__collection = db_client["user"]


def get_username(requst):
    # print(requst.cookies)
    token = requst.cookies.get("auth_token")
    # print(f"token = {token}")
    if not token:
        return "Guest"
    token = hashlib.sha256(token.encode("utf-8")).hexdigest()
    user = user__collection.find_one({"auth_token": token})
    # print(f"user = {user}")
    if not user:
        return "Guest"
    return user["username"]


def verify_xsrf(xsrf,username):
    user = user__collection.find_one({"username": username})
    # print(user)
    # print(f"request[xsrf_token] = {xsrf}")
    # print(user["xsrf_token"])
    if user["xsrf_token"] == xsrf:
        return True
    return False
    

    
    

def receive_message(requst,handler):
    message_json = json.loads(requst.body)
    # print(f" getting username {get_username(requst)}")
    username = get_username(requst)

    if username != "Guest":
        if not verify_xsrf(message_json["xsrf_token"],username):
            body = "403 Forbidden"
            response_403 = (
                "HTTP/1.1 403 Forbidden\r\n"
                "Content-Type: text/plain\r\n"
                f"Content-Length: {len(body)}\r\n"
                "X-Content-Type-Options: nosniff\r\n"
                "Connection: close\r\n"
                "\r\n"
                f"{body}"
            )

            handler.request.sendall(response_403.encode())
            return
    message = escape(message_json["message"])
    
    browser_cookie = requst.cookies["browser_cookie"]

    message_data = {
        "username": username,
        "message": message,
        "browser_cookie": browser_cookie
    }
    chat__collection.insert_one(message_data)
    body = "message sent"
    content_len = len(body)
    # print(message_data)
    response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Length: {}\r\n"
            "Content-Type: application/json; charset=utf-8\r\n"
            "X-Content-Type-Options: nosniff\r\n"
            "\r\n"
            "{}"
            ).format(content_len,body)
    handler.request.sendall(response.encode())

def save_message(username,message, browser_cookie):
    message_data = {
        "username": username,
        "message": message,
        "browser_cookie": browser_cookie
    }
    saved = chat__collection.insert_one(message_data)
    id = str(saved.inserted_id)
    # print(id)
    return id





def receive_image(requst,handler,filename):
    username = get_username(requst)
    message = f'<img src="/{filename}" alt="user upload"/>'

    if ".mp4" in filename: 
        message = f'<video controls><source src="/{filename}" type="video/mp4"></video>'
        
    browser_cookie = requst.cookies["browser_cookie"]

    message_data = {
        "username": username,
        "message": message,
        "browser_cookie": browser_cookie
    }
    chat__collection.insert_one(message_data)
    response = (
        "HTTP/1.1 302 Found\r\n"
        f"Location: /\r\n"
        "X-Content-Type-Options: nosniff\r\n"
        "Content-Type: text/html\r\n"
        "\r\n"
    )
    handler.request.sendall(response.encode())


def send_messages(request,handler):
    array = []
    for message in chat__collection.find():
        # print(message)
        array.append({
            "message": message["message"],
            "username": message["username"],
            "id": str(message["_id"]),
            "browser_cookie": message["browser_cookie"]
        })
    body = json.dumps(array)
    content_len = len(body)
    response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Length: {}\r\n"
            "Content-Type: application/json; charset=utf-8\r\n"
            "X-Content-Type-Options: nosniff\r\n"
            "\r\n"
            "{}"
            ).format(content_len,body)
    handler.request.sendall(response.encode())

def delete_messages(request,handler):
    id = request.path.split("/chat-messages/")[1]
    # print([i for i in chat__collection.find()])
    # print("deleting")
    msg = chat__collection.find_one({"_id": ObjectId(id)})
    # print(msg)
    username = get_username(request)
    # print(username)
    if username == msg["username"]:
        # print("DELETE MATCH")
        chat__collection.delete_one({"_id": ObjectId(id)})
        # print([i for i in chat__collection.find()])
        content_len = 0
        response = (
                "HTTP/1.1 204 No Content\r\n"
                "Content-Length: {}\r\n"
                "Content-Type: application/json; charset=utf-8\r\n"
                "X-Content-Type-Options: nosniff\r\n"
                "\r\n"
                ).format(content_len)
        handler.request.sendall(response.encode())
    
    # print("delete fail")
    body = "403 Forbidden"
    response_403 = (
        "HTTP/1.1 403 Forbidden\r\n"
        "Content-Type: text/plain\r\n"
        f"Content-Length: {len(body)}\r\n"
        "X-Content-Type-Options: nosniff\r\n"
        "Connection: close\r\n"
        "\r\n"
        f"{body}"
    )

    handler.request.sendall(response_403.encode())





    
