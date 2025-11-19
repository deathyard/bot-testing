#!/usr/bin/env python3
import socket
import ssl
from urllib.parse import urlparse
from urllib.request import urlopen, Request
import urllib.error

url = "https://nusock1-2447.ctf.nutanix.com/"

print("Attempting to connect to:", url)

# Try with urllib
try:
    print("\n=== Trying with urllib ===")
    req = Request(url)
    response = urlopen(req, timeout=10)
    print(f"Status Code: {response.getcode()}")
    print(f"Headers: {dict(response.headers)}")
    content = response.read().decode('utf-8', errors='ignore')
    print(f"Content: {content[:1000]}")
except Exception as e:
    print(f"Urllib failed: {e}")

# Try raw socket connection
try:
    print("\n=== Trying raw socket connection ===")
    parsed = urlparse(url)
    host = parsed.hostname
    port = parsed.port or 443
    
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    sock = socket.create_connection((host, port), timeout=10)
    ssock = context.wrap_socket(sock, server_hostname=host)
    
    request = f"GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
    ssock.send(request.encode())
    
    response = ssock.recv(4096).decode('utf-8', errors='ignore')
    print(response)
    ssock.close()
except Exception as e:
    print(f"Socket connection failed: {e}")

# Try different paths
paths = ["/", "/flag", "/flag.txt", "/robots.txt", "/.well-known/", "/index.html"]
for path in paths:
    try:
        print(f"\n=== Trying {path} ===")
        full_url = url + path.lstrip('/')
        req = Request(full_url)
        response = urlopen(req, timeout=5)
        print(f"Status: {response.getcode()}")
        content = response.read().decode('utf-8', errors='ignore')
        if content:
            print(f"Content: {content[:500]}")
    except Exception as e:
        print(f"Failed: {e}")
