#!/usr/bin/env python3
"""
CTF Image Steganography Analyzer
Finds hidden flags in images using multiple techniques
"""

import sys
import os
from PIL import Image
import subprocess

def banner():
    print("=" * 60)
    print("CTF Image Steganography Analyzer")
    print("=" * 60)

def check_strings(image_path):
    """Extract printable strings from image"""
    print("\n[*] Extracting strings from image...")
    try:
        result = subprocess.run(['strings', image_path], capture_output=True, text=True)
        strings_output = result.stdout
        
        # Look for common flag patterns
        flag_patterns = ['flag', 'FLAG', 'ctf', 'CTF', '{', '}']
        potential_flags = []
        
        for line in strings_output.split('\n'):
            for pattern in flag_patterns:
                if pattern in line:
                    potential_flags.append(line)
        
        if potential_flags:
            print("[+] Potential flags found in strings:")
            for flag in potential_flags:
                print(f"    {flag}")
        else:
            print("[-] No obvious flags in strings")
        
        return strings_output
    except Exception as e:
        print(f"[-] Error extracting strings: {e}")
        return ""

def check_lsb_stegano(image_path):
    """Check for LSB steganography using stegano library"""
    print("\n[*] Checking for LSB steganography...")
    try:
        from stegano import lsb
        hidden_data = lsb.reveal(image_path)
        if hidden_data:
            print("[+] LSB Hidden data found:")
            print(f"    {hidden_data}")
            return hidden_data
        else:
            print("[-] No LSB data found")
    except Exception as e:
        print(f"[-] LSB check failed: {e}")
    return None

def check_metadata(image_path):
    """Check image metadata/EXIF data"""
    print("\n[*] Checking image metadata...")
    try:
        from PIL import Image
        from PIL.ExifTags import TAGS
        
        img = Image.open(image_path)
        exif_data = img._getexif()
        
        if exif_data:
            print("[+] EXIF data found:")
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                print(f"    {tag}: {value}")
        else:
            print("[-] No EXIF data found")
            
        # Check other metadata
        print("\n[*] Image info:")
        print(f"    Format: {img.format}")
        print(f"    Size: {img.size}")
        print(f"    Mode: {img.mode}")
        
        if img.info:
            print("[+] Additional metadata:")
            for key, value in img.info.items():
                print(f"    {key}: {value}")
                
    except Exception as e:
        print(f"[-] Metadata check failed: {e}")

def check_pixel_data(image_path):
    """Analyze pixel data for anomalies"""
    print("\n[*] Analyzing pixel data...")
    try:
        img = Image.open(image_path)
        pixels = img.load()
        width, height = img.size
        
        # Check for unusual patterns in LSBs
        lsb_bits = []
        for y in range(min(height, 100)):  # Check first 100 rows
            for x in range(min(width, 100)):
                if img.mode == 'RGB':
                    r, g, b = pixels[x, y]
                    lsb_bits.append(r & 1)
                    lsb_bits.append(g & 1)
                    lsb_bits.append(b & 1)
                elif img.mode == 'RGBA':
                    r, g, b, a = pixels[x, y]
                    lsb_bits.append(r & 1)
                    lsb_bits.append(g & 1)
                    lsb_bits.append(b & 1)
        
        # Try to decode LSBs as ASCII
        bytes_data = []
        for i in range(0, len(lsb_bits) - 7, 8):
            byte = 0
            for j in range(8):
                byte = (byte << 1) | lsb_bits[i + j]
            if 32 <= byte <= 126:  # Printable ASCII
                bytes_data.append(chr(byte))
            else:
                bytes_data.append('.')
        
        text = ''.join(bytes_data[:200])  # First 200 chars
        if any(c.isalpha() for c in text):
            print(f"[+] Potential hidden text in LSBs: {text}")
        else:
            print("[-] No readable text in LSBs")
            
    except Exception as e:
        print(f"[-] Pixel analysis failed: {e}")

def check_file_structure(image_path):
    """Check for appended data or file structure anomalies"""
    print("\n[*] Checking file structure...")
    try:
        with open(image_path, 'rb') as f:
            data = f.read()
            
        # Check for multiple file signatures
        signatures = {
            b'\xFF\xD8\xFF': 'JPEG',
            b'\x89PNG': 'PNG',
            b'GIF87a': 'GIF87a',
            b'GIF89a': 'GIF89a',
            b'PK\x03\x04': 'ZIP',
            b'Rar!': 'RAR'
        }
        
        found_sigs = []
        for sig, name in signatures.items():
            count = data.count(sig)
            if count > 0:
                found_sigs.append(f"{name} ({count})")
        
        if found_sigs:
            print(f"[+] File signatures found: {', '.join(found_sigs)}")
        
        # Look for flag patterns in raw data
        flag_patterns = [b'flag{', b'FLAG{', b'ctf{', b'CTF{']
        for pattern in flag_patterns:
            if pattern in data:
                idx = data.find(pattern)
                # Extract surrounding context
                snippet = data[idx:idx+100]
                try:
                    decoded = snippet.decode('utf-8', errors='ignore')
                    print(f"[+] Potential flag found: {decoded}")
                except:
                    print(f"[+] Flag pattern found at offset {idx}")
        
    except Exception as e:
        print(f"[-] File structure check failed: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 ctf_image_analyzer.py <image_file>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found!")
        sys.exit(1)
    
    banner()
    print(f"[*] Analyzing: {image_path}\n")
    
    # Run all checks
    check_file_structure(image_path)
    check_strings(image_path)
    check_metadata(image_path)
    check_lsb_stegano(image_path)
    check_pixel_data(image_path)
    
    print("\n" + "=" * 60)
    print("Analysis complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
