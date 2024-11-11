import base64
import hashlib

def compute_accept(key):
    GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    key+= GUID
    return base64.b64encode(hashlib.sha1(key.encode()).digest()).decode("utf-8")


class Frame:
    def __init__(self,fin_bit,opcode,payload_length,payload):
        self.fin_bit = fin_bit
        self.opcode = opcode
        self.payload_length = payload_length
        self.payload = payload

def parse_ws_frame(bytes):
    fin_bit = (bytes[0] & 128)>> 7
    opcode = (bytes[0] & 15)
    print(f"fin bit = {fin_bit}")
    print(f"opcode = {opcode}")
    mask_bit = (bytes[1] & 128)>> 7
    len = (bytes[1] & 127)
    next_byte = 2
    if len == 126:
        payload_length = (bytes[2] << 8) | bytes[3]
        next_byte = 4
    if len == 127:
        payload_length = ((bytes[2] << 56) | (bytes[3] << 48) | (bytes[4] << 40) | (bytes[5] << 32) | (bytes[6] << 24) | (bytes[7] << 16) | (bytes[8] << 8) |bytes[9])
        next_byte = 10
    print(f"real_len = {payload_length}")
    if mask_bit == 1:
        masking_key = bytes[next_byte:next_byte+4]
        next_byte = next_byte+4
        print(f"masking_key = {masking_key.hex()}")
    payload = bytes[next_byte:]
    if mask_bit == 1:
        unmasked = b""
        for i in range(payload_length):
            unmasked += (payload[i] ^ masking_key[i % 4]).to_bytes(1,"big")
        payload = unmasked

    print(f"payload = {payload}")
    return Frame(fin_bit,opcode,payload_length,payload)


def generate_ws_frame(bytes):
    first_byte = 0b10000001
    print(first_byte.to_bytes(1,"big"))
    

generate_ws_frame("temp")



# Test Compute
# print(f" Testing compute_accept: {compute_accept('6dvvbSIGRQF/+IFgdB9nxw==') == '3QyF2DAlHFXVL00GOq9fyBQHotc='}")