#!/usr/bin/env python3
import base64
import binascii
import urllib.parse

url = "https://nusock1-2447.ctf.nutanix.com/"
subdomain = "nusock1-2447"

print("=" * 70)
print("Comprehensive URL/Subdomain Decoder")
print("=" * 70)

# Try different interpretations
print("\n1. Full subdomain:", subdomain)
print("2. Numbers only:", ''.join(filter(str.isdigit, subdomain)))
print("3. Letters only:", ''.join(filter(str.isalpha, subdomain)))

# Try base64 decoding with different padding
print("\n--- Base64 Decoding ---")
for padding in ['', '=', '==', '===']:
    try:
        decoded = base64.b64decode(subdomain + padding)
        print(f"  Base64{subdomain + padding}: {decoded} -> {decoded.decode('utf-8', errors='ignore')}")
    except:
        pass

# Try URL-safe base64
for padding in ['', '=', '==', '===']:
    try:
        decoded = base64.urlsafe_b64decode(subdomain + padding)
        print(f"  Base64URL{subdomain + padding}: {decoded} -> {decoded.decode('utf-8', errors='ignore')}")
    except:
        pass

# Try hex decoding
print("\n--- Hex Decoding ---")
hex_variants = [
    subdomain.replace('-', ''),
    subdomain.replace('-', '').upper(),
    ''.join([hex(ord(c))[2:] for c in subdomain]),
]
for variant in hex_variants:
    try:
        if len(variant) % 2 == 0:
            decoded = binascii.unhexlify(variant)
            print(f"  Hex {variant}: {decoded} -> {decoded.decode('utf-8', errors='ignore')}")
    except:
        pass

# Try ROT13
print("\n--- ROT13 ---")
try:
    import codecs
    rot13 = codecs.encode(subdomain, 'rot13')
    print(f"  ROT13: {rot13}")
except:
    pass

# Try ASCII codes
print("\n--- ASCII Code Analysis ---")
ascii_codes = [ord(c) for c in subdomain]
print(f"  ASCII codes: {ascii_codes}")
print(f"  As string: {''.join([chr(c) if 32 <= c <= 126 else f'\\x{c:02x}' for c in ascii_codes])}")

# Try interpreting numbers as ASCII
numbers = ''.join(filter(str.isdigit, subdomain))
print(f"\n--- Numbers as ASCII ({numbers}) ---")
# Try 2-digit groups
for i in range(0, len(numbers)-1, 2):
    try:
        code = int(numbers[i:i+2])
        if 32 <= code <= 126:
            print(f"  {numbers[i:i+2]} -> {chr(code)}")
    except:
        pass

# Try 3-digit groups
for i in range(0, len(numbers)-2, 3):
    try:
        code = int(numbers[i:i+3])
        if 32 <= code <= 126:
            print(f"  {numbers[i:i+3]} -> {chr(code)}")
    except:
        pass

# Try interpreting as decimal then hex
print(f"\n--- Number as Decimal/Hex ---")
try:
    num = int(numbers)
    print(f"  Decimal: {num}")
    print(f"  Hex: {hex(num)}")
    print(f"  Hex as ASCII: {bytes.fromhex(hex(num)[2:]).decode('utf-8', errors='ignore')}")
except:
    pass

# Try reversing
print("\n--- Reversed ---")
print(f"  Reversed subdomain: {subdomain[::-1]}")

# Try splitting and analyzing parts
print("\n--- Parts Analysis ---")
parts = subdomain.split('-')
for i, part in enumerate(parts):
    print(f"  Part {i+1}: {part}")
    # Try base64 on each part
    for padding in ['', '=', '==']:
        try:
            decoded = base64.b64decode(part + padding)
            print(f"    Base64: {decoded} -> {decoded.decode('utf-8', errors='ignore')}")
        except:
            pass

# Check if "nusock" is a hint (socket backwards?)
print("\n--- Word Play ---")
if 'nusock' in subdomain.lower():
    print("  'nusock' might be 'socket' backwards or related to network sockets")
    print("  'socket' backwards: socket[::-1] = tekcos")
    
# Try URL encoding/decoding
print("\n--- URL Encoding ---")
print(f"  URL encoded: {urllib.parse.quote(subdomain)}")
print(f"  URL decoded: {urllib.parse.unquote(subdomain)}")

# Check for flag patterns
print("\n--- Flag Pattern Search ---")
all_text = subdomain + numbers + ''.join(filter(str.isalpha, subdomain))
if 'flag' in all_text.lower():
    print(f"  Found 'flag' in: {all_text}")
if 'ctf' in all_text.lower():
    print(f"  Found 'ctf' in: {all_text}")

# Maybe the flag is just the numbers or a combination?
print("\n--- Potential Flag Formats ---")
potential_flags = [
    f"flag{{{numbers}}}",
    f"flag{{{subdomain}}}",
    f"CTF{{{numbers}}}",
    f"CTF{{{subdomain}}}",
    f"nutanix{{{numbers}}}",
    f"nutanix{{{subdomain}}}",
]
print("  Potential flags:")
for pf in potential_flags:
    print(f"    {pf}")
