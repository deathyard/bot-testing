#!/usr/bin/env python3
import cv2
import numpy as np
import re

def quick_scan(video_path):
    """Quick targeted scan for flags"""
    
    print("=== Quick Frame Scan ===")
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None
    
    # Just check first frame in detail
    ret, frame = cap.read()
    if ret:
        print(f"Frame shape: {frame.shape}")
        
        # Try LSB from first frame, all channels
        for ch in range(3):
            channel = frame[:, :, ch]
            lsb = channel & 1
            bits = lsb.flatten()
            
            # Convert to bytes
            bytes_data = bytearray()
            for i in range(0, min(len(bits) - 7, 50000), 8):
                byte_val = 0
                for j in range(8):
                    if i + j < len(bits):
                        byte_val |= (int(bits[i + j]) << j)
                bytes_data.append(byte_val)
            
            # Search for flag
            try:
                text = bytes_data.decode('utf-8', errors='ignore')
                flag_match = re.search(r'[fF][lL][aA][gG]\{[^}]+\}', text, re.IGNORECASE)
                if flag_match:
                    print(f"*** FLAG in channel {ch}: {flag_match.group()} ***")
                    cap.release()
                    return flag_match.group()
            except:
                pass
    
    cap.release()
    
    # Check raw file for appended data
    print("\n=== Checking file for appended data ===")
    with open(video_path, 'rb') as f:
        data = f.read()
    
    # Check last 10KB
    tail = data[-10000:]
    tail_str = tail.decode('utf-8', errors='ignore')
    flag_match = re.search(r'[fF][lL][aA][gG]\{[^}]+\}', tail_str, re.IGNORECASE)
    if flag_match:
        print(f"*** FLAG at end of file: {flag_match.group()} ***")
        return flag_match.group()
    
    # Check for base64 in tail
    import base64
    b64_pattern = re.compile(rb'[A-Za-z0-9+/]{20,}={0,2}')
    matches = b64_pattern.finditer(tail)
    for match in matches:
        try:
            b64_str = match.group().decode('ascii')
            decoded = base64.b64decode(b64_str)
            decoded_str = decoded.decode('utf-8', errors='ignore')
            flag_match = re.search(r'[fF][lL][aA][gG]\{[^}]+\}', decoded_str, re.IGNORECASE)
            if flag_match:
                print(f"*** FLAG in base64: {flag_match.group()} ***")
                return flag_match.group()
        except:
            pass
    
    return None

if __name__ == '__main__':
    result = quick_scan('nature.mp4')
    if result:
        print(f"\n*** FLAG FOUND: {result} ***")
    else:
        print("\nNo flag found in quick scan")
