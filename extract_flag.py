#!/usr/bin/env python3
# Extract flag from stegno_1.jpg

with open('/workspace/stegno_1.jpg', 'rb') as f:
    content = f.read()
    
# Find where binary data starts (after JPEG end marker)
end_pos = content.find(b'\xff\xd9')
if end_pos != -1:
    # Get data after end marker
    extra_data = content[end_pos+2:]
    
    # Extract binary string - the data contains ASCII '0' and '1' characters
    binary_str = ''
    for byte in extra_data:
        if byte == 48:  # ASCII '0'
            binary_str += '0'
        elif byte == 49:  # ASCII '1'
            binary_str += '1'
        else:
            # Stop if we hit non-binary characters, or continue
            pass
    
    print(f"Extracted binary string length: {len(binary_str)}")
    print(f"First 200 chars: {binary_str[:200]}")
    
    # Convert binary to ASCII
    if len(binary_str) >= 8:
        result = ''
        for i in range(0, len(binary_str)-7, 8):
            try:
                byte_val = int(binary_str[i:i+8], 2)
                if 32 <= byte_val <= 126:  # Printable ASCII
                    result += chr(byte_val)
                else:
                    result += '?'
            except:
                break
        print(f"\nDecoded flag: {result}")
        print(f"\nFull binary: {binary_str}")
