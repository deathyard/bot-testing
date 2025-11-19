#!/usr/bin/env python3
"""
Script to connect to nusock1-2447.ctf.nutanix.com and retrieve the flag.
This script tries multiple connection methods.
"""

import socket
import ssl
import requests
import time
import sys

HOST = 'nusock1-2447.ctf.nutanix.com'
PORTS = [80, 443, 8080, 8443, 3000, 5000, 8000, 9999]

def try_socket_connection(host, port, timeout=10):
    """Try a raw socket connection"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        if result == 0:
            print(f"[+] Port {port} is open!")
            return sock
        sock.close()
    except Exception as e:
        pass
    return None

def try_https_request(host, port=443, path="/"):
    """Try HTTPS request"""
    url = f"https://{host}:{port}{path}"
    try:
        r = requests.get(url, timeout=10, verify=False)
        print(f"[+] HTTPS Response ({path}):")
        print(f"    Status: {r.status_code}")
        print(f"    Headers: {dict(r.headers)}")
        print(f"    Body: {r.text[:500]}")
        return r.text
    except Exception as e:
        return None

def try_custom_protocol(host, port):
    """Try sending custom messages"""
    sock = try_socket_connection(host, port)
    if sock:
        messages = [
            b"FLAG\n",
            b"GETFLAG\n",
            b"flag\n",
            b"HELLO\n",
            b"PING\n",
        ]
        for msg in messages:
            try:
                sock.sendall(msg)
                response = sock.recv(4096)
                if response:
                    print(f"[+] Response to '{msg.decode()}': {response}")
                    if b'flag' in response.lower() or b'ctf' in response.lower():
                        print(f"[!] FLAG FOUND: {response}")
                        return response
            except:
                pass
        sock.close()
    return None

def main():
    print(f"Attempting to connect to {HOST}...")
    print("=" * 60)
    
    # Try HTTPS first
    print("\n[1] Trying HTTPS requests...")
    paths = ["/", "/flag", "/api/flag", "/getflag", "/challenge"]
    for path in paths:
        result = try_https_request(HOST, 443, path)
        if result and ('flag' in result.lower() or 'ctf' in result.lower()):
            print(f"\n[!] FLAG FOUND in response!")
            return
    
    # Try socket connections
    print("\n[2] Trying socket connections...")
    for port in PORTS:
        print(f"    Trying port {port}...", end='\r')
        result = try_custom_protocol(HOST, port)
        if result:
            return
    
    print("\n[3] All connection attempts failed.")
    print("    The server may require:")
    print("    - VPN or specific network access")
    print("    - Authentication headers")
    print("    - A specific client tool")

if __name__ == "__main__":
    main()
