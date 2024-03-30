from util.request import Request


class Part:
    def __init__(self, headers, name, content):
        self.headers = headers
        self.name = name
        self.content = content

class Multipart:
    def __init__(self, boundary, parts):
        self.boundary = boundary
        self.parts = parts

def parse_multipart(request):
    boundary = request.headers["Content-Type"]
    boundary = boundary.split("=")[1]
    ret_boundary = boundary
    boundary = "--" + boundary
    first_boundary = boundary + "\r\n"
    last_boundary = "\r\n" + boundary + "--\r\n"
    boundary = "\r\n" + boundary + "\r\n"

    data = request.body.replace(first_boundary.encode(), b"", 1)
    data = data.replace(last_boundary.encode(), b"")
    data = data.split(boundary.encode())

    parts = []
    for section in data:
        print(section)
        split = section.split(b"\r\n\r\n",1)

        content_headers = split[0].decode()

        header_parts = content_headers.split('\r\n')
        name = content_headers.split('name="')[1].split('"')[0]
        content = split[1]
        
        headers = {}
        for part in header_parts:
            key = part.split(":")[0].strip()
            value = part.split(":")[1].strip()
            headers[key] = value
        
        part = Part(headers,name,content)
        parts.append(part)
    
    return Multipart(ret_boundary, parts)




