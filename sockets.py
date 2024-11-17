from util.websockets import compute_accept
from util.websockets import parse_ws_frame
from util.websockets import generate_ws_frame
from chat import get_username
from chat import save_message
import json
import html


active_clients = []

def handshake(request,handler):
    print("WEBSOCKET HANDSHAKE")
    key = request.headers.get("Sec-WebSocket-Key",None)
    key = compute_accept(key)
    username = get_username(request)
    # print(request.headers)
    # print(request.cookies)
    browser_cookie = request.cookies["browser_cookie"]
    # print(browser_cookie)
    # print(username)
    response = (
        "HTTP/1.1 101 Switching Protocols\r\n"
        "X-Content-Type-Options: nosniff\r\n"
        "Connection: Upgrade\r\n"
        "Upgrade: websocket\r\n"
        f"Sec-WebSocket-Accept: {key}\r\n"
        "\r\n"
    )
    handler.request.sendall(response.encode())
    active_clients.append(handler)

    total_data = b""
    continuation_payload = b""
    while True:
        data = handler.request.recv(2048)
        print("RECIVING")
        if not data:
            print("BREAKING LOOP")
            break
        total_data += data
        while total_data != b"":
            #get the size of the frame manualy
            frame_size = get_frame_size(total_data)
            # if we dont have enough data were gonna break and bugger
            if len(total_data) < frame_size:
                break
            frame  = parse_ws_frame(total_data[:frame_size])
            # print(total_data)
            finbit = frame.fin_bit
            opcode = frame.opcode
            payload_len = frame.payload_length
            # print(f"The len of all the data i have recived {len(total_data)}")
            # print(f"the len of the frame I should be parsing {frame_size}")
            # adjusting data
            total_data = total_data[frame_size:]
            print(f"finbit {finbit} opcode {opcode} payload_len {payload_len}")
            # closing conection
            if opcode == 8:
                print("CLOSING CONECTION")
                active_clients.remove(handler)
                break
            if finbit == 0:
                continuation_payload += frame.payload
                continue
            if finbit == 1:
                if opcode == 0:
                    continuation_payload += frame.payload
                    print(continuation_payload)
                    # print(f"{len(continuation_payload)} len of continuation paylaod")
                    payload = json.loads(continuation_payload)
                    continuation_payload = b""
                else:
                    payload = json.loads(frame.payload)
            print(payload)

            # actualy sending it out
            if payload["messageType"] == "chatMessage":
                message = html.escape(payload["message"])
                send_message(username,message, browser_cookie)
            # ao
            if payload["messageType"] == "webRTC-offer" or payload["messageType"] == "webRTC-answer" or payload["messageType"] == "webRTC-candidate":
                frame = generate_ws_frame(json.dumps(payload).encode("utf-8"))
                other_client = (active_clients.index(handler) + 1) % 2
                print(active_clients)
                active_clients[other_client].request.sendall(frame)

        
        
def send_message(username, message, browser_cookie):
    print(f"Sending message")
    id = save_message(username,message, browser_cookie)
    payload = {
        'messageType': 'chatMessage', 
        'username': username, 
        'message': message, 
        'id': id
    }
    payload = json.dumps(payload).encode("utf-8")
    frame = generate_ws_frame(payload)
    # print(payload)
    # print(frame)
    for client in active_clients:
        client.request.sendall(frame)
        print(client)




def get_frame_size(data):
    # print(f"data = {data}")
    # print(f"type = {type(data)}")
    # print(f"data = {len(data)}")
    length = (data[1] & 127)
    mask_bit = (data[1] & 128)>> 7
    payload_length = length
    if length == 126:
        payload_length = (data[2] << 8) | data[3]
    if length == 127:
        payload_length = ((data[2] << 56) | (data[3] << 48) | (data[4] << 40) | (data[5] << 32) | (data[6] << 24) | (data[7] << 16) | (data[8] << 8) |data[9])
    size = 0
    #fin bit/op cod
    size += 1
    #mask
    if mask_bit == 1:
        size += 4
    if payload_length < 126:
        size += 1
    if payload_length >= 126 and payload_length < 65536:
        size += 3
    if payload_length >= 65536:
        size += 9
    return size + payload_length

