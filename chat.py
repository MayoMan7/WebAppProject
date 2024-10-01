from pymongo import MongoClient
import json
from bson import ObjectId
import uuid
from html import escape

client = MongoClient("mongo:27017")
db = client['chat_database']
chat__collection = db['chat_messages']

def receive_message(requst,handler):
    message_json = json.loads(requst.body)
    username = "Guest"
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
            "HTTP/1.1 20 OK\r\n"
            "Content-Length: {}\r\n"
            "Content-Type: application/json; charset=utf-8\r\n"
            "X-Content-Type-Options: nosniff\r\n"
            "\r\n"
            "{}"
            ).format(content_len,body)
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
    chat__collection.delete_one({'_id': ObjectId(id)})
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




    
