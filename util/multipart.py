class Mulipart():
    def __init__(self,boundary,parts):
        self.boundary = boundary
        self.parts = parts

class Part():
    def __init__(self,headers,name,content):
        self.headers = headers
        self.name = name
        self.content = content


def parse_multipart(request):
    parts = []
    boundary = request.headers["Content-Type"].split("=")[1]
    intial_bound = f"--{boundary}\r\n".encode()
    intial_split = request.body.split(intial_bound,1)[1]
    bound = f"\r\n--{boundary}\r\n".encode()
    restofthem = intial_split.split(bound)
    restofthem[-1] = restofthem[-1].split(f"\r\n--{boundary}--".encode())[0]
    for i in restofthem:
        headers, content = i.split(b"\r\n\r\n",1)
        # name = name.strip().split(b"=")
        h_dict = {}
        for header in headers.split(b"\r\n"):
            # print(header)
            if b"name" in header:
                name = header.split(b"=")[1].split(b";")[0].strip(b'""').decode()
            key =  header.split(b":")[0].decode()
            val = header.split(b":")[1].decode().strip()
            h_dict[key] = val
        parts.append(Part(h_dict,name,content))
    obj = Mulipart(boundary, parts)
    return obj