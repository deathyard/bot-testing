#!/usr/bin/env python3
import re
import struct

def final_comprehensive_scan(filename):
    """Final comprehensive scan of the video file"""
    
    with open(filename, 'rb') as f:
        data = f.read()
    
    print(f"File size: {len(data)} bytes\n")
    
    # 1. Direct search with various patterns
    patterns = [
        rb'flag\{[^}]+\}',
        rb'FLAG\{[^}]+\}',
        rb'ctf\{[^}]+\}',
        rb'CTF\{[^}]+\}',
        rb'flag_[a-zA-Z0-9_]+',
        rb'FLAG_[a-zA-Z0-9_]+',
    ]
    
    print("=== Direct pattern search ===")
    for pattern in patterns:
        matches = list(re.finditer(pattern, data, re.IGNORECASE))
        for m in matches:
            try:
                flag = m.group().decode('utf-8', errors='ignore')
                print(f"Found: {flag} at offset {m.start()}")
                return flag
            except:
                pass
    
    # 2. Check for flag split across bytes (every Nth byte)
    print("\n=== Checking every Nth byte patterns ===")
    for n in [1, 2, 3, 4, 8]:
        extracted = bytearray()
        for i in range(0, min(len(data), 100000), n):
            extracted.append(data[i])
        
        try:
            text = extracted.decode('utf-8', errors='ignore')
            flag_match = re.search(r'[fF][lL][aA][gG]\{[^}]+\}', text, re.IGNORECASE)
            if flag_match:
                print(f"FLAG found with step {n}: {flag_match.group()}")
                return flag_match.group()
        except:
            pass
    
    # 3. Check XOR with various keys
    print("\n=== XOR with common keys ===")
    keys = [b'key', b'KEY', b'flag', b'FLAG', b'ctf', b'CTF', b'secret', b'SECRET', b'password', b'PASSWORD']
    for key in keys:
        xored = bytearray()
        for i in range(min(len(data), 50000)):
            xored.append(data[i] ^ key[i % len(key)])
        
        try:
            text = xored.decode('utf-8', errors='ignore')
            flag_match = re.search(r'[fF][lL][aA][gG]\{[^}]+\}', text, re.IGNORECASE)
            if flag_match:
                print(f"FLAG with XOR key '{key.decode()}': {flag_match.group()}")
                return flag_match.group()
        except:
            pass
    
    # 4. Check MP4 boxes more carefully
    print("\n=== MP4 box analysis ===")
    offset = 0
    while offset < len(data) - 8:
        if offset + 8 > len(data):
            break
        
        size = struct.unpack('>I', data[offset:offset+4])[0]
        if size == 0 or size > len(data) - offset:
            break
        
        box_type = data[offset+4:offset+8]
        box_data = data[offset+8:offset+size] if size > 8 else b''
        
        # Check interesting boxes
        if box_type in [b'free', b'skip', b'udta', b'meta', b'uuid']:
            # Search in box data
            flag_match = re.search(rb'[fF][lL][aA][gG]\{[^}]+\}', box_data, re.IGNORECASE)
            if flag_match:
                try:
                    flag = flag_match.group().decode('utf-8', errors='ignore')
                    print(f"FLAG in {box_type.decode()} box: {flag}")
                    return flag
                except:
                    pass
        
        offset += size
    
    # 5. Check for base64/hex encoded flags
    print("\n=== Checking encoded data ===")
    import base64
    
    # Base64
    b64_pattern = rb'[A-Za-z0-9+/]{30,}={0,2}'
    for match in re.finditer(b64_pattern, data):
        try:
            b64_str = match.group().decode('ascii')
            decoded = base64.b64decode(b64_str)
            decoded_str = decoded.decode('utf-8', errors='ignore')
            flag_match = re.search(r'[fF][lL][aA][gG]\{[^}]+\}', decoded_str, re.IGNORECASE)
            if flag_match:
                print(f"FLAG in base64: {flag_match.group()}")
                return flag_match.group()
        except:
            pass
    
    # Hex
    hex_pattern = rb'[0-9a-fA-F]{40,}'
    for match in re.finditer(hex_pattern, data):
        try:
            hex_str = match.group().decode('ascii')
            decoded = bytes.fromhex(hex_str)
            decoded_str = decoded.decode('utf-8', errors='ignore')
            flag_match = re.search(r'[fF][lL][aA][gG]\{[^}]+\}', decoded_str, re.IGNORECASE)
            if flag_match:
                print(f"FLAG in hex: {flag_match.group()}")
                return flag_match.group()
        except:
            pass
    
    print("\nNo flag found")
    return None

if __name__ == '__main__':
    result = final_comprehensive_scan('nature.mp4')
    if result:
        print(f"\n*** FINAL FLAG: {result} ***")
