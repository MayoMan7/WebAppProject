class Request:

    def __init__(self, request: bytes):
        # TODO: parse the bytes of the request and populate the following instance variables
        self.body = b""
        self.method = ""
        self.path = ""
        self.http_version = ""
        self.headers = {}
        self.cookies = {}


        headers = request.split(b'\r\n\r\n',1)[0]
        body = request.split(b'\r\n\r\n',1)[1]

    
        
        lines = headers.decode().split("\r\n")
        line1 = lines[0]
        line1 = line1.split(" ")
        self.method = line1[0]
        self.path = line1[1]
        self.http_version = line1[2]

        for line in lines[1:]:
            if line == "":
                break
            header_line = line.split(":",1)
            key = header_line[0].strip()
            value = header_line[1]
            value = value.strip()
            self.headers.update({key:value})

            if(key == "Cookie"):
                cookies = header_line[1].split(";")
                for cookie in cookies:
                    cookie = cookie.split("=")
                    key = cookie[0].strip()
                    value = cookie[1].strip()
                    self.cookies.update({key:value})
            

        self.body = body


def test1():
    request = Request(b'GET / HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\n\r\n')
    assert request.method == "GET"
    assert "Host" in request.headers
    assert request.headers["Host"] == "localhost:8080"  # note: The leading space in the header value must be removed
    assert request.body == b""  # There is no body for this request.
    # When parsing POST requests, the body must be in bytes, not str

    # This is the start of a simple way (ie. no external libraries) to test your code.
    # It's recommended that you complete this test and add others, including at least one
    # test using a POST request. Also, ensure that the types of all values are correct

def test_2():
    request_with_cookies = b'GET / HTTP/1.1\r\nHost: localhost:8080\r\nCookie: session_id=123; user_id=123\r\n\r\n'
    request = Request(request_with_cookies)
    assert "session_id" in request.cookies
    assert request.cookies["session_id"] == "123"
    assert "user_id" in request.cookies
    assert request.cookies["user_id"] == "123"


if __name__ == '__main__':
    test1()
    test_2()
    print("pass")



