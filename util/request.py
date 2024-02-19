class Request:

    def __init__(self, request: bytes):
        # TODO: parse the bytes of the request and populate the following instance variables
        self.body = b""
        self.method = ""
        self.path = ""
        self.http_version = ""
        self.headers = {}
        self.cookies = {}
        
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

                header_line = header_line.split(":",1)
                key = header_line[0].strip()

                if(key.lower() == "cookie"):
                    cookies = header_line[1].split(";")
                    for cookie in cookies:
                        cookie = cookie.split("=")
                        key = cookie[0].strip()
                        value = cookie[1].strip()
                        self.cookies.update({key:value})
                else:
                    value = header_line[1]
                    value = value.strip()
                    self.headers.update({key:value})

        index_of_body = request.decode().find("\r\n\r\n")
        if(index_of_body != -1):
            self.body = request[index_of_body + len("\r\n\r\n"):]
            


