#!/usr/bin/env python3
import socket
import ssl
import base64

hostname = "nusock1-2447.ctf.nutanix.com"
subdomain = "nusock1-2447"

print("=" * 70)
print("Socket Connection Attempts")
print("=" * 70)

# Try HTTP on port 80
print("\n--- Trying HTTP (port 80) ---")
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    sock.connect((hostname, 80))
    request = f"GET / HTTP/1.1\r\nHost: {hostname}\r\n\r\n"
    sock.send(request.encode())
    response = sock.recv(4096).decode('utf-8', errors='ignore')
    print(f"Response:\n{response[:500]}")
    sock.close()
except Exception as e:
    print(f"Error: {e}")

# Try HTTPS on port 443
print("\n--- Trying HTTPS (port 443) ---")
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    sock.connect((hostname, 443))
    context = ssl.create_default_context()
    ssock = context.wrap_socket(sock, server_hostname=hostname)
    request = f"GET / HTTP/1.1\r\nHost: {hostname}\r\n\r\n"
    ssock.send(request.encode())
    response = ssock.recv(4096).decode('utf-8', errors='ignore')
    print(f"Response:\n{response[:500]}")
    ssock.close()
except Exception as e:
    print(f"Error: {e}")

# Try port 2447 (the number in the subdomain!)
print("\n--- Trying port 2447 (from subdomain) ---")
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    sock.connect((hostname, 2447))
    request = f"GET / HTTP/1.1\r\nHost: {hostname}\r\n\r\n"
    sock.send(request.encode())
    response = sock.recv(4096).decode('utf-8', errors='ignore')
    print(f"Response:\n{response[:500]}")
    if 'flag' in response.lower():
        print("\n*** FLAG FOUND IN RESPONSE ***")
        print(response)
    sock.close()
except Exception as e:
    print(f"Error: {e}")

# Try interpreting "nusock" as a hint - maybe it's "socket" related
# "nusock" backwards is "kcosun" - not helpful
# But wait - what if "nusock1" means "no socket 1" or something?
# Or maybe it's "new socket" abbreviated?

# Let's also check if the flag might be in the subdomain when interpreted differently
print("\n--- Subdomain Analysis for Flag ---")
print(f"Subdomain: {subdomain}")

# Maybe "nusock1-2447" decodes to a flag?
# Try treating it as base32
try:
    import base64
    # base32 uses A-Z and 2-7
    # "nusock1-2447" has lowercase and dash, so maybe uppercase it?
    b32_str = subdomain.upper().replace('-', '')
    decoded = base64.b32decode(b32_str + '======')
    print(f"Base32 decode: {decoded} -> {decoded.decode('utf-8', errors='ignore')}")
except Exception as e:
    print(f"Base32 error: {e}")

# Maybe the flag format is flag{nusock1-2447} or flag{2447}?
print("\n--- Potential Flags ---")
print(f"flag{{{subdomain}}}")
print(f"flag{{2447}}")
print(f"flag{{12447}}")
print(f"CTF{{{subdomain}}}")
print(f"nutanix{{{subdomain}}}")
