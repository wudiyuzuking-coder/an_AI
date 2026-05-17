import struct
import zlib

def create_png(filename, width, height, r, g, b):
    def chunk(chunk_type, data):
        c = chunk_type + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
    
    signature = b'\x89PNG\r\n\x1a\n'
    ihdr = chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0))
    
    raw_data = b''
    for y in range(height):
        raw_data += b'\x00'
        for x in range(width):
            raw_data += bytes([r, g, b])
    
    idat = chunk(b'IDAT', zlib.compress(raw_data))
    iend = chunk(b'IEND', b'')
    
    with open(filename, 'wb') as f:
        f.write(signature + ihdr + idat + iend)

create_png('d:\\Code\\an_AI\\miniapp\\images\\chat.png', 24, 24, 153, 153, 153)
create_png('d:\\Code\\an_AI\\miniapp\\images\\chat-active.png', 24, 24, 76, 175, 80)
create_png('d:\\Code\\an_AI\\miniapp\\images\\feedback.png', 24, 24, 153, 153, 153)
create_png('d:\\Code\\an_AI\\miniapp\\images\\feedback-active.png', 24, 24, 76, 175, 80)
print("Icons created!")
