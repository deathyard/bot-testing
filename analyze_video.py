#!/usr/bin/env python3
import sys
import re

def analyze_video_file(filename):
    """Analyze video file for hidden flags"""
    
    print(f"Analyzing {filename}...")
    
    # Read the entire file
    with open(filename, 'rb') as f:
        data = f.read()
    
    print(f"File size: {len(data)} bytes")
    
    # 1. Search for common flag patterns in raw bytes
    print("\n=== Searching for flag patterns ===")
    flag_patterns = [
        rb'flag\{[^}]+\}',
        rb'FLAG\{[^}]+\}',
        rb'ctf\{[^}]+\}',
        rb'CTF\{[^}]+\}',
        rb'flag_[a-zA-Z0-9_]+',
        rb'FLAG_[a-zA-Z0-9_]+',
    ]
    
    for pattern in flag_patterns:
        matches = re.findall(pattern, data, re.IGNORECASE)
        if matches:
            for match in matches:
                try:
                    print(f"Found: {match.decode('utf-8', errors='ignore')}")
                except:
                    print(f"Found (hex): {match.hex()}")
    
    # 2. Extract all readable strings
    print("\n=== Extracting readable strings ===")
    strings = re.findall(rb'[a-zA-Z0-9_\-]{10,}', data)
    unique_strings = set(strings)
    for s in sorted(unique_strings):
        try:
            decoded = s.decode('utf-8', errors='ignore')
            if any(keyword in decoded.lower() for keyword in ['flag', 'ctf', 'secret', 'hidden']):
                print(f"Interesting string: {decoded}")
        except:
            pass
    
    # 3. Check for LSB steganography in first few KB
    print("\n=== Checking LSB steganography (first 8KB) ===")
    sample = data[:8192]
    lsb_bits = ''.join([str(byte & 1) for byte in sample])
    # Look for ASCII patterns in LSB
    for i in range(0, len(lsb_bits) - 7, 8):
        byte_bits = lsb_bits[i:i+8]
        if len(byte_bits) == 8:
            char_code = int(byte_bits, 2)
            if 32 <= char_code <= 126:  # Printable ASCII
                print(f"LSB byte at offset {i//8}: {chr(char_code)}", end='')
    print()
    
    # 4. Check file structure for hidden data
    print("\n=== Checking file structure ===")
    # Look for unusual chunks or metadata
    mp4_boxes = ['ftyp', 'mdat', 'moov', 'free', 'skip', 'udta', 'meta']
    for box in mp4_boxes:
        pattern = box.encode('ascii')
        positions = [i for i in range(len(data)) if data[i:i+len(pattern)] == pattern]
        if positions:
            print(f"Found '{box}' box at positions: {positions[:5]}")
    
    # 5. Check end of file for appended data
    print("\n=== Checking end of file ===")
    tail = data[-1000:]
    tail_strings = re.findall(rb'[a-zA-Z0-9_\-]{5,}', tail)
    for s in tail_strings:
        try:
            decoded = s.decode('utf-8', errors='ignore')
            if len(decoded) > 5:
                print(f"End of file string: {decoded}")
        except:
            pass
    
    # 6. Check for base64 encoded data
    print("\n=== Checking for base64 patterns ===")
    base64_pattern = rb'[A-Za-z0-9+/]{20,}={0,2}'
    matches = re.findall(base64_pattern, data)
    for match in matches[:10]:  # Check first 10 matches
        try:
            decoded = match.decode('ascii')
            if len(decoded) > 20:
                print(f"Possible base64: {decoded[:50]}...")
        except:
            pass

if __name__ == '__main__':
    analyze_video_file('nature.mp4')
