#!/usr/bin/env python3
import cv2
import re

def find_flag_in_video(video_path):
    """Extract all frames and search for flag"""
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None
    
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Analyzing {frame_count} frames...")
    
    # Check every 10th frame for efficiency
    for frame_idx in range(0, frame_count, 10):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert frame to bytes and search
        frame_bytes = frame.tobytes()
        
        # Search for flag pattern
        flag_match = re.search(rb'[fF][lL][aA][gG]\{[^}]+\}', frame_bytes, re.IGNORECASE)
        if flag_match:
            try:
                flag = flag_match.group().decode('utf-8', errors='ignore')
                print(f"*** FLAG FOUND in frame {frame_idx}: {flag} ***")
                cap.release()
                return flag
            except:
                pass
        
        # Also try LSB extraction
        lsb_data = bytearray()
        for ch in range(3):
            channel = frame[:, :, ch]
            lsb = channel & 1
            bits = lsb.flatten()
            for i in range(0, min(len(bits) - 7, 10000), 8):
                byte_val = 0
                for j in range(8):
                    if i + j < len(bits):
                        byte_val |= (int(bits[i + j]) << j)
                lsb_data.append(byte_val)
        
        try:
            lsb_str = lsb_data.decode('utf-8', errors='ignore')
            flag_match = re.search(r'[fF][lL][aA][gG]\{[^}]+\}', lsb_str, re.IGNORECASE)
            if flag_match:
                print(f"*** FLAG FOUND in frame {frame_idx} LSB: {flag_match.group()} ***")
                cap.release()
                return flag_match.group()
        except:
            pass
    
    cap.release()
    return None

if __name__ == '__main__':
    result = find_flag_in_video('nature.mp4')
    if result:
        print(f"\n*** FLAG: {result} ***")
    else:
        print("\nFlag not found")
