#!/usr/bin/env python3
import cv2
import numpy as np
from PIL import Image
import os
import re

def extract_lsb_systematic():
    """Extract LSBs systematically from all channels and frames"""
    frames_dir = 'frames'
    frames = sorted([f for f in os.listdir(frames_dir) if f.endswith('.png')])
    
    print(f"Processing {len(frames)} frames...")
    
    # Try different extraction methods
    methods = [
        ('red_channel', 0),
        ('green_channel', 1),
        ('blue_channel', 2),
        ('all_channels_combined', None),
    ]
    
    for method_name, channel_idx in methods:
        print(f"\n=== Method: {method_name} ===")
        all_text = []
        
        for frame_file in frames:
            frame_path = os.path.join(frames_dir, frame_file)
            try:
                img = Image.open(frame_path)
                img_array = np.array(img)
                
                if len(img_array.shape) == 3:
                    if channel_idx is not None:
                        channel = img_array[:, :, channel_idx]
                    else:
                        # Combine all channels
                        channel = img_array[:, :, 0]  # Start with red
                    
                    # Extract LSBs
                    lsb_bits = channel & 1
                    flat_bits = lsb_bits.flatten()
                    
                    # Convert to bytes
                    bit_string = ''.join([str(int(b)) for b in flat_bits])
                    
                    # Extract ASCII characters
                    for i in range(0, len(bit_string) - 7, 8):
                        byte_val = int(bit_string[i:i+8], 2)
                        if 32 <= byte_val <= 126:
                            all_text.append(chr(byte_val))
            except Exception as e:
                continue
        
        combined_text = ''.join(all_text)
        
        # Search for flag patterns
        flag_patterns = [
            r'flag\{[A-Za-z0-9_]{10,}\}',
            r'FLAG\{[A-Za-z0-9_]{10,}\}',
            r'picoCTF\{[A-Za-z0-9_]{10,}\}',
            r'[a-z]{4}\{[A-Za-z0-9_]{10,}\}',
            r'[A-Z]{4}\{[A-Za-z0-9_]{10,}\}',
        ]
        
        print(f"Extracted {len(combined_text)} characters")
        
        found_any = False
        for pattern in flag_patterns:
            matches = re.findall(pattern, combined_text)
            if matches:
                print(f"*** FLAG FOUND with pattern {pattern}: {matches} ***")
                found_any = True
        
        if not found_any and len(combined_text) > 100:
            # Show first 500 chars to see if there's a pattern
            print(f"First 500 chars: {combined_text[:500]}")
            # Also search for any occurrence of 'flag' (case insensitive)
            flag_idx = combined_text.lower().find('flag')
            if flag_idx != -1:
                print(f"Found 'flag' at position {flag_idx}: {combined_text[max(0,flag_idx-20):flag_idx+100]}")

if __name__ == '__main__':
    extract_lsb_systematic()
