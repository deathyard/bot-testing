#!/usr/bin/env python3
"""
CTF Steganography Analysis Tool
Analyzes images for hidden flags using multiple techniques
"""

import sys
import os
from PIL import Image
import binascii
import base64
import re

def extract_lsb(image_path):
    """Extract Least Significant Bit (LSB) steganography"""
    try:
        img = Image.open(image_path)
        pixels = img.load()
        width, height = img.size
        
        binary_data = ""
        for y in range(height):
            for x in range(width):
                pixel = pixels[x, y]
                if isinstance(pixel, tuple):
                    # Extract LSB from each color channel
                    for channel in pixel[:3]:  # RGB only
                        binary_data += str(channel & 1)
                else:
                    binary_data += str(pixel & 1)
        
        # Convert binary to text
        text = ""
        for i in range(0, len(binary_data), 8):
            byte = binary_data[i:i+8]
            if len(byte) == 8:
                try:
                    char = chr(int(byte, 2))
                    if char.isprintable() or char in '\n\r\t':
                        text += char
                except:
                    pass
        
        return text
    except Exception as e:
        return f"Error in LSB extraction: {e}"

def extract_metadata(image_path):
    """Extract metadata from image"""
    try:
        img = Image.open(image_path)
        metadata = {}
        
        # EXIF data
        if hasattr(img, '_getexif') and img._getexif():
            metadata['exif'] = dict(img._getexif())
        
        # Other metadata
        if hasattr(img, 'info'):
            metadata['info'] = img.info
        
        return metadata
    except Exception as e:
        return f"Error extracting metadata: {e}"

def extract_strings(image_path):
    """Extract readable strings from image file"""
    try:
        with open(image_path, 'rb') as f:
            data = f.read()
        
        # Find printable strings
        strings = []
        current_string = ""
        
        for byte in data:
            if 32 <= byte <= 126:  # Printable ASCII
                current_string += chr(byte)
            else:
                if len(current_string) >= 4:
                    strings.append(current_string)
                current_string = ""
        
        if len(current_string) >= 4:
            strings.append(current_string)
        
        return strings
    except Exception as e:
        return f"Error extracting strings: {e}"

def find_base64_in_strings(strings):
    """Find base64 encoded data in strings"""
    base64_pattern = re.compile(r'[A-Za-z0-9+/]{20,}={0,2}')
    results = []
    
    for s in strings:
        matches = base64_pattern.findall(s)
        for match in matches:
            try:
                decoded = base64.b64decode(match + '==')
                if all(32 <= b <= 126 or b in [9, 10, 13] for b in decoded):
                    results.append((match, decoded.decode('utf-8', errors='ignore')))
            except:
                pass
    
    return results

def find_flags(text):
    """Find CTF flag patterns"""
    flag_patterns = [
        r'FLAG\{[^}]+\}',
        r'flag\{[^}]+\}',
        r'CTF\{[^}]+\}',
        r'ctf\{[^}]+\}',
        r'nutanix\{[^}]+\}',
        r'NUTANIX\{[^}]+\}',
        r'[A-Z0-9_]{10,}',  # Uppercase flags
    ]
    
    flags = []
    for pattern in flag_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        flags.extend(matches)
    
    return list(set(flags))

def analyze_image(image_path):
    """Main analysis function"""
    print(f"🔍 Analyzing image: {image_path}\n")
    print("=" * 60)
    
    if not os.path.exists(image_path):
        print(f"❌ Error: File not found: {image_path}")
        return
    
    # File info
    file_size = os.path.getsize(image_path)
    print(f"📁 File size: {file_size} bytes")
    
    try:
        img = Image.open(image_path)
        print(f"📐 Image dimensions: {img.size}")
        print(f"🎨 Image mode: {img.mode}")
        print(f"📋 Image format: {img.format}")
    except Exception as e:
        print(f"⚠️  Error reading image: {e}")
    
    print("\n" + "=" * 60)
    print("1️⃣  EXTRACTING METADATA...")
    print("=" * 60)
    metadata = extract_metadata(image_path)
    if isinstance(metadata, dict):
        for key, value in metadata.items():
            print(f"\n{key.upper()}:")
            if isinstance(value, dict):
                for k, v in value.items():
                    print(f"  {k}: {v}")
            else:
                print(f"  {value}")
    else:
        print(metadata)
    
    print("\n" + "=" * 60)
    print("2️⃣  EXTRACTING STRINGS...")
    print("=" * 60)
    strings = extract_strings(image_path)
    if isinstance(strings, list):
        print(f"Found {len(strings)} strings")
        # Look for flags in strings
        all_strings_text = " ".join(strings)
        flags_in_strings = find_flags(all_strings_text)
        if flags_in_strings:
            print("\n🚩 FLAGS FOUND IN STRINGS:")
            for flag in flags_in_strings:
                print(f"  ✓ {flag}")
        
        # Check for base64
        base64_data = find_base64_in_strings(strings)
        if base64_data:
            print("\n🔐 BASE64 DATA FOUND:")
            for b64, decoded in base64_data[:5]:  # Show first 5
                print(f"  Base64: {b64[:50]}...")
                print(f"  Decoded: {decoded[:100]}...")
                flags = find_flags(decoded)
                if flags:
                    print(f"  🚩 Flags in decoded: {flags}")
    else:
        print(strings)
    
    print("\n" + "=" * 60)
    print("3️⃣  EXTRACTING LSB (Least Significant Bit)...")
    print("=" * 60)
    lsb_text = extract_lsb(image_path)
    if lsb_text:
        # Look for flags in LSB data
        flags_in_lsb = find_flags(lsb_text)
        if flags_in_lsb:
            print("\n🚩 FLAGS FOUND IN LSB:")
            for flag in flags_in_lsb:
                print(f"  ✓ {flag}")
        
        # Show first 500 chars of extracted text
        print("\n📝 First 500 characters of extracted LSB data:")
        print(lsb_text[:500])
        if len(lsb_text) > 500:
            print(f"\n... (truncated, total length: {len(lsb_text)} chars)")
    else:
        print("No readable data found in LSB")
    
    print("\n" + "=" * 60)
    print("4️⃣  FINAL FLAG SUMMARY")
    print("=" * 60)
    
    # Collect all flags found
    all_flags = []
    if isinstance(strings, list):
        all_flags.extend(find_flags(" ".join(strings)))
    if lsb_text:
        all_flags.extend(find_flags(lsb_text))
    
    unique_flags = list(set(all_flags))
    if unique_flags:
        print("\n🎯 ALL FLAGS FOUND:")
        for flag in unique_flags:
            print(f"  🚩 {flag}")
    else:
        print("\n⚠️  No flags found with standard patterns")
        print("💡 Try manual inspection or other steganography tools")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 analyze_stegno.py <image_path>")
        print("\nExample: python3 analyze_stegno.py stegno_1.jpg")
        sys.exit(1)
    
    image_path = sys.argv[1]
    analyze_image(image_path)
