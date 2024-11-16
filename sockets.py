from util.websockets import compute_accept

def handshake(request,handler):
    print(request.headers)
    print("Sec-WebSocket-Key" in request.headers.keys())
    key = request.headers.get("Sec-WebSocket-Key",None)
    print(f"key from client {key}")
    key = compute_accept(key)
    print(key)
    response = (
        "HTTP/1.1 101 Switching Protocols\r\n"
        "X-Content-Type-Options: nosniff\r\n"
        "Connection: Upgrade\r\n"
        "Upgrade: websocket\r\n"
        f"Sec-WebSocket-Accept: {key}\r\n"
        "\r\n"
    )
    handler.request.sendall(response.encode())
