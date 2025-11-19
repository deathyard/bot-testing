#!/usr/bin/env python3
import cv2
import numpy as np
from PIL import Image
import os
import re

def check_all_frames_for_text():
    """Check all frames for visible text or patterns"""
    frames_dir = 'frames'
    if not os.path.exists(frames_dir):
        print("Frames directory not found")
        return
    
    frames = sorted([f for f in os.listdir(frames_dir) if f.endswith('.png')])
    
    print(f"Checking {len(frames)} frames...")
    
    for frame_file in frames:
        frame_path = os.path.join(frames_dir, frame_file)
        img = cv2.imread(frame_path)
        
        if img is None:
            continue
        
        # Check if frame has unusual patterns
        # Check for text-like patterns
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Look for high contrast areas
        edges = cv2.Canny(gray, 50, 150)
        edge_ratio = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
        
        # If frame has many edges, it might contain text
        if edge_ratio > 0.1:
            print(f"Frame {frame_file} has high edge density (might contain text)")

def extract_lsb_from_all_frames():
    """Extract LSBs from all frames and combine"""
    frames_dir = 'frames'
    if not os.path.exists(frames_dir):
        return
    
    frames = sorted([f for f in os.listdir(frames_dir) if f.endswith('.png')])
    
    all_lsb_text = []
    
    for frame_file in frames[:50]:  # Check first 50 frames
        frame_path = os.path.join(frames_dir, frame_file)
        try:
            img = Image.open(frame_path)
            img_array = np.array(img)
            
            # Extract LSBs from red channel
            if len(img_array.shape) == 3:
                red_channel = img_array[:, :, 0]
                lsb_bits = red_channel & 1
                
                # Convert to bytes
                flat_bits = lsb_bits.flatten()
                bit_string = ''.join([str(int(b)) for b in flat_bits])
                
                # Extract ASCII characters
                for i in range(0, len(bit_string) - 7, 8):
                    byte_val = int(bit_string[i:i+8], 2)
                    if 32 <= byte_val <= 126:
                        all_lsb_text.append(chr(byte_val))
        except Exception as e:
            continue
    
    combined_text = ''.join(all_lsb_text)
    
    # Search for flag patterns
    flag_patterns = [
        r'flag\{[^}]+\}',
        r'FLAG\{[^}]+\}',
        r'picoCTF\{[^}]+\}',
        r'[A-Z]{3,}\{[A-Za-z0-9_]{10,}\}',
    ]
    
    print(f"Extracted {len(combined_text)} characters from LSBs")
    print(f"First 500 chars: {combined_text[:500]}")
    
    for pattern in flag_patterns:
        matches = re.findall(pattern, combined_text)
        if matches:
            print(f"\nFLAG FOUND: {matches}")

def check_frame_differences():
    """Check if flag is hidden in frame differences"""
    frames_dir = 'frames'
    if not os.path.exists(frames_dir):
        return
    
    frames = sorted([f for f in os.listdir(frames_dir) if f.endswith('.png')])
    
    if len(frames) < 2:
        return
    
    prev_frame = cv2.imread(os.path.join(frames_dir, frames[0]))
    
    for i in range(1, min(10, len(frames))):
        curr_frame = cv2.imread(os.path.join(frames_dir, frames[i]))
        
        # Calculate difference
        diff = cv2.absdiff(prev_frame, curr_frame)
        
        # Extract LSBs from difference
        diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        lsb_bits = diff_gray & 1
        
        # Convert to text
        flat_bits = lsb_bits.flatten()
        bit_string = ''.join([str(int(b)) for b in flat_bits])
        
        text = ''
        for j in range(0, len(bit_string) - 7, 8):
            byte_val = int(bit_string[j:j+8], 2)
            if 32 <= byte_val <= 126:
                text += chr(byte_val)
        
        # Check for flags
        flag_patterns = [
            r'flag\{[^}]+\}',
            r'FLAG\{[^}]+\}',
            r'picoCTF\{[^}]+\}',
        ]
        
        for pattern in flag_patterns:
            matches = re.findall(pattern, text)
            if matches:
                print(f"FLAG FOUND in frame difference {i}: {matches}")
        
        prev_frame = curr_frame

def main():
    print("=== Checking frames for text ===")
    check_all_frames_for_text()
    
    print("\n=== Extracting LSBs from all frames ===")
    extract_lsb_from_all_frames()
    
    print("\n=== Checking frame differences ===")
    check_frame_differences()

if __name__ == '__main__':
    main()
