#!/usr/bin/env python3
"""Check if flag is encoded in the URL/domain name"""
import base64
import binascii
from urllib.parse import unquote

host = "nusock1-2447.ctf.nutanix.com"
parts = host.split('.')

print("Checking if flag is encoded in domain name...")
print("=" * 60)

for part in parts:
    print(f"\nPart: {part}")
    
    # Try various encodings
    encodings = []
    
    # Base64
    for padding in ['', '=', '==', '===']:
        try:
            decoded = base64.b64decode(part + padding)
            text = decoded.decode('utf-8', errors='ignore')
            if any(c.isprintable() for c in text) and len(text) > 1:
                encodings.append(('Base64', text))
        except:
            pass
    
    # Base32
    try:
        decoded = base64.b32decode(part + '====')
        text = decoded.decode('utf-8', errors='ignore')
        if any(c.isprintable() for c in text):
            encodings.append(('Base32', text))
    except:
        pass
    
    # Hex
    try:
        if len(part) % 2 == 0:
            decoded = bytes.fromhex(part)
            text = decoded.decode('utf-8', errors='ignore')
            if any(c.isprintable() for c in text):
                encodings.append(('Hex', text))
    except:
        pass
    
    # URL decode
    try:
        decoded = unquote(part)
        if decoded != part:
            encodings.append(('URL', decoded))
    except:
        pass
    
    # Check if it looks like a flag
    if 'flag' in part.lower() or 'ctf' in part.lower():
        print(f"  *** Contains 'flag' or 'ctf' ***")
    
    if encodings:
        for enc_type, text in encodings:
            print(f"  {enc_type}: {text}")
            if 'flag' in text.lower() or 'ctf{' in text.lower():
                print(f"    *** POTENTIAL FLAG FOUND ***")

# Check the number 2447
print(f"\n\nChecking number 2447:")
print(f"  Decimal: 2447")
print(f"  Hex: {hex(2447)} = {bytes.fromhex(hex(2447)[2:]).decode('utf-8', errors='ignore') if len(hex(2447)[2:]) % 2 == 0 else 'N/A'}")
print(f"  ASCII: {chr(2447 % 256) if 2447 < 256 else 'N/A'}")

# Maybe the flag format is flag{nusock1-2447} or similar
print(f"\n\nPossible flag formats:")
print(f"  flag{{nusock1-2447}}")
print(f"  CTF{{nusock1-2447}}")
print(f"  flag{{nusock1}}")
print(f"  flag{{2447}}")
