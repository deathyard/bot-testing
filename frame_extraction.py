#!/usr/bin/env python3
import cv2
import numpy as np
import re

def extract_and_analyze_frames(video_path):
    """Extract frames and save for analysis"""
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Cannot open video")
        return
    
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Total frames: {frame_count}")
    
    # Extract first, middle, and last frames
    frames_to_check = [0, frame_count // 2, frame_count - 1]
    
    for frame_idx in frames_to_check:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret:
            continue
        
        print(f"\n=== Analyzing frame {frame_idx} ===")
        
        # Save frame
        cv2.imwrite(f'frame_{frame_idx}.png', frame)
        print(f"Saved frame_{frame_idx}.png")
        
        # Try different steganography techniques on this frame
        for method in ['lsb', 'msb', 'bit_plane_1', 'bit_plane_2']:
            extracted = extract_data_from_frame(frame, method)
            if extracted:
                flag_match = re.search(r'[fF][lL][aA][gG]\{[^}]+\}', extracted, re.IGNORECASE)
                if flag_match:
                    print(f"*** FLAG FOUND with {method}: {flag_match.group()} ***")
                    cap.release()
                    return flag_match.group()
    
    cap.release()
    return None

def extract_data_from_frame(frame, method='lsb'):
    """Extract data from frame using different methods"""
    extracted_bytes = bytearray()
    
    if method == 'lsb':
        # LSB from all channels
        for ch in range(3):
            channel = frame[:, :, ch]
            lsb = channel & 1
            bits = lsb.flatten()
            for i in range(0, min(len(bits) - 7, 20000), 8):
                byte_val = 0
                for j in range(8):
                    if i + j < len(bits):
                        byte_val |= (int(bits[i + j]) << j)
                extracted_bytes.append(byte_val)
    
    elif method == 'msb':
        # MSB from all channels
        for ch in range(3):
            channel = frame[:, :, ch]
            msb = (channel >> 7) & 1
            bits = msb.flatten()
            for i in range(0, min(len(bits) - 7, 20000), 8):
                byte_val = 0
                for j in range(8):
                    if i + j < len(bits):
                        byte_val |= (int(bits[i + j]) << j)
                extracted_bytes.append(byte_val)
    
    elif method == 'bit_plane_1':
        # Second bit plane
        for ch in range(3):
            channel = frame[:, :, ch]
            bp = (channel >> 1) & 1
            bits = bp.flatten()
            for i in range(0, min(len(bits) - 7, 20000), 8):
                byte_val = 0
                for j in range(8):
                    if i + j < len(bits):
                        byte_val |= (int(bits[i + j]) << j)
                extracted_bytes.append(byte_val)
    
    elif method == 'bit_plane_2':
        # Third bit plane
        for ch in range(3):
            channel = frame[:, :, ch]
            bp = (channel >> 2) & 1
            bits = bp.flatten()
            for i in range(0, min(len(bits) - 7, 20000), 8):
                byte_val = 0
                for j in range(8):
                    if i + j < len(bits):
                        byte_val |= (int(bits[i + j]) << j)
                extracted_bytes.append(byte_val)
    
    try:
        return extracted_bytes.decode('utf-8', errors='ignore')
    except:
        return None

if __name__ == '__main__':
    result = extract_and_analyze_frames('nature.mp4')
    if result:
        print(f"\n*** FINAL FLAG: {result} ***")
