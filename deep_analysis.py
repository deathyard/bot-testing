#!/usr/bin/env python3
import re
import struct

def extract_lsb_text(data, max_bytes=10000):
    """Extract text from LSBs of bytes"""
    lsb_string = ''
    for byte in data[:max_bytes]:
        lsb_string += str(byte & 1)
    
    # Try to extract ASCII characters
    text = ''
    for i in range(0, len(lsb_string) - 7, 8):
        byte_val = int(lsb_string[i:i+8], 2)
        if 32 <= byte_val <= 126:
            text += chr(byte_val)
        else:
            text += '.'
    
    # Look for flag patterns in extracted text
    flag_patterns = [
        r'flag\{[^}]+\}',
        r'FLAG\{[^}]+\}',
        r'picoCTF\{[^}]+\}',
        r'[A-Z]{3,}\{[A-Za-z0-9_]{10,}\}',
    ]
    
    for pattern in flag_patterns:
        matches = re.findall(pattern, text)
        if matches:
            print(f"Found flag in LSB: {matches}")
    
    return text[:500]  # Return first 500 chars

def check_metadata_fields(data):
    """Check MP4 metadata fields more carefully"""
    # Look for 'data' atoms which often contain metadata
    i = 0
    while i < len(data) - 20:
        # Look for 'data' atom marker
        if data[i:i+4] == b'data':
            # Next 4 bytes might be size or flags
            # Then the actual data
            if i + 8 < len(data):
                metadata = data[i+8:i+100]  # Check next 100 bytes
                text = metadata.decode('utf-8', errors='ignore')
                if any(c.isalnum() for c in text) and len(text.strip()) > 5:
                    # Check for flag patterns
                    flag_patterns = [
                        r'flag\{[^}]+\}',
                        r'FLAG\{[^}]+\}',
                        r'picoCTF\{[^}]+\}',
                    ]
                    for pattern in flag_patterns:
                        matches = re.findall(pattern, text)
                        if matches:
                            print(f"Found flag in metadata: {matches}")
                    if 'flag' in text.lower() or 'FLAG' in text:
                        print(f"Metadata text: {text[:200]}")
        i += 1

def check_binary_patterns(data):
    """Check for patterns that might indicate hidden data"""
    # Check for XOR patterns
    # Check for repeating patterns
    # Check for unusual byte sequences
    
    # Look for strings that might be flags
    # Try different encodings
    for encoding in ['utf-8', 'latin-1', 'ascii']:
        try:
            text = data.decode(encoding, errors='ignore')
            # Search for flag patterns
            patterns = [
                r'flag\{[A-Za-z0-9_]{10,}\}',
                r'FLAG\{[A-Za-z0-9_]{10,}\}',
                r'picoCTF\{[A-Za-z0-9_]{10,}\}',
            ]
            for pattern in patterns:
                matches = re.findall(pattern, text)
                if matches:
                    print(f"Found flag ({encoding}): {matches}")
        except:
            pass

def main():
    with open('nature.mp4', 'rb') as f:
        data = f.read()
    
    print("=== Extracting LSB text ===")
    lsb_text = extract_lsb_text(data)
    print(f"LSB text (first 200 chars): {lsb_text[:200]}")
    
    print("\n=== Checking metadata fields ===")
    check_metadata_fields(data)
    
    print("\n=== Checking binary patterns ===")
    check_binary_patterns(data)
    
    # Also check if flag might be in file name or path embedded in file
    print("\n=== Checking for embedded file paths/names ===")
    path_pattern = rb'[A-Za-z0-9_/\\\.]{10,}'
    matches = re.findall(path_pattern, data)
    for match in matches[:20]:
        decoded = match.decode('utf-8', errors='ignore')
        if 'flag' in decoded.lower() or len(decoded) > 20:
            print(f"Path-like string: {decoded}")

if __name__ == '__main__':
    main()
