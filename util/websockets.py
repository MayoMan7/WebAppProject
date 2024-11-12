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
    print(f"mask bit = {mask_bit}")
    len = (bytes[1] & 127)
    payload_length = len
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
    frame = b""
    content_len = len(bytes)
    # content_len = 18446744073709551614 # testing
    first_byte = 0b10000001
    frame += first_byte.to_bytes(1,"big")
    second_byte = 0b00000000
    if content_len < 126:
        second_byte |= content_len
        frame += second_byte.to_bytes(1,"big")
    if content_len == 126:
        second_byte |= content_len
        frame += second_byte.to_bytes(1,"big")
        next_bytes = 0b0000000000000000
        next_bytes |= content_len
        frame += next_bytes.to_bytes(2,"big")
    if content_len > 126:
        second_byte |= 127
        frame += second_byte.to_bytes(1,"big")
        next_bytes = 0b0000000000000000000000000000000000000000000000000000000000000000
        next_bytes |= content_len
        frame += next_bytes.to_bytes(8,"big")
    frame += bytes
    return frame
    

print(generate_ws_frame(b"TEST"))

# fin bit = 1, opcode = 1 mask = 0, len = 4
parse_ws_frame(b'\x81\x04TEST')

print(compute_accept("D12+CDq1GMcX8NNQZRE/GQ==") == "pwi4T2+FJkdUgam0CMHGpniT88k=")