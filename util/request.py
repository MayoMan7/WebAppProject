class Request:

    def __init__(self, request: bytes):
        # TODO: parse the bytes of the request and populate the following instance variables
        self.body = b""
        self.method = ""
        self.path = ""
        self.http_version = ""
        self.headers = {}
        self.cookies = {}
        print(request.decode())
        lines = request.decode().split("\r\n")
        line1 = lines[0]
        line1 = line1.split(" ")
        self.method = line1[0]
        self.path = line1[1]
        self.http_version = line1[2]
        for row in range(len(lines)):
            if(row == 0):
                line1 = lines[row]
                line1 = line1.split(" ")
                self.method = line1[0]
                self.path = line1[1]
                self.http_version = line1[2]
            else:
                header_line = lines[row]
                if header_line == "":
                    break
                header_line = header_line.split(": ")
                key = header_line[0]
                if(key == "Cookie"):
                    cookies = header_line[1].split("; ")
                    for cookie in cookies:
                        cookie = cookie.split("=")
                        self.cookies.update(cookie[0],cookie[1])
                else:
                    value = header_line[1]
                    value = value.strip()
                    self.headers.update({key:value})


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
