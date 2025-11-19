#!/usr/bin/env python3
import zipfile
import io

# Read the MP3 file
with open('steg_audio.mp3', 'rb') as f:
    data = f.read()

# Look for ZIP file signature (PK\x03\x04 or PK\x05\x06)
zip_start = None
for i in range(len(data) - 4):
    if data[i:i+2] == b'PK':
        # Check if it's a ZIP file header
        if data[i:i+4] == b'PK\x03\x04' or data[i:i+4] == b'PK\x05\x06':
            zip_start = i
            print(f"Found ZIP signature at offset {i}")
            break

if zip_start:
    # Extract ZIP data
    zip_data = data[zip_start:]
    
    # Try to open as ZIP
    try:
        zip_file = zipfile.ZipFile(io.BytesIO(zip_data))
        print("\nZIP file contents:")
        for name in zip_file.namelist():
            print(f"  - {name}")
        
        # Extract all files
        zip_file.extractall('.')
        print("\nExtracted files!")
        
        # Read flag.txt if it exists
        if 'flag.txt' in zip_file.namelist():
            flag_content = zip_file.read('flag.txt')
            print(f"\nFlag content:\n{flag_content.decode('utf-8', errors='ignore')}")
            
    except Exception as e:
        print(f"Error extracting ZIP: {e}")
        # Try to find the ZIP manually
        print("\nTrying alternative extraction...")
        # Look for the end of ZIP marker
        zip_end = data.rfind(b'PK\x05\x06')
        if zip_end != -1:
            print(f"Found ZIP end marker at {zip_end}")
            zip_data = data[zip_start:zip_end+22]  # ZIP end record is 22 bytes
            try:
                zip_file = zipfile.ZipFile(io.BytesIO(zip_data))
                print("\nZIP file contents:")
                for name in zip_file.namelist():
                    print(f"  - {name}")
                zip_file.extractall('.')
                if 'flag.txt' in zip_file.namelist():
                    flag_content = zip_file.read('flag.txt')
                    print(f"\nFlag content:\n{flag_content.decode('utf-8', errors='ignore')}")
            except Exception as e2:
                print(f"Still error: {e2}")
else:
    print("No ZIP signature found. Trying to extract from end of file...")
    # Sometimes ZIP is at the very end
    # Try last 100KB
    tail = data[-100000:]
    zip_start_tail = tail.find(b'PK\x03\x04')
    if zip_start_tail != -1:
        actual_start = len(data) - len(tail) + zip_start_tail
        print(f"Found ZIP at offset {actual_start}")
        zip_data = data[actual_start:]
        try:
            zip_file = zipfile.ZipFile(io.BytesIO(zip_data))
            print("\nZIP file contents:")
            for name in zip_file.namelist():
                print(f"  - {name}")
            zip_file.extractall('.')
            if 'flag.txt' in zip_file.namelist():
                flag_content = zip_file.read('flag.txt')
                print(f"\nFlag content:\n{flag_content.decode('utf-8', errors='ignore')}")
        except Exception as e:
            print(f"Error: {e}")
