#!/usr/bin/env python3
import cv2
import numpy as np
import re

def extract_frames_and_analyze(video_path):
    """Extract frames and look for hidden flags"""
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video")
        return
    
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    print(f"Video info: {frame_count} frames, {fps} fps")
    print(f"Extracting and analyzing frames...\n")
    
    frame_num = 0
    flags_found = []
    
    # Extract frames at different intervals
    intervals = [0, frame_count // 4, frame_count // 2, frame_count * 3 // 4, frame_count - 1]
    intervals = sorted(set([int(i) for i in intervals if i < frame_count]))
    
    for target_frame in intervals:
        cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
        ret, frame = cap.read()
        
        if not ret:
            continue
        
        print(f"Analyzing frame {target_frame}...")
        
        # 1. Check for text in frame (OCR-like, simple pattern matching)
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 2. LSB steganography on frame
        # Extract LSB from each color channel
        for channel_idx in range(3):  # B, G, R channels
            channel = frame[:, :, channel_idx]
            lsb = channel & 1
            
            # Try to reconstruct data from LSB
            lsb_flat = lsb.flatten()
            # Group into bytes
            lsb_bytes = bytearray()
            for i in range(0, len(lsb_flat) - 7, 8):
                byte_val = 0
                for j in range(8):
                    if i + j < len(lsb_flat):
                        byte_val |= (int(lsb_flat[i + j]) << j)
                lsb_bytes.append(byte_val)
            
            # Search for flag in LSB data
            try:
                lsb_str = lsb_bytes.decode('utf-8', errors='ignore')
                flag_match = re.search(r'[fF][lL][aA][gG]\{[^}]+\}', lsb_str, re.IGNORECASE)
                if flag_match:
                    flag = flag_match.group()
                    if flag not in flags_found:
                        flags_found.append(flag)
                        print(f"  *** FLAG FOUND in channel {channel_idx} LSB: {flag} ***")
            except:
                pass
        
        # 3. Check if frame has unusual patterns (might indicate hidden data)
        # Check variance - low variance might indicate hidden data
        frame_variance = np.var(gray)
        
        # 4. Look for QR codes or barcodes (sometimes flags are encoded)
        # This is a simple check - full QR detection would need zbar or similar
        
        # 5. Save frame for manual inspection if interesting
        if frame_variance < 100:  # Low variance might indicate steganography
            print(f"  Frame {target_frame} has low variance ({frame_variance:.2f}) - might contain hidden data")
    
    cap.release()
    
    # Also try extracting every Nth frame for thorough analysis
    print("\n=== Extracting sample frames for detailed analysis ===")
    cap = cv2.VideoCapture(video_path)
    sample_rate = max(1, frame_count // 100)  # Sample 100 frames
    
    all_lsb_data = bytearray()
    frames_analyzed = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame_num % sample_rate == 0:
            # Extract LSB from all channels
            for channel_idx in range(3):
                channel = frame[:, :, channel_idx]
                lsb = channel & 1
                lsb_flat = lsb.flatten()
                
                # Add to cumulative LSB data
                for bit in lsb_flat[:1000]:  # Limit per frame
                    all_lsb_data.append(bit)
            
            frames_analyzed += 1
            if frames_analyzed >= 50:  # Limit to 50 frames
                break
        
        frame_num += 1
    
    cap.release()
    
    # Search cumulative LSB data
    if len(all_lsb_data) > 0:
        # Group bits into bytes
        lsb_bytes = bytearray()
        for i in range(0, len(all_lsb_data) - 7, 8):
            byte_val = 0
            for j in range(8):
                if i + j < len(all_lsb_data):
                    byte_val |= (int(all_lsb_data[i + j]) << j)
            lsb_bytes.append(byte_val)
        
        try:
            lsb_str = lsb_bytes.decode('utf-8', errors='ignore')
            flag_match = re.search(r'[fF][lL][aA][gG]\{[^}]+\}', lsb_str, re.IGNORECASE)
            if flag_match:
                flag = flag_match.group()
                if flag not in flags_found:
                    flags_found.append(flag)
                    print(f"\n*** FLAG FOUND in cumulative LSB: {flag} ***")
        except:
            pass
    
    # Print summary
    print(f"\n=== Summary ===")
    if flags_found:
        print("Flags found:")
        for flag in flags_found:
            print(f"  {flag}")
    else:
        print("No flags found in frame analysis")
        print("Trying alternative methods...")

if __name__ == '__main__':
    extract_frames_and_analyze('nature.mp4')
