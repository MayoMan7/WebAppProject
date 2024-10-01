import uuid

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

# router function for sending css code
def host_css(request, handler):
    print("WE WANT CSS")
    path = "public/style.css"
    try:
        print("WE SHOULD HAVE GOT CSS")
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
    try:
        with open(path,"rb") as file:
            body = file.read()
            content_len = len(body)
            response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Length: {}\r\n"
            "Content-Type: image/jpeg\r\n"
            "X-Content-Type-Options: nosniff\r\n"
            "\r\n"
            ).format(content_len,body)
            handler.request.sendall(response.encode('utf-8'))
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
            handler.request.sendall(response.encode('utf-8'))
            handler.request.sendall(body)
    except:
        response = ("HTTP/1.1 404 Not Found\r\n""Content-Type: text/plain\r\n""Content-Length: 15\r\n""\r\n""404 Not Found")
        handler.request.sendall(response.encode())