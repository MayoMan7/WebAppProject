def extract_credentials(request):
    body = request.body.decode()
    body = body.split("&")
    user_name = body[0].split("=")[1]
    pass_word = body[1].split("=")[1]
    user_final = ""
    pass_final = ""
    index = 0

    while index < len(user_name):
        if user_name[index] == "%":
            if user_name[index+1] == "2":
                if user_name[index+2] == "1":
                    user_final+="!"
                if user_name[index+2] == "3":
                    user_final+=("#") 
                if user_name[index+2] == "4":
                    user_final+=("$")  
                if user_name[index+2] == "5":
                    user_final+=("%")
                if user_name[index+2] == "6":
                    user_final+=("&")
                if user_name[index+2] == "8":
                    user_final+=("(")
                if user_name[index+2] == "9":
                    user_final+=(")")
                if user_name[index+2] == "D":
                    user_final+=("-")
            if user_name[index+1] == "3":
                if user_name[index+2] == "D":
                    user_final+=("=")
            if user_name[index+1] == "4":
                if user_name[index+2] == "0":
                    user_final+=("@")
            if user_name[index+1] == "5":
                if user_name[index+2] == "E":
                    user_final+=("^")
                if user_name[index+2] == "F":
                    user_final+=("_")
            index += 3
        else:
            user_final+=(user_name[index])
            index += 1

    index = 0
    while index < len(pass_word):
        if pass_word[index] == "%":
            if pass_word[index+1] == "2":
                if pass_word[index+2] == "1":
                    pass_final+=("!")
                if pass_word[index+2] == "3":
                    pass_final+=("#") 
                if pass_word[index+2] == "4":
                    pass_final+=("$")  
                if pass_word[index+2] == "5":
                    pass_final+=("%")
                if pass_word[index+2] == "6":
                    pass_final+=("&")
                if pass_word[index+2] == "8":
                    pass_final+=("(")
                if pass_word[index+2] == "9":
                    pass_final+=(")")
                if pass_word[index+2] == "D":
                    pass_final+=("-")
            if pass_word[index+1] == "3":
                if pass_word[index+2] == "D":
                    pass_final+=("=")
            if pass_word[index+1] == "4":
                if pass_word[index+2] == "0":
                    pass_final+=("@")
            if pass_word[index+1] == "5":
                if pass_word[index+2] == "E":
                    pass_final+=("^")
                if pass_word[index+2] == "F":
                    pass_final+=("_")
            index +=3
        else:
            pass_final+=(pass_word[index])
            index +=1
    
    ret = []
    ret.append(user_final)
    ret.append(pass_final)
    return ret

def validate_password(string):
    chars = ['!', '@', '#', '$', '%', '^', '&', '(', ')', '-', '_', '=']
    valid_characters = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    '!', '@', '#', '$', '%', '^', '&', '(', ')', '-', '_', '=']

    ret_val = False
    # checking len
    if(len(string) >= 8):
        ret_val = True
    if ret_val == False:
        return False
    ret_val = False
    # cheking for upper case
    for char in string:
        if char.isupper():
            ret_val = True
    if ret_val == False:
        return False
    ret_val = False
    #checking for lower case
    for char in string:
        if char.islower():
            ret_val = True
    if ret_val == False:
        return False
    ret_val = False
    # checking for number
    for char in string:
        if char.isdigit():
            ret_val = True
    if ret_val == False:
        return False
    ret_val = False
    # checking for special char
    for char in string:
        if char in chars:
            ret_val = True
    if ret_val == False:
        return False
    ret_val = False
    # checking for number
    for char in string:
        if char.isdigit():
            ret_val = True
    if ret_val == False:
        return False
    for char in string:
        if not (char in valid_characters):
            ret_val = False
    return ret_val
    
    



    