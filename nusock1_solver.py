#!/usr/bin/env python3
"""
CTF Challenge Solver for nusock1-2447.ctf.nutanix.com
This script attempts various methods to find the flag.
"""

import socket
import ssl
import time
import re
import http.client
import urllib.request

host = 'nusock1-2447.ctf.nutanix.com'
ports_to_try = [80, 443, 2447, 1337, 8080, 4444, 9999, 31337, 8443]

def search_for_flags(text):
    """Search for common flag patterns in text."""
    patterns = [
        r'flag\{[^}]+\}',
        r'CTF\{[^}]+\}',
        r'Nutanix\{[^}]+\}',
        r'FLAG\{[^}]+\}',
        r'nutanix\{[^}]+\}',
    ]
    flags = []
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        flags.extend(matches)
    return flags

def try_socket_connection(host, port, use_ssl=False, send_data=None):
    """Try connecting via raw socket."""
    try:
        print(f"[*] Trying socket connection to {host}:{port} (SSL: {use_ssl})...")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s.connect((host, port))
        print(f"[+] Connected!")
        
        if use_ssl:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            s = context.wrap_socket(s, server_hostname=host)
            print("[+] SSL handshake successful")
        
        # Receive initial data
        try:
            s.settimeout(2)
            data = s.recv(4096)
            if data:
                response = data.decode('utf-8', errors='ignore')
                print(f"[*] Initial data: {response[:500]}")
                flags = search_for_flags(response)
                if flags:
                    return flags
        except:
            pass
        
        # Send data if provided
        if send_data:
            if isinstance(send_data, str):
                send_data = send_data.encode()
            print(f"[*] Sending data...")
            s.send(send_data)
            time.sleep(1)
        
        # Receive response
        try:
            s.settimeout(5)
            data = s.recv(4096)
            if data:
                response = data.decode('utf-8', errors='ignore')
                print(f"[+] Response: {response[:1000]}")
                flags = search_for_flags(response)
                if flags:
                    return flags
        except:
            pass
        
        s.close()
        return None
    except Exception as e:
        print(f"[-] Failed: {e}")
        return None

def try_http_connection(host, port, use_ssl=False, path='/'):
    """Try connecting via HTTP/HTTPS."""
    try:
        print(f"[*] Trying HTTP{'S' if use_ssl else ''} connection to {host}:{port}{path}...")
        if use_ssl:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            conn = http.client.HTTPSConnection(host, port, timeout=10, context=context)
        else:
            conn = http.client.HTTPConnection(host, port, timeout=10)
        
        conn.request('GET', path)
        response = conn.getresponse()
        print(f"[+] Status: {response.status}")
        print(f"[+] Headers: {dict(response.headers)}")
        
        data = response.read().decode('utf-8', errors='ignore')
        print(f"[+] Content: {data[:1000]}")
        
        flags = search_for_flags(data)
        if flags:
            return flags
        
        # Also check headers for flags
        header_str = str(dict(response.headers))
        flags = search_for_flags(header_str)
        if flags:
            return flags
        
        conn.close()
        return None
    except Exception as e:
        print(f"[-] Failed: {e}")
        return None

def main():
    print("=" * 60)
    print("CTF Challenge Solver: nusock1-2447.ctf.nutanix.com")
    print("=" * 60)
    
    found_flags = []
    
    # Try HTTP/HTTPS connections
    for port in [80, 443]:
        use_ssl = (port == 443)
        result = try_http_connection(host, port, use_ssl=use_ssl)
        if result:
            found_flags.extend(result)
    
    # Try raw socket connections
    for port in ports_to_try:
        use_ssl = (port in [443, 8443])
        result = try_socket_connection(host, port, use_ssl=use_ssl)
        if result:
            found_flags.extend(result)
        
        # Try with HTTP GET request
        if port in [80, 443, 8080, 8443]:
            http_request = f"GET / HTTP/1.1\r\nHost: {host}\r\n\r\n"
            result = try_socket_connection(host, port, use_ssl=use_ssl, send_data=http_request)
            if result:
                found_flags.extend(result)
        
        # Try with simple hello
        if port not in [80, 443, 8080, 8443]:
            result = try_socket_connection(host, port, use_ssl=use_ssl, send_data=b"hello\n")
            if result:
                found_flags.extend(result)
    
    # Try common paths
    if not found_flags:
        print("\n[*] Trying common paths...")
        paths = ['/', '/flag', '/flag.txt', '/index.html', '/robots.txt', '/.well-known/flag']
        for path in paths:
            result = try_http_connection(host, 443, use_ssl=True, path=path)
            if result:
                found_flags.extend(result)
            result = try_http_connection(host, 80, use_ssl=False, path=path)
            if result:
                found_flags.extend(result)
    
    # Print results
    print("\n" + "=" * 60)
    if found_flags:
        print(f"[!] FOUND {len(found_flags)} FLAG(S):")
        for flag in set(found_flags):
            print(f"    {flag}")
    else:
        print("[!] No flags found. The server may not be accessible from this environment.")
        print("    Try running this script from a different network or check if the challenge is still active.")
    print("=" * 60)

if __name__ == '__main__':
    main()
