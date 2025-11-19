#!/usr/bin/env python3
import base64
import binascii
import urllib.parse
import urllib.request
import urllib.error
from urllib.parse import urlparse
import socket

url = "https://nusock1-2447.ctf.nutanix.com/"

print("=" * 60)
print("CTF Flag Finder")
print("=" * 60)

# Extract hostname components
hostname = urlparse(url).hostname
print(f"\nHostname: {hostname}")

# Try to decode the subdomain part
subdomain = hostname.split('.')[0]  # nusock1-2447
print(f"\nSubdomain: {subdomain}")

# Try various decoding methods
print("\n--- Trying different decodings of subdomain ---")

# Base64 decode
try:
    decoded = base64.b64decode(subdomain + '==')
    print(f"Base64 decode: {decoded}")
except:
    pass

try:
    decoded = base64.urlsafe_b64decode(subdomain + '==')
    print(f"Base64 URL-safe decode: {decoded}")
except:
    pass

# Hex decode
try:
    decoded = binascii.unhexlify(subdomain.replace('-', ''))
    print(f"Hex decode: {decoded}")
except:
    pass

# Try extracting numbers
numbers = ''.join(filter(str.isdigit, subdomain))
print(f"Numbers extracted: {numbers}")

# Try HTTP requests with different methods and headers
print("\n--- Trying HTTP requests ---")

req = urllib.request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
req.add_header('Accept', '*/*')

try:
    print("Trying GET request...")
    with urllib.request.urlopen(req, timeout=5) as response:
        print(f"Status: {response.status}")
        print(f"Headers: {dict(response.headers)}")
        content = response.read().decode('utf-8', errors='ignore')
        print(f"Response (first 500 chars): {content[:500]}")
        if 'flag' in content.lower() or 'ctf' in content.lower():
            print("*** POTENTIAL FLAG FOUND IN RESPONSE ***")
            print(content)
except urllib.error.URLError as e:
    print(f"URL error: {e}")
except socket.timeout:
    print("Request timed out")
except Exception as e:
    print(f"Error: {e}")

# Try HEAD request
try:
    print("\nTrying HEAD request...")
    req.get_method = lambda: 'HEAD'
    with urllib.request.urlopen(req, timeout=5) as response:
        print(f"Status: {response.status}")
        print(f"Headers: {dict(response.headers)}")
        # Check headers for flag
        headers_str = str(dict(response.headers))
        if 'flag' in headers_str.lower():
            print("*** POTENTIAL FLAG FOUND IN HEADERS ***")
            print(headers_str)
except Exception as e:
    print(f"HEAD error: {e}")

# Try different paths
print("\n--- Trying different paths ---")
paths = ['/', '/flag', '/flag.txt', '/index.html', '/robots.txt', '/.well-known/flag']
for path in paths:
    try:
        test_url = url.rstrip('/') + path
        print(f"\nTrying: {test_url}")
        req = urllib.request.Request(test_url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        with urllib.request.urlopen(req, timeout=5) as response:
            print(f"Status: {response.status}")
            content = response.read().decode('utf-8', errors='ignore')
            if content:
                print(f"Response (first 300 chars): {content[:300]}")
    except Exception as e:
        print(f"Error: {e}")

# Check if flag is in URL encoding
print("\n--- Checking URL encoding ---")
print(f"URL encoded: {urllib.parse.quote(url)}")
print(f"URL decoded: {urllib.parse.unquote(url)}")

# Check subdomain for patterns
print("\n--- Analyzing subdomain pattern ---")
parts = subdomain.split('-')
print(f"Parts: {parts}")
for part in parts:
    print(f"  {part}: ascii={[ord(c) for c in part]}")

# Try decoding numbers as ASCII
print("\n--- Trying number to ASCII conversion ---")
for num_str in numbers:
    try:
        ascii_char = chr(int(num_str))
        print(f"  {num_str} -> {ascii_char}")
    except:
        pass

# Try the full number sequence
if len(numbers) > 0:
    print(f"\nFull number sequence: {numbers}")
    # Try as decimal ASCII codes
    try:
        # Split into 2-digit or 3-digit numbers
        for i in range(0, len(numbers), 2):
            if i+2 <= len(numbers):
                code = int(numbers[i:i+2])
                if 32 <= code <= 126:  # Printable ASCII
                    print(f"  {numbers[i:i+2]} -> {chr(code)}")
    except:
        pass
