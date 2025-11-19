#!/usr/bin/env python3
import re
import sys

def analyze_video(filename):
    print(f"Analyzing {filename}...")
    
    with open(filename, 'rb') as f:
        data = f.read()
    
    print(f"File size: {len(data)} bytes")
    
    # Search for common flag patterns
    patterns = [
        rb'flag\{[^}]+\}',
        rb'FLAG\{[^}]+\}',
        rb'picoCTF\{[^}]+\}',
        rb'[A-Za-z0-9_]{20,}',
        rb'[A-Z]{5,}[A-Z0-9_]{10,}',  # Uppercase flags
    ]
    
    print("\n=== Searching for flag patterns ===")
    for pattern in patterns:
        matches = re.findall(pattern, data)
        for match in matches[:10]:  # Limit to first 10 matches
            try:
                decoded = match.decode('utf-8', errors='ignore')
                if len(decoded) > 10:  # Filter out short matches
                    print(f"Found: {decoded}")
            except:
                pass
    
    # Check for base64-like strings
    print("\n=== Searching for base64-like strings ===")
    base64_pattern = rb'[A-Za-z0-9+/]{20,}={0,2}'
    matches = re.findall(base64_pattern, data)
    for match in matches[:20]:
        try:
            decoded = match.decode('utf-8', errors='ignore')
            if len(decoded) > 15:
                print(f"Base64-like: {decoded[:50]}")
        except:
            pass
    
    # Check metadata areas (beginning and end of file)
    print("\n=== Checking file beginning ===")
    print(data[:500].decode('utf-8', errors='ignore'))
    
    print("\n=== Checking file end ===")
    print(data[-500:].decode('utf-8', errors='ignore'))
    
    # Look for ASCII strings in the entire file
    print("\n=== Extracting readable ASCII strings ===")
    ascii_strings = re.findall(rb'[ -~]{10,}', data)
    for s in ascii_strings[:50]:
        decoded = s.decode('utf-8', errors='ignore')
        if any(keyword in decoded.lower() for keyword in ['flag', 'secret', 'key', 'password', 'hidden']):
            print(f"Interesting string: {decoded}")
    
    # Check for LSB steganography (extract LSBs)
    print("\n=== Checking LSB steganography ===")
    lsb_bits = ''.join([str(byte & 1) for byte in data[:10000]])  # Check first 10KB
    # Try to find readable text in LSBs
    for i in range(0, len(lsb_bits) - 8, 8):
        byte_val = int(lsb_bits[i:i+8], 2)
        if 32 <= byte_val <= 126:  # Printable ASCII
            print(f"LSB byte at offset {i//8}: {chr(byte_val)}", end='')
    print()
    
    # Check MP4 atoms/boxes for hidden data
    print("\n=== Checking MP4 structure ===")
    i = 0
    while i < len(data) - 8:
        size = int.from_bytes(data[i:i+4], 'big')
        box_type = data[i+4:i+8].decode('utf-8', errors='ignore')
        if size > 0 and size < len(data) and box_type.isprintable():
            print(f"Box: {box_type}, size: {size}")
            # Check if this box contains text
            if i + size < len(data):
                box_data = data[i+8:i+size]
                text_in_box = re.findall(rb'[ -~]{10,}', box_data)
                for text in text_in_box[:5]:
                    decoded = text.decode('utf-8', errors='ignore')
                    if len(decoded) > 10:
                        print(f"  Text in {box_type}: {decoded[:100]}")
        i += size if size > 0 else 8
        if i >= len(data) - 8:
            break

if __name__ == '__main__':
    analyze_video('nature.mp4')
