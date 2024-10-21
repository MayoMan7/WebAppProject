from util.auth import extract_credentials
from util.auth import validate_password
from pymongo import MongoClient
import bcrypt
import os
import hashlib

client = MongoClient("mongo:27017")
db = client["user_database"]
user__collection = db["user"]

def register(request,handler):
    username,password = extract_credentials(request)
    print(username,password)
    if validate_password(password) and not user__collection.find_one({"username": username}):            
        salt = bcrypt.gensalt()
        hashed_pass = bcrypt.hashpw(password.encode("utf-8"),salt)
        account = {
            "username": username,
            "password": hashed_pass.decode("utf-8"),
        }
        user__collection.insert_one(account)
        print("ABOUT TO PRINT USERS!!!!!!!!!!")
        for user in user__collection.find():
            print(user)

        print("good work")
        response = (
            "HTTP/1.1 302 Found\r\n"
            "Location: /\r\n"
            "X-Content-Type-Options: nosniff\r\n"
            "Content-Type: text/plain\r\n"
            "Content-Length: 0\r\n"
            "\r\n"
        )
        return handler.request.sendall(response.encode())
    body = "404 Not Found"
    response_404 = (
        "HTTP/1.1 404 Not Found\r\n"
        "Content-Type: text/plain\r\n"
        f"Content-Length: {len(body)}\r\n"
        "X-Content-Type-Options: nosniff\r\n"
        "Connection: close\r\n"
        "\r\n"
        f"{body}"
    )

    handler.request.sendall(response_404.encode())

def login(request,handler):
    username,password = extract_credentials(request)
    print(username,password)

    user = user__collection.find_one({"username": username})
    if user:
        saved_pass = user["password"]
        if bcrypt.checkpw(password.encode("utf-8"),saved_pass.encode("utf-8")):
            token = os.urandom(32).hex()
            hashed_token = hashlib.sha256(token.encode("utf-8")).hexdigest()
            print(f"hashed_token = {hashed_token}")
            user__collection.update_one({"username": username},{"$set": {"auth_token": hashed_token}})
            print("printing user data")
            for user in user__collection.find():
                print(user)
            response = (
                "HTTP/1.1 302 Found\r\n"
                f"Set-Cookie: auth_token={token}; HttpOnly\r\n"
                "Location: /\r\n"
                "X-Content-Type-Options: nosniff\r\n"
                "Content-Type: text/plain\r\n"
                "Content-Length: 0\r\n"
                "\r\n"
            )
            return handler.request.sendall(response.encode())
    

    
    body = "404 Not Found"
    response_404 = (
        "HTTP/1.1 404 Not Found\r\n"
        "Content-Type: text/plain\r\n"
        f"Content-Length: {len(body)}\r\n"
        "X-Content-Type-Options: nosniff\r\n"
        "\r\n"
        f"{body}"
    )

    handler.request.sendall(response_404.encode())


def logout(request,handler):
    print("starting logout")
    token = request.cookies.get("auth_token")
    token = hashlib.sha256(token.encode("utf-8")).hexdigest()
    user = user__collection.find_one({"auth_token": token})
    print(f"user = {user}")
    if user:
        username = user["username"]
        user__collection.update_one({"username": username},{"$unset": {"auth_token": token}})
        print(user)
        response = (
            "HTTP/1.1 302 Found\r\n"
            "Set-Cookie: auth_token=; HttpOnly; Max-Age=0;\r\n"
            "X-Content-Type-Options: nosniff\r\n"
            "Location: /\r\n"
            "Content-Type: text/plain\r\n"
            "Content-Length: 0\r\n"
            "\r\n"
        )
        return handler.request.sendall(response.encode())
    
    
    body = "404 Not Found"
    response_404 = (
        "HTTP/1.1 404 Not Found\r\n"
        "Content-Type: text/plain\r\n"
        f"Content-Length: {len(body)}\r\n"
        "X-Content-Type-Options: nosniff\r\n"
        "\r\n"
        f"{body}"
    )

    return handler.request.sendall(response_404.encode())

    
            

    