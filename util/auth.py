def extract_credentials(request):
    body = request.body.decode()
    username = body.split("&")[0].split("=")[1]
    password = body.split("&")[1].split("=")[1]
    percent_encodings = {
        "%21": "!",
        "%40": "@",
        "%23": "#",
        "%24": "$",
        "%26": "&",
        "%28": "(",
        "%29": ")",
        "%2D": "-",
        "%5F": "_",
        "%3D": "="
    }
    for i in percent_encodings:
        password = password.replace(i,percent_encodings[i])
    password = password.replace("%25","%")
    # print(password)
    return [username,password]
    

def validate_password(password):
    special_chars = ['!', '@', '#', '$', '%', '^', '&', '(', ')', '-', '_', '=']
    if len(password) < 8:
        return False
    # print(char.islower() for char in password)
    # print("SOMTHING TIME")
    # for i in (char.islower() for char in password):
    #     print(i)
    if not any(char.islower() for char in password):
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char in special_chars for char in password):
        return False
    if not all(char.isalnum() or char in special_chars for char in password):
        return False
    return True

