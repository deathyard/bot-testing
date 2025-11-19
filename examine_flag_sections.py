#!/usr/bin/env python3
import cv2
import numpy as np
from PIL import Image
import os
import re

def extract_and_search():
    """Extract LSBs and search around flag occurrences"""
    frames_dir = 'frames'
    frames = sorted([f for f in os.listdir(frames_dir) if f.endswith('.png')])
    
    # Extract from red channel
    all_text = []
    for frame_file in frames:
        frame_path = os.path.join(frames_dir, frame_file)
        try:
            img = Image.open(frame_path)
            img_array = np.array(img)
            if len(img_array.shape) == 3:
                channel = img_array[:, :, 0]  # Red channel
                lsb_bits = channel & 1
                flat_bits = lsb_bits.flatten()
                bit_string = ''.join([str(int(b)) for b in flat_bits])
                for i in range(0, len(bit_string) - 7, 8):
                    byte_val = int(bit_string[i:i+8], 2)
                    if 32 <= byte_val <= 126:
                        all_text.append(chr(byte_val))
        except:
            continue
    
    combined_text = ''.join(all_text)
    
    # Find all occurrences of 'flag' (case insensitive)
    import re
    flag_positions = []
    for match in re.finditer(r'[fF][lL][aA][gG]', combined_text, re.IGNORECASE):
        flag_positions.append(match.start())
    
    print(f"Found {len(flag_positions)} occurrences of 'flag'")
    
    # Examine context around each occurrence
    for i, pos in enumerate(flag_positions[:10]):  # Check first 10
        start = max(0, pos - 50)
        end = min(len(combined_text), pos + 200)
        context = combined_text[start:end]
        print(f"\nOccurrence {i+1} at position {pos}:")
        print(f"Context: {context}")
        
        # Try to find flag pattern in this context
        flag_patterns = [
            r'[fF][lL][aA][gG]\{[A-Za-z0-9_]{10,}\}',
            r'[fF][lL][aA][gG][:\{][A-Za-z0-9_]{10,}',
        ]
        for pattern in flag_patterns:
            matches = re.findall(pattern, context)
            if matches:
                print(f"  *** FLAG FOUND: {matches} ***")
    
    # Also try searching for common CTF flag formats
    print("\n=== Searching for CTF flag formats ===")
    patterns = [
        r'[a-z]{4}\{[A-Za-z0-9_]{15,}\}',  # flag{...}
        r'[A-Z]{4}\{[A-Za-z0-9_]{15,}\}',  # FLAG{...}
        r'picoCTF\{[A-Za-z0-9_]{15,}\}',
        r'[a-z]{4}CTF\{[A-Za-z0-9_]{15,}\}',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, combined_text)
        if matches:
            print(f"Pattern {pattern}: {matches}")

if __name__ == '__main__':
    extract_and_search()
