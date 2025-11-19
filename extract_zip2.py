#!/usr/bin/env python3
import zipfile
import io

# Read the MP3 file
with open('steg_audio.mp3', 'rb') as f:
    data = f.read()

print(f"Total file size: {len(data)} bytes")

# Find all PK markers
pk_positions = []
for i in range(len(data) - 1):
    if data[i:i+2] == b'PK':
        pk_positions.append(i)

print(f"\nFound {len(pk_positions)} PK markers")
print(f"Positions: {pk_positions[-10:]}")  # Show last 10

# Try to find ZIP file starting from different positions
for start_pos in pk_positions[-5:]:  # Check last 5 PK positions
    print(f"\nTrying ZIP extraction from offset {start_pos}...")
    zip_data = data[start_pos:]
    
    # Try different lengths
    for length_multiplier in [1, 1.1, 1.2, 1.5, 2]:
        test_length = int(len(zip_data) * length_multiplier)
        if test_length > len(data):
            test_length = len(data) - start_pos
        
        try:
            test_data = data[start_pos:start_pos+test_length]
            zip_file = zipfile.ZipFile(io.BytesIO(test_data))
            print(f"  SUCCESS! ZIP found at offset {start_pos} with length {test_length}")
            print(f"  Files in ZIP:")
            for name in zip_file.namelist():
                print(f"    - {name}")
            
            # Extract
            zip_file.extractall('.')
            print(f"  Files extracted!")
            
            # Read flag
            if 'flag.txt' in zip_file.namelist():
                flag_content = zip_file.read('flag.txt')
                print(f"\n  FLAG: {flag_content.decode('utf-8', errors='ignore')}")
            break
        except:
            continue

# Also try binwalk approach - extract everything after MP3
print("\n" + "="*60)
print("Trying binwalk-style extraction...")
print("="*60)

# MP3 files typically end with certain patterns
# Try extracting from various offsets near the end
for offset in range(max(0, len(data)-50000), len(data), 100):
    test_data = data[offset:]
    if len(test_data) < 100:
        break
    
    # Check if it starts with ZIP
    if test_data[:2] == b'PK':
        try:
            zip_file = zipfile.ZipFile(io.BytesIO(test_data))
            print(f"Found valid ZIP at offset {offset}!")
            print(f"Files: {zip_file.namelist()}")
            zip_file.extractall('.')
            if 'flag.txt' in zip_file.namelist():
                flag_content = zip_file.read('flag.txt')
                print(f"\nFLAG: {flag_content.decode('utf-8', errors='ignore')}")
            break
        except:
            continue
