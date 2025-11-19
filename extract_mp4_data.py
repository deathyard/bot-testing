#!/usr/bin/env python3
import struct
import re

def read_mp4_box(data, offset):
    """Read MP4 box header"""
    if offset + 8 > len(data):
        return None, None, offset
    
    size = struct.unpack('>I', data[offset:offset+4])[0]
    box_type = data[offset+4:offset+8]
    
    return size, box_type, offset + 8

def extract_box_data(data, box_type):
    """Extract all data from boxes of a specific type"""
    results = []
    offset = 0
    
    while offset < len(data) - 8:
        size, box, new_offset = read_mp4_box(data, offset)
        
        if size == 0 or size > len(data) - offset:
            break
            
        if box == box_type:
            # Extract box data (skip 8-byte header)
            box_data = data[offset+8:offset+size]
            results.append((offset, box_data))
        
        offset += size
    
    return results

def analyze_video():
    with open('nature.mp4', 'rb') as f:
        data = f.read()
    
    print("=== Extracting 'free' box data ===")
    free_boxes = extract_box_data(data, b'free')
    for i, (offset, box_data) in enumerate(free_boxes):
        print(f"\nFree box {i+1} at offset {offset}, size: {len(box_data)}")
        # Look for readable strings
        strings = re.findall(rb'[a-zA-Z0-9_\-{}]{10,}', box_data)
        for s in strings[:20]:
            try:
                decoded = s.decode('utf-8', errors='ignore')
                if 'flag' in decoded.lower() or 'ctf' in decoded.lower():
                    print(f"  FLAG FOUND: {decoded}")
                elif len(decoded) > 10:
                    print(f"  String: {decoded}")
            except:
                pass
        # Show hex dump of first 200 bytes
        print(f"  First 200 bytes (hex): {box_data[:200].hex()}")
        # Check for flag pattern
        if b'flag{' in box_data.lower() or b'ctf{' in box_data.lower():
            flag_match = re.search(rb'[fF][lL][aA][gG]\{[^}]+\}', box_data, re.IGNORECASE)
            if flag_match:
                print(f"  *** FLAG FOUND: {flag_match.group().decode('utf-8', errors='ignore')} ***")
    
    print("\n=== Extracting 'skip' box data ===")
    skip_boxes = extract_box_data(data, b'skip')
    for i, (offset, box_data) in enumerate(skip_boxes):
        print(f"\nSkip box {i+1} at offset {offset}, size: {len(box_data)}")
        strings = re.findall(rb'[a-zA-Z0-9_\-{}]{10,}', box_data)
        for s in strings[:20]:
            try:
                decoded = s.decode('utf-8', errors='ignore')
                if 'flag' in decoded.lower() or 'ctf' in decoded.lower():
                    print(f"  FLAG FOUND: {decoded}")
                elif len(decoded) > 10:
                    print(f"  String: {decoded}")
            except:
                pass
        if b'flag{' in box_data.lower() or b'ctf{' in box_data.lower():
            flag_match = re.search(rb'[fF][lL][aA][gG]\{[^}]+\}', box_data, re.IGNORECASE)
            if flag_match:
                print(f"  *** FLAG FOUND: {flag_match.group().decode('utf-8', errors='ignore')} ***")
    
    print("\n=== Searching entire file for flag patterns ===")
    # More comprehensive search
    patterns = [
        rb'flag\{[a-zA-Z0-9_\-]+\}',
        rb'FLAG\{[a-zA-Z0-9_\-]+\}',
        rb'ctf\{[a-zA-Z0-9_\-]+\}',
        rb'CTF\{[a-zA-Z0-9_\-]+\}',
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, data, re.IGNORECASE)
        for match in matches:
            try:
                flag = match.group().decode('utf-8', errors='ignore')
                print(f"*** FLAG FOUND at offset {match.start()}: {flag} ***")
            except:
                print(f"Found flag (hex) at offset {match.start()}: {match.group().hex()}")
    
    # Check for base64 encoded flags
    print("\n=== Checking for base64 encoded data ===")
    base64_pattern = rb'[A-Za-z0-9+/]{30,}={0,2}'
    matches = re.finditer(base64_pattern, data)
    for i, match in enumerate(matches):
        if i > 50:  # Limit to first 50
            break
        try:
            b64_str = match.group().decode('ascii')
            # Try to decode
            import base64
            try:
                decoded = base64.b64decode(b64_str)
                decoded_str = decoded.decode('utf-8', errors='ignore')
                if 'flag' in decoded_str.lower() or 'ctf' in decoded_str.lower():
                    print(f"Base64 at offset {match.start()}: {b64_str[:50]}...")
                    print(f"  Decoded: {decoded_str}")
            except:
                pass
        except:
            pass

if __name__ == '__main__':
    analyze_video()
