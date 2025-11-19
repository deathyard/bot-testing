#!/usr/bin/env python3
import zipfile
import io

# Read the MP3 file
with open('steg_audio.mp3', 'rb') as f:
    data = f.read()

# From hexdump, ZIP starts at offset 0x570a0 (356640 decimal)
# But let's find it dynamically
zip_start = None
for i in range(len(data) - 100):
    if data[i:i+4] == b'PK\x03\x04':
        # Check if next bytes look like a ZIP entry
        # ZIP local file header is at least 30 bytes
        if i + 30 < len(data):
            zip_start = i
            break

if zip_start:
    print(f"Found ZIP at offset {zip_start}")
    zip_data = data[zip_start:]
    
    try:
        zip_file = zipfile.ZipFile(io.BytesIO(zip_data))
        print(f"ZIP file contents: {zip_file.namelist()}")
        
        # Extract flag.txt
        if 'flag.txt' in zip_file.namelist():
            flag_content = zip_file.read('flag.txt')
            print(f"\n{'='*60}")
            print(f"FLAG FOUND:")
            print(f"{'='*60}")
            print(flag_content.decode('utf-8', errors='ignore'))
            print(f"{'='*60}")
            
            # Also extract to file
            zip_file.extractall('.')
            print("\nExtracted flag.txt to current directory")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
