#!/usr/bin/env python3
import cv2
import numpy as np
from PIL import Image
import os

def extract_frames(video_path, output_dir='frames'):
    """Extract frames from video"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    extracted_frames = []
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_path = os.path.join(output_dir, f'frame_{frame_count:04d}.png')
        cv2.imwrite(frame_path, frame)
        extracted_frames.append(frame_path)
        frame_count += 1
        
        # Limit to first 100 frames for analysis
        if frame_count >= 100:
            break
    
    cap.release()
    print(f"Extracted {frame_count} frames")
    return extracted_frames

def analyze_frame_lsb(frame_path):
    """Analyze LSB steganography in a frame"""
    img = Image.open(frame_path)
    img_array = np.array(img)
    
    # Extract LSBs from each color channel
    lsb_data = []
    for channel in range(min(3, img_array.shape[2] if len(img_array.shape) > 2 else 1)):
        if len(img_array.shape) == 3:
            channel_data = img_array[:, :, channel]
        else:
            channel_data = img_array
        
        # Extract LSBs
        lsb_bits = channel_data & 1
        lsb_bytes = lsb_bits.flatten()
        
        # Convert bits to bytes (8 bits = 1 byte)
        bit_string = ''.join([str(int(b)) for b in lsb_bytes])
        for i in range(0, len(bit_string) - 7, 8):
            byte_val = int(bit_string[i:i+8], 2)
            if 32 <= byte_val <= 126:  # Printable ASCII
                lsb_data.append(chr(byte_val))
    
    return ''.join(lsb_data)

def check_frame_for_text(frame_path):
    """Check if frame contains readable text"""
    img = cv2.imread(frame_path)
    if img is None:
        return None
    
    # Try OCR-like extraction (simple approach)
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Look for high contrast areas that might be text
    # This is a simple heuristic
    
    return gray

def main():
    video_path = 'nature.mp4'
    
    print("=== Extracting frames from video ===")
    try:
        frames = extract_frames(video_path)
        
        print("\n=== Analyzing frames for LSB steganography ===")
        for i, frame_path in enumerate(frames[:10]):  # Check first 10 frames
            lsb_text = analyze_frame_lsb(frame_path)
            if len(lsb_text) > 20:
                # Look for flag patterns
                import re
                flag_patterns = [
                    r'flag\{[^}]+\}',
                    r'FLAG\{[^}]+\}',
                    r'picoCTF\{[^}]+\}',
                ]
                for pattern in flag_patterns:
                    matches = re.findall(pattern, lsb_text)
                    if matches:
                        print(f"FLAG FOUND in frame {i}: {matches}")
                        print(f"LSB text: {lsb_text[:200]}")
    except Exception as e:
        print(f"Error processing video: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
