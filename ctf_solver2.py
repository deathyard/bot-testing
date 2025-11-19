#!/usr/bin/env python3
import socket
import ssl
from urllib.parse import urlparse

url = "https://nusock1-2447.ctf.nutanix.com/"
parsed = urlparse(url)
host = parsed.hostname

print(f"Hostname: {host}")
print(f"Analyzing hostname for clues...")

# Check if there's anything encoded in the hostname
print(f"\nHostname parts: {host.split('.')}")

# Try different ports
ports = [80, 443, 8080, 8443, 3000, 8000, 2447]  # 2447 might be significant from the URL

for port in ports:
    print(f"\n=== Trying port {port} ===")
    try:
        if port == 443:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            sock = socket.create_connection((host, port), timeout=5)
            ssock = context.wrap_socket(sock, server_hostname=host)
            request = f"GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
            ssock.send(request.encode())
            response = ssock.recv(4096).decode('utf-8', errors='ignore')
            print(response[:500])
            ssock.close()
        else:
            sock = socket.create_connection((host, port), timeout=5)
            request = f"GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
            sock.send(request.encode())
            response = sock.recv(4096).decode('utf-8', errors='ignore')
            print(response[:500])
            sock.close()
    except socket.timeout:
        print(f"Timeout on port {port}")
    except Exception as e:
        print(f"Error on port {port}: {e}")

# Check if the number 2447 in the URL is significant
print(f"\n=== Checking if 2447 is a port or hint ===")
try:
    sock = socket.create_connection((host, 2447), timeout=5)
    request = f"GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
    sock.send(request.encode())
    response = sock.recv(4096).decode('utf-8', errors='ignore')
    print(response)
    sock.close()
except Exception as e:
    print(f"Port 2447 failed: {e}")

# Maybe the flag is in the URL itself or needs to be decoded
print(f"\n=== Analyzing URL components ===")
print(f"Full URL: {url}")
print(f"Path: {parsed.path}")
print(f"Query: {parsed.query}")
print(f"Fragment: {parsed.fragment}")

# Check if "nusock1" or "2447" contain encoded data
import base64
try:
    # Try base64 decoding parts of the hostname
    parts = host.split('.')
    for part in parts:
        if part and len(part) > 4:
            try:
                decoded = base64.b64decode(part + '==')
                print(f"Base64 decode of '{part}': {decoded}")
            except:
                pass
except:
    pass
