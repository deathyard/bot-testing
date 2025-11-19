#!/usr/bin/env python3
import socket
import ssl
from urllib.parse import urlparse
from urllib.request import urlopen, Request
import urllib.error

host = "nusock1-2447.ctf.nutanix.com"

# Try HTTP instead of HTTPS
print("=== Trying HTTP ===")
try:
    req = Request(f"http://{host}/")
    response = urlopen(req, timeout=10)
    print(f"Status: {response.getcode()}")
    print(response.read().decode('utf-8', errors='ignore')[:1000])
except Exception as e:
    print(f"HTTP failed: {e}")

# Try with different User-Agents
user_agents = [
    "Mozilla/5.0",
    "curl/7.68.0",
    "python-urllib/3.8",
    "CTF-Bot/1.0"
]

for ua in user_agents:
    try:
        print(f"\n=== Trying with User-Agent: {ua} ===")
        req = Request(f"https://{host}/")
        req.add_header('User-Agent', ua)
        response = urlopen(req, timeout=5)
        print(f"Status: {response.getcode()}")
        print(response.read().decode('utf-8', errors='ignore')[:500])
    except Exception as e:
        print(f"Failed: {str(e)[:100]}")

# Try raw socket with different HTTP versions
print("\n=== Trying HTTP/1.0 ===")
try:
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    sock = socket.create_connection((host, 443), timeout=10)
    ssock = context.wrap_socket(sock, server_hostname=host)
    request = f"GET / HTTP/1.0\r\nHost: {host}\r\n\r\n"
    ssock.send(request.encode())
    response = ssock.recv(8192).decode('utf-8', errors='ignore')
    print(response[:1000])
    ssock.close()
except Exception as e:
    print(f"HTTP/1.0 failed: {e}")

# Check if flag is in the domain name itself
print("\n=== Analyzing domain name for encoded flag ===")
domain_parts = host.split('.')
for part in domain_parts:
    print(f"\nPart: {part}")
    # Try hex decoding
    try:
        if len(part) % 2 == 0:
            hex_decoded = bytes.fromhex(part).decode('utf-8', errors='ignore')
            if any(c.isprintable() for c in hex_decoded):
                print(f"  Hex decode: {hex_decoded}")
    except:
        pass
    
    # Try base64
    import base64
    for padding in ['', '=', '==', '===']:
        try:
            b64_decoded = base64.b64decode(part + padding).decode('utf-8', errors='ignore')
            if 'flag' in b64_decoded.lower() or 'ctf' in b64_decoded.lower():
                print(f"  Base64 decode (with '{padding}'): {b64_decoded}")
        except:
            pass

# Check if 2447 is significant
print(f"\n=== Checking number 2447 ===")
print(f"2447 in decimal: {2447}")
print(f"2447 in hex: {hex(2447)}")
print(f"2447 in binary: {bin(2447)}")
# Maybe it's a port or offset
print(f"Trying port 2447...")
try:
    sock = socket.create_connection((host, 2447), timeout=5)
    request = f"GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
    sock.send(request.encode())
    response = sock.recv(4096).decode('utf-8', errors='ignore')
    print(response)
    sock.close()
except Exception as e:
    print(f"Port 2447 failed: {e}")
