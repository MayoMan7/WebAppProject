import hashlib
import uuid
import os
from pymongo import MongoClient

client = MongoClient("mongo:27017")
db_client = client["user_database"]
user__collection = db_client["user"]

# router function for sending html code
def host_html(request, handler):
    path = "public/index.html"
    visit_count = 1
    if "visits" in request.cookies:
        visit_count = int(request.cookies["visits"]) + 1

    if "browser_cookie" not in request.cookies:
        browser_cookie = str(uuid.uuid4())
    else:
        browser_cookie = request.cookies["browser_cookie"]

    try:
        with open(path,"r") as file:
            body = file.read()
            body = body.replace("{{visits}}", str(visit_count))
            body = loginlogout(body,request)
            body = gen_xsrf(body)
            content_len = len(body.encode())
            response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Length: {}\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            "Set-Cookie: visits={}; Path=/; Max-Age=3600;\r\n"
            "Set-Cookie: browser_cookie={}; Path=/; Max-Age=3600; SameSite=Lax\r\n"
            "X-Content-Type-Options: nosniff\r\n"
            "\r\n"
            "{}"
            ).format(content_len,visit_count,browser_cookie,body)
    except:
        response = ("HTTP/1.1 404 Not Found\r\n""Content-Type: text/plain\r\n""Content-Length: 15\r\n""\r\n""404 Not Found")
    handler.request.sendall(response.encode())


def gen_xsrf(body):

    to_replace = "{{token_placeholder}}"
    xsrf_token = os.urandom(32).hex()
    body = body.replace(to_replace,xsrf_token)
    
    return body

def loginlogout(body,request):
    
    to_replace = "{{login/logout}}"
    login_html = """
    Login:
        <form action="/login" method="post" enctype="application/x-www-form-urlencoded">
            <label>Username:
                <input type="text" name="username"/>
            </label>
            <br/>
            <label>Password:&nbsp;
                <input type="password" name="password">
            </label>
            <input type="submit" value="Post">
        </form>
    """
    
    logout_html = """
    Logout:
        <form action="/logout" method="post" enctype="application/x-www-form-urlencoded">
            <input type="submit" value="Post">
        </form>
    """
    
    # print(to_replace in body)


    token = request.cookies.get("auth_token")
    # print(f"WE ARE TRYING TO REPLACE, TOKEN = {token}")
    if token:
        token = hashlib.sha256(token.encode("utf-8")).hexdigest()
        user = user__collection.find_one({"auth_token": token})
        # print(user)
        if user:
            body = body.replace(to_replace,logout_html)
            to_replace = "{{token_placeholder}}"
            xsrf_token = os.urandom(32).hex()
            body = body.replace(to_replace,xsrf_token)
            user__collection.update_one({"auth_token": token},{"$set": {"xsrf_token": xsrf_token}})
            return body
    body = body.replace(to_replace,login_html)
    return body

# router function for sending css code
def host_css(request, handler):
    # print("WE WANT CSS")
    path = "public/style.css"
    try:
        # print("WE SHOULD HAVE GOT CSS")
        with open(path,"r") as file:
            body = file.read()
            content_len = len(body.encode())
            response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Length: {}\r\n"
            "Content-Type: text/css; charset=utf-8\r\n"
            "X-Content-Type-Options: nosniff\r\n"
            "\r\n"
            "{}"
            ).format(content_len,body)
    except:
        response = ("HTTP/1.1 404 Not Found\r\n""Content-Type: text/plain\r\n""Content-Length: 15\r\n""\r\n""404 Not Found")
    handler.request.sendall(response.encode())

# router function for sending js code
def host_functions(request, handler):
    path = "public/functions.js"
    try:
        with open(path,"r") as file:
            body = file.read()
            content_len = len(body.encode())
            response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Length: {}\r\n"
            "Content-Type: text/javascript; charset=utf-8\r\n"
            "X-Content-Type-Options: nosniff\r\n"
            "\r\n"
            "{}"
            ).format(content_len,body)
    except:
        response = ("HTTP/1.1 404 Not Found\r\n""Content-Type: text/plain\r\n""Content-Length: 15\r\n""\r\n""404 Not Found")
    handler.request.sendall(response.encode())

# router function for sending js code
def host_webrtc(request, handler):
    path = "public/webrtc.js"
    try:
        with open(path,"r") as file:
            body = file.read()
            content_len = len(body.encode())
            response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Length: {}\r\n"
            "Content-Type: text/javascript; charset=utf-8\r\n"
            "X-Content-Type-Options: nosniff\r\n"
            "\r\n"
            "{}"
            ).format(content_len,body)
    except:
        response = ("HTTP/1.1 404 Not Found\r\n""Content-Type: text/plain\r\n""Content-Length: 15\r\n""\r\n""404 Not Found")
    handler.request.sendall(response.encode())

def host_images(request, handler):
    path = request.path[1:]
    filename = path.split("public/image/")[1]
    filename = filename.replace("/","")
    filetype = filename.split(".")[1]
    if filetype == "mp4":
        mimetype = f"video/{filetype}"
    else:
        mimetype = f"image/{filetype}"
    path = f"public/image/{filename}"
    try:
        with open(path,"rb") as file:
            body = file.read()
            content_len = len(body)
            response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Length: {}\r\n"
            "Content-Type: {}\r\n"
            "X-Content-Type-Options: nosniff\r\n"
            "\r\n"
            ).format(content_len,mimetype,body)
            handler.request.sendall(response.encode("utf-8"))
            handler.request.sendall(body)
    except:
        response = ("HTTP/1.1 404 Not Found\r\n""Content-Type: text/plain\r\n""Content-Length: 15\r\n""\r\n""404 Not Found")
        handler.request.sendall(response.encode())

def host_favicon(request, handler):
    path = "public/favicon.ico"
    try:
        with open(path,"rb") as file:
            body = file.read()
            content_len = len(body)
            response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Length: {}\r\n"
            "Content-Type: image/x-icon\r\n"
            "X-Content-Type-Options: nosniff\r\n"
            "\r\n"
            ).format(content_len,body)
            handler.request.sendall(response.encode("utf-8"))
            handler.request.sendall(body)
    except:
        response = ("HTTP/1.1 404 Not Found\r\n""Content-Type: text/plain\r\n""Content-Length: 15\r\n""\r\n""404 Not Found")
        handler.request.sendall(response.encode())