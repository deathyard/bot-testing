#!/usr/bin/env python3
import cv2
import numpy as np
import re
import struct

def analyze_video_comprehensive(video_path):
    """Comprehensive analysis of video for hidden flags"""
    
    # 1. Frame-by-frame LSB analysis with different bit planes
    print("=== Frame LSB Analysis (all bit planes) ===")
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Cannot open video")
        return
    
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Total frames: {frame_count}")
    
    # Analyze first few frames in detail
    for frame_idx in range(min(10, frame_count)):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret:
            continue
        
        # Try all bit planes (0-7)
        for bit_plane in range(8):
            extracted_data = bytearray()
            
            for channel in range(3):  # B, G, R
                channel_data = frame[:, :, channel]
                # Extract specific bit plane
                bit_plane_data = (channel_data >> bit_plane) & 1
                bit_flat = bit_plane_data.flatten()
                
                # Convert bits to bytes
                for i in range(0, len(bit_flat) - 7, 8):
                    byte_val = 0
                    for j in range(8):
                        if i + j < len(bit_flat):
                            byte_val |= (int(bit_flat[i + j]) << j)
                    extracted_data.append(byte_val)
            
            # Search for flag
            try:
                data_str = extracted_data.decode('utf-8', errors='ignore')
                flag_match = re.search(r'[fF][lL][aA][gG]\{[^}]+\}', data_str, re.IGNORECASE)
                if flag_match:
                    print(f"*** FLAG FOUND in frame {frame_idx}, bit plane {bit_plane}: {flag_match.group()} ***")
                    return flag_match.group()
            except:
                pass
    
    cap.release()
    
    # 2. Check for text overlays in frames
    print("\n=== Checking for text overlays ===")
    cap = cv2.VideoCapture(video_path)
    
    # Sample frames
    for frame_idx in [0, frame_count // 4, frame_count // 2, frame_count * 3 // 4]:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret:
            continue
        
        # Simple edge detection to find text regions
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        
        # Look for rectangular regions (might be text)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if 20 < w < 500 and 10 < h < 100:  # Text-like dimensions
                roi = frame[y:y+h, x:x+w]
                # Extract LSB from ROI
                roi_lsb = roi & 1
                roi_bits = roi_lsb.flatten()
                
                # Convert to bytes
                roi_bytes = bytearray()
                for i in range(0, len(roi_bits) - 7, 8):
                    byte_val = 0
                    for j in range(8):
                        if i + j < len(roi_bits):
                            byte_val |= (int(roi_bits[i + j]) << j)
                    roi_bytes.append(byte_val)
                
                try:
                    roi_str = roi_bytes.decode('utf-8', errors='ignore')
                    if 'flag' in roi_str.lower():
                        flag_match = re.search(r'[fF][lL][aA][gG]\{[^}]+\}', roi_str, re.IGNORECASE)
                        if flag_match:
                            print(f"*** FLAG in text region frame {frame_idx}: {flag_match.group()} ***")
                            return flag_match.group()
                except:
                    pass
    
    cap.release()
    
    # 3. XOR with frame number
    print("\n=== Checking XOR with frame numbers ===")
    cap = cv2.VideoCapture(video_path)
    
    for frame_idx in range(min(20, frame_count)):
        ret, frame = cap.read()
        if not ret:
            break
        
        # XOR each pixel with frame number
        xored = frame ^ (frame_idx % 256)
        
        # Extract LSB from XORed frame
        xored_lsb = xored & 1
        xored_bits = xored_lsb.flatten()
        
        xored_bytes = bytearray()
        for i in range(0, min(len(xored_bits) - 7, 10000), 8):
            byte_val = 0
            for j in range(8):
                if i + j < len(xored_bits):
                    byte_val |= (int(xored_bits[i + j]) << j)
            xored_bytes.append(byte_val)
        
        try:
            xored_str = xored_bytes.decode('utf-8', errors='ignore')
            flag_match = re.search(r'[fF][lL][aA][gG]\{[^}]+\}', xored_str, re.IGNORECASE)
            if flag_match:
                print(f"*** FLAG with XOR frame {frame_idx}: {flag_match.group()} ***")
                return flag_match.group()
        except:
            pass
    
    cap.release()
    
    # 4. Check raw file for frame-specific patterns
    print("\n=== Checking raw file structure ===")
    with open(video_path, 'rb') as f:
        data = f.read()
    
    # Look for frame markers and check data around them
    # MP4 uses specific markers for frames
    # Try to find I-frames or keyframes
    
    # 5. Try extracting data from specific color channels only
    print("\n=== Channel-specific extraction ===")
    cap = cv2.VideoCapture(video_path)
    
    for frame_idx in range(min(5, frame_count)):
        ret, frame = cap.read()
        if not ret:
            break
        
        # Try extracting from each channel separately
        for ch_name, ch_idx in [('Blue', 0), ('Green', 1), ('Red', 2)]:
            channel = frame[:, :, ch_idx]
            
            # Extract all bit planes from this channel
            for bit in range(8):
                bit_data = (channel >> bit) & 1
                bits_flat = bit_data.flatten()
                
                # Convert to bytes
                ch_bytes = bytearray()
                for i in range(0, len(bits_flat) - 7, 8):
                    byte_val = 0
                    for j in range(8):
                        if i + j < len(bits_flat):
                            byte_val |= (int(bits_flat[i + j]) << j)
                    ch_bytes.append(byte_val)
                
                try:
                    ch_str = ch_bytes.decode('utf-8', errors='ignore')
                    flag_match = re.search(r'[fF][lL][aA][gG]\{[^}]+\}', ch_str, re.IGNORECASE)
                    if flag_match:
                        print(f"*** FLAG in {ch_name} channel, bit {bit}, frame {frame_idx}: {flag_match.group()} ***")
                        return flag_match.group()
                except:
                    pass
    
    cap.release()
    
    print("\n=== No flag found with standard methods ===")
    return None

if __name__ == '__main__':
    result = analyze_video_comprehensive('nature.mp4')
    if result:
        print(f"\n*** FINAL FLAG: {result} ***")
