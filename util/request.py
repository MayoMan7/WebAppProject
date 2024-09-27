class Request:

    def __init__(self, request: bytes):
        # TODO: parse the bytes of the request and populate the following instance variables
        lines, self.body = (request.split(b"\r\n\r\n"))
        lines = lines.split(b"\r\n")
        self.method = lines[0].split(b" ")[0].decode()
        self.path = lines[0].split(b" ")[1].decode()
        self.http_version = lines[0].split(b" ")[2].decode()
        self.headers = {}
        self.cookies = {}
        for header in lines[1:]: # the second line to the 3rd to last line
            print(header)
            if header == b"":
                continue 
            if header.split(b":",1)[0].decode() == "Cookie":
                for cookie in header.split(b":",1)[1].decode().strip().split("; "):
                    self.cookies[cookie.split("=")[0]] = cookie.split("=")[1]

            # else:
            self.headers[header.split(b":",1)[0].decode().strip()] = header.split(b":",1)[1].decode().strip()
        

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


# Run the test function
if __name__ == "__main__":
    test1()

