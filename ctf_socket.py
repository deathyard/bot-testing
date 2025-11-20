#!/usr/bin/env python3
import socket
import ssl
import sys

def try_connection(host, port, use_ssl=False):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        
        if use_ssl:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            sock = context.wrap_socket(sock, server_hostname=host)
        
        sock.connect((host, port))
        print(f"Connected to {host}:{port} (SSL: {use_ssl})")
        
        # Try sending HTTP request
        request = b"GET / HTTP/1.1\r\nHost: " + host.encode() + b"\r\n\r\n"
        sock.send(request)
        
        response = sock.recv(4096)
        print("Response:")
        print(response.decode('utf-8', errors='ignore'))
        
        sock.close()
        return True
    except Exception as e:
        print(f"Error connecting to {host}:{port} (SSL: {use_ssl}): {e}")
        return False

host = "nusock1-2447.ctf.nutanix.com"

# Try common ports
ports = [443, 80, 8080, 8443, 3000, 8000, 1337, 9999]

for port in ports:
    print(f"\n=== Trying port {port} ===")
    if port == 443:
        try_connection(host, port, use_ssl=True)
    else:
        try_connection(host, port, use_ssl=False)
        # Also try SSL on non-standard ports
        try_connection(host, port, use_ssl=True)
