import base64
import hashlib
from pymongo import MongoClient
import requests
import os

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")

client = MongoClient("mongo:27017")
db = client["user_database"]
user__collection = db["user"]


def get_code(request,handler):
    print("STARTING SPOTIFY")
    
    state = os.urandom(16)
    scope = "user-read-private user-read-email"

    params = (
        f"response_type=code&"
        f"client_id={client_id}&"
        f"scope={scope}&"
        f"redirect_uri={redirect_uri}&"
        f"state={state}"
    )
    url = f"https://accounts.spotify.com/authorize?{params}"

    response = (
        "HTTP/1.1 302 Found\r\n"
        f"Location: {url}\r\n"
        "X-Content-Type-Options: nosniff\r\n"
        "Content-Type: text/html\r\n"
        "\r\n"
    )
    handler.request.sendall(response.encode())


def get_access(request,handler):
    print("STEP 2")
    query_string = request.path.split("?")[1]

    params = {part.split("=")[0]:part.split("=")[1] for part in query_string.split("&")}
    form = {
        "code": params["code"],
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code"
    }
    authorization = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode("utf-8")
    print(f"authorization = {authorization}")
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {authorization}"
    }
    url = "https://accounts.spotify.com/api/token"

    response = requests.post(url, data=form, headers=headers)
    print(f"Response status_code: {response.status_code}")
    print(f"Response text: {response.text}")
    data = response.json()
    access_token = data.get("access_token")

    api_url = "https://api.spotify.com/v1/me"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(api_url,headers=headers)
    print(f"Response status_code: {response.status_code}")
    print(f"Response text: {response.text}")
    data = response.json()
    email = data.get("email")
    login_with_spotify(email,handler)



def login_with_spotify(username,handler):
    if not user__collection.find_one({"username": username}):
        account = {
            "username": username,
        }
        user__collection.insert_one(account)
    token = os.urandom(32).hex()
    hashed_token = hashlib.sha256(token.encode("utf-8")).hexdigest()
    user__collection.update_one({"username": username},{"$set": {"auth_token": hashed_token}})
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
    









