#!/usr/bin/env python3
import re

def extract_lsb_strings(data, num_bits=8):
    """Extract strings from LSB steganography"""
    results = []
    
    # Try extracting every 8 bits as ASCII
    for start_offset in range(8):
        bits = []
        for i in range(start_offset, len(data) * 8, 8):
            byte_idx = i // 8
            bit_pos = i % 8
            if byte_idx < len(data):
                bit = (data[byte_idx] >> bit_pos) & 1
                bits.append(str(bit))
        
        # Convert bits to bytes
        bit_string = ''.join(bits)
        for i in range(0, len(bit_string) - 7, 8):
            byte_val = int(bit_string[i:i+8], 2)
            if 32 <= byte_val <= 126:  # Printable ASCII
                results.append((start_offset, byte_val))
    
    # Try extracting consecutive LSBs
    lsb_bits = ''.join([str(byte & 1) for byte in data])
    for i in range(0, len(lsb_bits) - 7, 8):
        byte_val = int(lsb_bits[i:i+8], 2)
        if 32 <= byte_val <= 126:
            if i // 8 < 200:  # Print first 200 bytes
                print(f"LSB byte {i//8}: {chr(byte_val)}", end='')
    print()
    
    return results

def check_mp4_boxes(data):
    """Parse MP4 boxes and check for hidden data"""
    i = 0
    boxes = []
    while i < len(data) - 8:
        if i + 4 > len(data):
            break
        size = int.from_bytes(data[i:i+4], 'big')
        if size == 0 or size > len(data) or size < 8:
            i += 1
            continue
        
        if i + 8 > len(data):
            break
            
        box_type = data[i+4:i+8].decode('utf-8', errors='ignore')
        
        if all(c.isprintable() or c == ' ' for c in box_type):
            box_data = data[i+8:i+size] if i+size <= len(data) else data[i+8:]
            boxes.append((box_type, i, size, box_data))
            
            # Check for text in this box
            text_matches = re.findall(rb'[ -~]{10,}', box_data)
            for match in text_matches[:10]:
                decoded = match.decode('utf-8', errors='ignore')
                if len(decoded) > 10 and any(c.isalnum() for c in decoded):
                    print(f"\nBox '{box_type}' at offset {i}:")
                    print(f"  Found text: {decoded[:200]}")
        
        i += size
        if i >= len(data) - 8:
            break
    
    return boxes

def main():
    with open('nature.mp4', 'rb') as f:
        data = f.read()
    
    print("=== Extracting LSB steganography ===")
    extract_lsb_strings(data)
    
    print("\n=== Checking MP4 boxes ===")
    boxes = check_mp4_boxes(data)
    
    print("\n=== Searching entire file for flag patterns ===")
    # More comprehensive flag search
    patterns = [
        rb'flag\{[A-Za-z0-9_]{10,}\}',
        rb'FLAG\{[A-Za-z0-9_]{10,}\}',
        rb'picoCTF\{[A-Za-z0-9_]{10,}\}',
        rb'[A-Z]{3,}\{[A-Za-z0-9_]{10,}\}',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, data)
        for match in matches:
            decoded = match.decode('utf-8', errors='ignore')
            print(f"FLAG FOUND: {decoded}")
    
    # Check for base64 encoded flags
    print("\n=== Checking for base64 encoded data ===")
    base64_pattern = rb'[A-Za-z0-9+/]{30,}={0,2}'
    matches = re.findall(base64_pattern, data)
    for match in matches[:10]:
        decoded = match.decode('utf-8', errors='ignore')
        if len(decoded) > 20:
            print(f"Base64: {decoded[:100]}")

if __name__ == '__main__':
    main()
