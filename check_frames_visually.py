#!/usr/bin/env python3
import cv2
import numpy as np
import os

def check_frames_for_text():
    """Check frames for visible text using OCR-like techniques"""
    frames_dir = 'frames'
    frames = sorted([f for f in os.listdir(frames_dir) if f.endswith('.png')])
    
    print(f"Checking {len(frames)} frames for visible text...")
    
    for frame_file in frames[:20]:  # Check first 20 frames
        frame_path = os.path.join(frames_dir, frame_file)
        img = cv2.imread(frame_path)
        
        if img is None:
            continue
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply threshold to find text-like regions
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        
        # Look for high contrast regions (potential text)
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
        
        # Check if frame has unusual patterns that might be text
        # Look at specific regions where text might appear (corners, center)
        h, w = gray.shape
        
        # Check corners and center
        regions = [
            gray[0:h//10, 0:w//10],  # Top-left
            gray[0:h//10, -w//10:],  # Top-right
            gray[-h//10:, 0:w//10],  # Bottom-left
            gray[-h//10:, -w//10:],  # Bottom-right
            gray[h//2-h//20:h//2+h//20, w//2-w//20:w//2+w//20],  # Center
        ]
        
        for i, region in enumerate(regions):
            # Check if region has high variance (text has high variance)
            if np.var(region) > 1000:  # Threshold for text-like variance
                print(f"Frame {frame_file}, region {i} has high variance (might contain text)")
                # Extract LSBs from this region
                lsb_bits = region & 1
                # Try to extract text from LSBs
                flat = lsb_bits.flatten()
                bit_string = ''.join([str(int(b)) for b in flat])
                text = ''
                for j in range(0, len(bit_string) - 7, 8):
                    byte_val = int(bit_string[j:j+8], 2)
                    if 32 <= byte_val <= 126:
                        text += chr(byte_val)
                if len(text) > 10:
                    # Check for flag patterns
                    import re
                    flag_matches = re.findall(r'[fF][lL][aA][gG]\{[^}]+\}', text)
                    if flag_matches:
                        print(f"  FLAG FOUND: {flag_matches}")
                    elif 'flag' in text.lower():
                        print(f"  Potential flag text: {text[:100]}")

if __name__ == '__main__':
    check_frames_for_text()
