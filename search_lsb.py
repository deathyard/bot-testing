#!/usr/bin/env python3
import cv2
import numpy as np
from PIL import Image
import os
import re

def extract_all_lsb_text():
    """Extract LSBs from all frames and search for flags"""
    frames_dir = 'frames'
    if not os.path.exists(frames_dir):
        return
    
    frames = sorted([f for f in os.listdir(frames_dir) if f.endswith('.png')])
    
    all_lsb_text = []
    
    print(f"Processing {len(frames)} frames...")
    
    for frame_file in frames:
        frame_path = os.path.join(frames_dir, frame_file)
        try:
            img = Image.open(frame_path)
            img_array = np.array(img)
            
            # Extract LSBs from all channels
            if len(img_array.shape) == 3:
                for channel_idx in range(3):  # R, G, B
                    channel = img_array[:, :, channel_idx]
                    lsb_bits = channel & 1
                    
                    flat_bits = lsb_bits.flatten()
                    bit_string = ''.join([str(int(b)) for b in flat_bits])
                    
                    for i in range(0, len(bit_string) - 7, 8):
                        byte_val = int(bit_string[i:i+8], 2)
                        if 32 <= byte_val <= 126:
                            all_lsb_text.append(chr(byte_val))
        except Exception as e:
            continue
    
    combined_text = ''.join(all_lsb_text)
    
    print(f"Extracted {len(combined_text)} characters")
    
    # Search for flag patterns with various formats
    flag_patterns = [
        r'flag\{[A-Za-z0-9_]{10,}\}',
        r'FLAG\{[A-Za-z0-9_]{10,}\}',
        r'picoCTF\{[A-Za-z0-9_]{10,}\}',
        r'[A-Z]{3,}\{[A-Za-z0-9_]{10,}\}',
        r'flag:[A-Za-z0-9_]{10,}',
        r'FLAG:[A-Za-z0-9_]{10,}',
        r'[a-z]{4,}\{[A-Za-z0-9_]{10,}\}',  # lowercase flag
    ]
    
    print("\n=== Searching for flag patterns ===")
    found_flags = []
    for pattern in flag_patterns:
        matches = re.findall(pattern, combined_text)
        if matches:
            found_flags.extend(matches)
            print(f"Pattern {pattern}: {matches}")
    
    if found_flags:
        print(f"\n*** FLAGS FOUND: {found_flags} ***")
    else:
        print("\nNo flag patterns found. Showing sample of extracted text:")
        # Show sections that might contain flags
        for i in range(0, len(combined_text) - 50, 1000):
            sample = combined_text[i:i+200]
            if any(c.isalnum() for c in sample):
                print(f"Offset {i}: {sample}")
    
    # Also try searching for common CTF flag formats
    print("\n=== Searching for CTF flag formats ===")
    # Look for strings that start with common prefixes
    common_prefixes = ['flag', 'FLAG', 'pico', 'PICO', 'ctf', 'CTF']
    for prefix in common_prefixes:
        idx = combined_text.find(prefix)
        if idx != -1:
            # Extract surrounding text
            start = max(0, idx - 10)
            end = min(len(combined_text), idx + 100)
            context = combined_text[start:end]
            print(f"Found '{prefix}' at offset {idx}: {context}")

if __name__ == '__main__':
    extract_all_lsb_text()
