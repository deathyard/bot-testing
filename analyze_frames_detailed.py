#!/usr/bin/env python3
import cv2
import numpy as np
import re

def analyze_extracted_frames():
    """Analyze the extracted frame images"""
    
    frame_files = ['frame_0.png', 'frame_178.png', 'frame_356.png']
    
    for frame_file in frame_files:
        try:
            frame = cv2.imread(frame_file)
            if frame is None:
                continue
            
            print(f"\n=== Analyzing {frame_file} ===")
            print(f"Shape: {frame.shape}")
            
            # Try all bit planes for all channels
            for bit_plane in range(8):
                for channel_idx in range(3):
                    channel = frame[:, :, channel_idx]
                    bit_data = (channel >> bit_plane) & 1
                    bits_flat = bit_data.flatten()
                    
                    # Convert to bytes
                    bytes_data = bytearray()
                    for i in range(0, min(len(bits_flat) - 7, 50000), 8):
                        byte_val = 0
                        for j in range(8):
                            if i + j < len(bits_flat):
                                byte_val |= (int(bits_flat[i + j]) << j)
                        bytes_data.append(byte_val)
                    
                    # Search for flag
                    try:
                        text = bytes_data.decode('utf-8', errors='ignore')
                        flag_match = re.search(r'[fF][lL][aA][gG]\{[^}]+\}', text, re.IGNORECASE)
                        if flag_match:
                            print(f"*** FLAG FOUND in {frame_file}, bit plane {bit_plane}, channel {channel_idx}: {flag_match.group()} ***")
                            return flag_match.group()
                    except:
                        pass
            
            # Try XOR patterns
            for xor_key in [0x00, 0xFF, 0xAA, 0x55]:
                xored = frame ^ xor_key
                lsb = xored & 1
                bits_flat = lsb.flatten()
                
                bytes_data = bytearray()
                for i in range(0, min(len(bits_flat) - 7, 20000), 8):
                    byte_val = 0
                    for j in range(8):
                        if i + j < len(bits_flat):
                            byte_val |= (int(bits_flat[i + j]) << j)
                    bytes_data.append(byte_val)
                
                try:
                    text = bytes_data.decode('utf-8', errors='ignore')
                    flag_match = re.search(r'[fF][lL][aA][gG]\{[^}]+\}', text, re.IGNORECASE)
                    if flag_match:
                        print(f"*** FLAG FOUND with XOR {hex(xor_key)}: {flag_match.group()} ***")
                        return flag_match.group()
                except:
                    pass
        
        except Exception as e:
            print(f"Error analyzing {frame_file}: {e}")
            continue
    
    return None

if __name__ == '__main__':
    result = analyze_extracted_frames()
    if result:
        print(f"\n*** FINAL FLAG: {result} ***")
    else:
        print("\nNo flag found in frame analysis")
