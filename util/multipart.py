from request import Request
    

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
            print(header)
            if b"name" in header:
                name = header.split(b"=")[1].split(b";")[0].strip(b'""').decode()
            key =  header.split(b":")[0].decode()
            val = header.split(b":")[1].decode().strip()
            h_dict[key] = val
        parts.append(Part(h_dict,name,content))
    obj = Mulipart(boundary, parts)
    return obj


def lecture_test():
    boundary = "----WebKitFormBoundarycriD3u6M0UuPR1ia"
    data = (
        f"POST /form-path HTTP/1.1\r\n"
        f"Content-Length: 9937\r\n"
        f"Content-Type: multipart/form-data; boundary={boundary}\r\n"
        f"\r\n"
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"commenter\"\r\n\r\n"
        f"Jesse\r\n"
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"upload\"; filename=\"discord.png\"\r\n"
        f"Content-Type: image/png\r\n\r\n"
        f"<bytes_of_the_file>\r\n"
        f"--{boundary}--"
    ).encode()

    request = Request(data)

    result = parse_multipart(request)

    expected_boundary = boundary
    expected_parts = [
        {
            "headers": {"Content-Disposition": "form-data; name=\"commenter\""},
            "name": "commenter",
            "content": b"Jesse"
        },
        {
            "headers": {
                "Content-Disposition": "form-data; name=\"upload\"; filename=\"discord.png\"",
                "Content-Type": "image/png"
            },
            "name": "upload",
            "content": b"<bytes_of_the_file>"
        }
    ]

    assert result.boundary == expected_boundary
    for part, expected_part in zip(result.parts, expected_parts):
        print(f"actual header = {part.headers}")
        print(f"expected header = {expected_part["headers"]}")
        assert part.headers == expected_part["headers"]
        print(f"actual name = {part.name}")
        print(f"expected name = {expected_part["name"]}")
        assert part.name == expected_part["name"]
        assert part.content == expected_part["content"]


# Run the test case
if __name__ == "__main__":
    lecture_test()
