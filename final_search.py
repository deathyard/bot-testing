#!/usr/bin/env python3
import re

# Read the entire video file
with open('nature.mp4', 'rb') as f:
    data = f.read()

print(f"File size: {len(data)} bytes")

# Try different search strategies
print("\n=== Strategy 1: Direct flag pattern search ===")
patterns = [
    rb'flag\{[A-Za-z0-9_]{10,}\}',
    rb'FLAG\{[A-Za-z0-9_]{10,}\}',
    rb'picoCTF\{[A-Za-z0-9_]{10,}\}',
    rb'[a-z]{4}\{[A-Za-z0-9_]{10,}\}',  # lowercase flag
    rb'[A-Z]{4}\{[A-Za-z0-9_]{10,}\}',  # uppercase FLAG
]

for pattern in patterns:
    matches = re.findall(pattern, data)
    if matches:
        for match in matches:
            print(f"FOUND: {match.decode('utf-8', errors='ignore')}")

print("\n=== Strategy 2: Search in readable ASCII sections ===")
# Find all readable ASCII sections
ascii_sections = re.findall(rb'[ -~]{50,}', data)
for i, section in enumerate(ascii_sections[:20]):
    decoded = section.decode('utf-8', errors='ignore')
    # Look for flag-like patterns
    if re.search(r'[fF][lL][aA][gG]', decoded):
        print(f"Section {i}: {decoded[:200]}")

print("\n=== Strategy 3: Check MP4 metadata atoms ===")
# MP4 files have atoms/boxes - check 'udta' (user data) and 'meta' atoms
i = 0
while i < len(data) - 8:
    if i + 8 > len(data):
        break
    size = int.from_bytes(data[i:i+4], 'big')
    if size == 0 or size > len(data) or size < 8:
        i += 1
        continue
    
    box_type = data[i+4:i+8]
    if box_type in [b'udta', b'meta', b'ilst']:
        box_data = data[i+8:min(i+size, len(data))]
        # Search for flags in this box
        text = box_data.decode('utf-8', errors='ignore')
        flag_matches = re.findall(r'[fF][lL][aA][gG]\{[^}]+\}', text)
        if flag_matches:
            print(f"Found in {box_type.decode()}: {flag_matches}")
        # Also print readable text from this box
        readable = re.findall(r'[ -~]{20,}', box_data)
        for r in readable[:5]:
            decoded_r = r.decode('utf-8', errors='ignore')
            if len(decoded_r) > 10:
                print(f"  Text in {box_type.decode()}: {decoded_r[:100]}")
    
    i += size
    if i >= len(data) - 8:
        break

print("\n=== Strategy 4: XOR analysis ===")
# Sometimes flags are XORed with a key
for key in [0x42, 0x55, 0xAA, 0xFF]:
    xor_data = bytes([b ^ key for b in data[:10000]])  # Check first 10KB
    text = xor_data.decode('utf-8', errors='ignore')
    flag_matches = re.findall(r'[fF][lL][aA][gG]\{[^}]+\}', text)
    if flag_matches:
        print(f"Found with XOR key 0x{key:02X}: {flag_matches}")

print("\n=== Strategy 5: Check end of file ===")
# Sometimes flags are appended at the end
end_data = data[-1000:]
text = end_data.decode('utf-8', errors='ignore')
flag_matches = re.findall(r'[fF][lL][aA][gG]\{[^}]+\}', text)
if flag_matches:
    print(f"Found at end of file: {flag_matches}")
else:
    print("Last 200 bytes as text:", repr(text[-200:]))
