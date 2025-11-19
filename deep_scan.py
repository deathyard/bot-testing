#!/usr/bin/env python3
import re
import base64

def scan_file(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    
    print(f"File size: {len(data)} bytes\n")
    
    # 1. Direct flag pattern search (case insensitive)
    print("=== Direct flag pattern search ===")
    flag_regex = rb'[fF][lL][aA][gG]\{[^}]+\}'
    matches = list(re.finditer(flag_regex, data))
    if matches:
        for m in matches:
            print(f"Found: {m.group().decode('utf-8', errors='ignore')} at offset {m.start()}")
    else:
        print("No direct flag patterns found")
    
    # 2. Check every 1000th byte for patterns
    print("\n=== Sampling file at intervals ===")
    for offset in range(0, len(data), 10000):
        chunk = data[offset:offset+1000]
        # Look for readable text
        text = ''.join([chr(b) if 32 <= b <= 126 else '.' for b in chunk])
        if 'flag' in text.lower() or 'ctf' in text.lower():
            print(f"Interesting text at offset {offset}:")
            print(text[:200])
    
    # 3. LSB extraction from entire file (more carefully)
    print("\n=== LSB extraction (full file) ===")
    lsb_bytes = bytes([b & 1 for b in data])
    # Group into bytes
    lsb_data = bytearray()
    for i in range(0, len(lsb_bytes) - 7, 8):
        byte_val = 0
        for j in range(8):
            if i + j < len(lsb_bytes):
                byte_val |= (lsb_bytes[i + j] << j)
        lsb_data.append(byte_val)
    
    # Search for flag in LSB data
    lsb_str = lsb_data.decode('utf-8', errors='ignore')
    flag_match = re.search(r'[fF][lL][aA][gG]\{[^}]+\}', lsb_str)
    if flag_match:
        print(f"FLAG in LSB: {flag_match.group()}")
    else:
        # Show first 500 chars of LSB
        readable = ''.join([c if 32 <= ord(c) <= 126 else '.' for c in lsb_str[:500]])
        if 'flag' in readable.lower():
            print(f"LSB data (first 500): {readable}")
    
    # 4. Check for XOR encoding
    print("\n=== Checking XOR patterns ===")
    common_keys = [b'flag', b'FLAG', b'ctf', b'CTF', b'key', b'KEY', b'secret', b'SECRET']
    for key in common_keys:
        xored = bytearray()
        for i, byte in enumerate(data[:10000]):  # Check first 10KB
            xored.append(byte ^ key[i % len(key)])
        xored_str = xored.decode('utf-8', errors='ignore')
        if 'flag{' in xored_str.lower():
            flag_match = re.search(r'[fF][lL][aA][gG]\{[^}]+\}', xored_str, re.IGNORECASE)
            if flag_match:
                print(f"FLAG found with XOR key '{key.decode()}': {flag_match.group()}")
    
    # 5. Check for data appended at the end
    print("\n=== Checking end of file ===")
    tail = data[-5000:]
    tail_str = tail.decode('utf-8', errors='ignore')
    flag_match = re.search(r'[fF][lL][aA][gG]\{[^}]+\}', tail_str, re.IGNORECASE)
    if flag_match:
        print(f"FLAG at end of file: {flag_match.group()}")
    else:
        # Show readable parts
        readable_tail = ''.join([c if 32 <= ord(c) <= 126 else '.' for c in tail_str])
        if 'flag' in readable_tail.lower() or len([c for c in readable_tail if c.isalnum()]) > 50:
            print(f"End of file (readable): {readable_tail[-200:]}")
    
    # 6. Check MP4 metadata boxes more carefully
    print("\n=== Checking MP4 metadata ===")
    # Look for 'udta' (user data) and 'meta' boxes
    udta_pos = data.find(b'udta')
    if udta_pos != -1:
        print(f"Found 'udta' at offset {udta_pos}")
        udta_section = data[udta_pos:udta_pos+2000]
        udta_str = udta_section.decode('utf-8', errors='ignore')
        flag_match = re.search(r'[fF][lL][aA][gG]\{[^}]+\}', udta_str, re.IGNORECASE)
        if flag_match:
            print(f"FLAG in udta: {flag_match.group()}")
        else:
            readable = ''.join([c if 32 <= ord(c) <= 126 else '.' for c in udta_str])
            if 'flag' in readable.lower() or len([c for c in readable if c.isalnum()]) > 20:
                print(f"udta content: {readable[:300]}")
    
    # 7. Check for steganography in specific byte positions
    print("\n=== Checking byte position patterns ===")
    # Sometimes flags are hidden at specific offsets
    for offset in [0, 100, 1000, 10000, 100000, len(data)//2, len(data)-1000]:
        if offset < len(data):
            chunk = data[offset:offset+100]
            chunk_str = chunk.decode('utf-8', errors='ignore')
            if 'flag{' in chunk_str.lower():
                flag_match = re.search(r'[fF][lL][aA][gG]\{[^}]+\}', chunk_str, re.IGNORECASE)
                if flag_match:
                    print(f"FLAG at offset {offset}: {flag_match.group()}")

if __name__ == '__main__':
    scan_file('nature.mp4')
