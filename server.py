import socketserver
from util.request import Request
from util.router import Router
from util.hello_path import hello_path
from hosting_files import *
from chat import *
from authentication import *
from spotify import *
from media import *


class MyTCPHandler(socketserver.BaseRequestHandler):

    def __init__(self, request, client_address, server):
        self.router = Router()
        self.router.add_route("GET", "/hello", hello_path, True)
        # TODO: Add your routes here
        self.router.add_route("GET", "/", host_html, True)
        self.router.add_route("GET", "/public/style.css", host_css, True)
        self.router.add_route("GET", "/public/functions.js", host_functions, True)
        self.router.add_route("GET", "/public/webrtc.js", host_webrtc, True)
        self.router.add_route("GET", "/public/image/", host_images, False)
        self.router.add_route("GET", "/public/favicon.ico", host_favicon, True)
        self.router.add_route("POST", "/chat-messages", receive_message, True)
        self.router.add_route("GET", "/chat-messages", send_messages, True)
        self.router.add_route("DELETE", "/chat-messages/", delete_messages, False)
        self.router.add_route("POST", "/register", register, True)
        self.router.add_route("POST", "/login", login, True)
        self.router.add_route("POST", "/logout", logout, True )
        self.router.add_route("GET", "/spotify-login", get_code, False)
        self.router.add_route("GET", "/spotify", get_access, False)
        self.router.add_route("POST", "/media-uploads", upload, True)

        super().__init__(request, client_address, server)

    def handle(self):
        received_data = self.request.recv(2048)
        # print(self.client_address)
        # print("--- received data ---")
        # print(received_data)
        # print("--- end of data ---\n\n")
        request = Request(received_data)
        print(request.path)
        if request.path == "/register":
            print("register")
            print(request.body)

        self.router.route_request(request, self)


def main():
    host = "0.0.0.0"
    port = 8080
    socketserver.TCPServer.allow_reuse_address = True

    server = socketserver.TCPServer((host, port), MyTCPHandler)

    print("Listening on port " + str(port))
    server.serve_forever()


if __name__ == "__main__":
    main()
