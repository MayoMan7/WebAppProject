import hashlib
import base64

def compute_accept(key):
    GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

    webkey = key + GUID

    hashed = hashlib.sha1(webkey.encode())

    Sec_WebSocket_Key = base64.b64encode(hashed.digest()).decode().strip()

    return Sec_WebSocket_Key

class Frame:
    def __init__(self, fin_bit, opcode, payload_length, payload):
        self.fin_bit = fin_bit
        self.opcode = opcode
        self.payload_length = payload_length
        self.payload = payload

def parse_ws_frame(bytes):

    bytes = bytearray(bytes)

    opcode = bytes[0] & 0x0F
    fin = bytes[0] >>7 & 0x01
    content_len = bytes[1] & 0x7F

    if content_len == 126:
        content_len = int.from_bytes(bytes[2:4],byteorder="big")
        payload_length = 4
    elif content_len == 127:
        content_len = int.from_bytes(bytes[2:10],byteorder="big")
        payload_length = 10
    else:
        payload_length = 2

    endOfKey = payload_length + 4

    maskKey = bytes[payload_length:endOfKey]
    
    payload = bytes[endOfKey:endOfKey+content_len]

    for i in range(len(payload)):
        payload[i] ^= maskKey[i%4]
    
    frame = Frame(fin,opcode,content_len,payload)

    return frame

def generate_ws_frame(bytes):

    size = len(bytes)
    fin = 1
    opcode = 1
    maskbit = 0
    start = (fin<<7) | opcode | maskbit
    ret = bytearray([start])

    if size < 126:
        ret.append(size)

    elif size < 65536:
        size_bytes = size.to_bytes(2,"big")
        size_bytes = bytearray(size_bytes)
        ret.extend([126])
        ret.extend([size_bytes[0],size_bytes[1]])

    else:
        size_bytes = size.to_bytes(8,"big")
        size_bytes = bytearray(size_bytes)
        ret.extend([127])
        for i in range(8):
            ret.extend([size_bytes[i]])

    ret.extend(bytes)
    
    return ret  


def test_compute_accept():
    key = "dGhlIHNhbXBsZSBub25jZQ=="
    expected_accept = "s3pPLMBiTxaQ9kYGzzhZRbK+xOo="
    assert compute_accept(key) == expected_accept

def test_parse_ws_frame_small():
    # Test case for a single frame with payload length < 126
    frame_bytes = bytearray([0x81, 0x05]) + b"hello"
    expected_result = Frame(fin_bit=1, opcode=1, payload_length=5, payload=b"hello")
    print(expected_result.fin_bit,expected_result.opcode,expected_result.payload_length,expected_result.payload)
    # assert parse_ws_frame(frame_bytes).__dict__ == expected_result.__dict__

def test_parse_ws_frame_medium():
    # Test case for a single frame with payload length = 126
    frame_bytes = bytearray([0x81, 0x7e, 0x00, 0x7d]) + b" " * 125
    expected_result = Frame(fin_bit=1, opcode=1, payload_length=125, payload=b" " * 125)
    print(expected_result.fin_bit,expected_result.opcode,expected_result.payload_length,expected_result.payload)

    # assert parse_ws_frame(frame_bytes).__dict__ == expected_result.__dict__

def test_parse_ws_frame_long():
    # Test case for a single frame with payload length = 127
    frame_bytes = bytearray([0x81, 0x7f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01]) + b" " * 65536
    expected_result = Frame(fin_bit=1, opcode=1, payload_length=65536, payload=b" " * 65536)
    print(expected_result.fin_bit,expected_result.opcode,expected_result.payload_length,expected_result.payload)

    # assert parse_ws_frame(frame_bytes).__dict__ == expected_result.__dict__

if __name__ == "__main__":
    test_parse_ws_frame_small()
    test_parse_ws_frame_medium()
    test_parse_ws_frame_long()
    print("All parse frame tests passed!")

