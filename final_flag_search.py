#!/usr/bin/env python3
"""
Final comprehensive flag search
"""
import re
import cv2
import numpy as np
from PIL import Image
import os

def search_in_file():
    """Search directly in the MP4 file"""
    with open('nature.mp4', 'rb') as f:
        data = f.read()
    
    print("=== Searching in raw file ===")
    # Try all possible flag patterns
    patterns = [
        rb'flag\{[A-Za-z0-9_]{10,}\}',
        rb'FLAG\{[A-Za-z0-9_]{10,}\}',
        rb'picoCTF\{[A-Za-z0-9_]{10,}\}',
        rb'[a-z]{4}\{[A-Za-z0-9_]{15,}\}',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, data)
        if matches:
            for match in matches:
                print(f"FOUND: {match.decode('utf-8', errors='ignore')}")

def search_in_frames_lsb():
    """Search in frame LSBs"""
    frames_dir = 'frames'
    if not os.path.exists(frames_dir):
        print("Frames directory not found")
        return
    
    frames = sorted([f for f in os.listdir(frames_dir) if f.endswith('.png')])
    
    print(f"\n=== Searching in {len(frames)} frames LSBs ===")
    
    # Extract LSBs from red channel of all frames
    all_chars = []
    for frame_file in frames:
        try:
            img = cv2.imread(os.path.join(frames_dir, frame_file))
            if img is not None:
                red_channel = img[:, :, 2]  # BGR format, so index 2 is red
                lsb_bits = red_channel & 1
                flat = lsb_bits.flatten()
                bit_string = ''.join([str(int(b)) for b in flat])
                for i in range(0, len(bit_string) - 7, 8):
                    byte_val = int(bit_string[i:i+8], 2)
                    if 32 <= byte_val <= 126:
                        all_chars.append(chr(byte_val))
        except:
            continue
    
    combined = ''.join(all_chars)
    print(f"Extracted {len(combined)} characters from LSBs")
    
    # Search for flags
    patterns = [
        r'flag\{[A-Za-z0-9_]{10,}\}',
        r'FLAG\{[A-Za-z0-9_]{10,}\}',
        r'picoCTF\{[A-Za-z0-9_]{10,}\}',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, combined)
        if matches:
            print(f"*** FLAG FOUND: {matches} ***")
            return matches
    
    # If no standard format found, look for any flag-like pattern
    flag_idx = combined.lower().find('flag{')
    if flag_idx != -1:
        # Extract potential flag
        potential_flag = combined[flag_idx:flag_idx+100]
        print(f"Found 'flag{{' at position {flag_idx}: {potential_flag}")
        # Try to extract the flag
        match = re.search(r'flag\{[^}]+\}', potential_flag, re.IGNORECASE)
        if match:
            print(f"*** EXTRACTED FLAG: {match.group()} ***")

if __name__ == '__main__':
    search_in_file()
    search_in_frames_lsb()
