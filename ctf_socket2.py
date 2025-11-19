#!/usr/bin/env python3
import socket
import ssl
import time

def try_raw_socket(host, port, use_ssl=False):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        
        print(f"Connecting to {host}:{port}...")
        sock.connect((host, port))
        print(f"✓ Connected!")
        
        if use_ssl:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            sock = context.wrap_socket(sock, server_hostname=host)
            print("✓ SSL handshake complete")
        
        # Try sending HTTP request
        request = f"GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        sock.send(request.encode())
        print("✓ Request sent")
        
        # Try to receive response
        response = b""
        sock.settimeout(2)
        try:
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response += chunk
        except socket.timeout:
            pass
        
        if response:
            print("\n=== Response ===")
            print(response.decode('utf-8', errors='ignore'))
            print("===============\n")
        
        sock.close()
        return True
    except socket.timeout:
        print(f"✗ Connection timed out")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

host = "nusock1-2447.ctf.nutanix.com"
ips = ["52.201.139.216", "3.95.117.251", "54.90.7.206"]

# Try port 2447 first (from URL)
print("=== Trying port 2447 ===")
for ip in ips:
    print(f"\nTrying {ip}:2447")
    try_raw_socket(ip, 2447, use_ssl=False)
    try_raw_socket(ip, 2447, use_ssl=True)

# Try common ports
print("\n\n=== Trying common ports ===")
ports = [443, 80, 8080, 8443, 3000, 8000, 1337, 9999]
for port in ports:
    print(f"\n=== Port {port} ===")
    for ip in ips[:1]:  # Just try first IP to save time
        if port == 443:
            try_raw_socket(ip, port, use_ssl=True)
        else:
            try_raw_socket(ip, port, use_ssl=False)
