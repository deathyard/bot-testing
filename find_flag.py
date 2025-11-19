#!/usr/bin/env python3
"""
CTF Flag Finder for nusock1-2447.ctf.nutanix.com
This script attempts various methods to find the flag.
"""
import socket
import ssl
from urllib.parse import urlparse
from urllib.request import urlopen, Request, build_opener, HTTPHandler, HTTPSHandler
import urllib.error
import base64
import binascii

URL = "https://nusock1-2447.ctf.nutanix.com/"
HOST = "nusock1-2447.ctf.nutanix.com"

def try_standard_request():
    """Try standard HTTP/HTTPS requests"""
    print("=" * 60)
    print("Method 1: Standard HTTPS Request")
    print("=" * 60)
    try:
        req = Request(URL)
        response = urlopen(req, timeout=10)
        content = response.read().decode('utf-8', errors='ignore')
        headers = dict(response.headers)
        
        print(f"Status: {response.getcode()}")
        print(f"Headers: {headers}")
        print(f"Content:\n{content}")
        
        # Search for flag in content
        if 'flag' in content.lower() or 'ctf{' in content.lower():
            print("\n*** FLAG FOUND IN CONTENT ***")
            import re
            flags = re.findall(r'(flag\{[^}]+\}|CTF\{[^}]+\}|FLAG\{[^}]+\})', content, re.IGNORECASE)
            if flags:
                print(f"FLAGS: {flags}")
        
        # Search for flag in headers
        for key, value in headers.items():
            if 'flag' in str(value).lower():
                print(f"\n*** FLAG FOUND IN HEADER {key}: {value} ***")
        
        return content
    except Exception as e:
        print(f"Failed: {e}")
    return None

def try_custom_headers():
    """Try requests with various custom headers"""
    print("\n" + "=" * 60)
    print("Method 2: Custom Headers")
    print("=" * 60)
    
    headers_to_try = [
        {'User-Agent': 'CTF-Bot'},
        {'X-Flag': 'please'},
        {'X-Forwarded-For': '127.0.0.1'},
        {'Referer': 'https://ctf.nutanix.com/'},
    ]
    
    for headers in headers_to_try:
        try:
            print(f"\nTrying headers: {headers}")
            req = Request(URL)
            for key, value in headers.items():
                req.add_header(key, value)
            response = urlopen(req, timeout=5)
            content = response.read().decode('utf-8', errors='ignore')
            print(f"Status: {response.getcode()}")
            if 'flag' in content.lower():
                print(f"*** FLAG FOUND: {content} ***")
        except Exception as e:
            print(f"Failed: {str(e)[:100]}")

def try_different_paths():
    """Try different URL paths"""
    print("\n" + "=" * 60)
    print("Method 3: Different Paths")
    print("=" * 60)
    
    paths = [
        "/", "/flag", "/flag.txt", "/.flag", "/flag.html",
        "/robots.txt", "/sitemap.xml", "/.well-known/",
        "/api/flag", "/getflag", "/2447", "/nusock1"
    ]
    
    for path in paths:
        try:
            full_url = URL.rstrip('/') + path
            print(f"\nTrying: {full_url}")
            req = Request(full_url)
            response = urlopen(req, timeout=5)
            content = response.read().decode('utf-8', errors='ignore')
            print(f"Status: {response.getcode()}")
            if content and len(content) < 500:
                print(f"Content: {content}")
            if 'flag' in content.lower():
                print(f"*** FLAG FOUND: {content} ***")
        except Exception as e:
            pass

def try_socket_connection():
    """Try raw socket connection"""
    print("\n" + "=" * 60)
    print("Method 4: Raw Socket Connection")
    print("=" * 60)
    
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        sock = socket.create_connection((HOST, 443), timeout=10)
        ssock = context.wrap_socket(sock, server_hostname=HOST)
        
        # Try different HTTP requests
        requests = [
            f"GET / HTTP/1.1\r\nHost: {HOST}\r\nConnection: close\r\n\r\n",
            f"GET / HTTP/1.0\r\nHost: {HOST}\r\n\r\n",
            f"GET /flag HTTP/1.1\r\nHost: {HOST}\r\nConnection: close\r\n\r\n",
        ]
        
        for req in requests:
            try:
                ssock.send(req.encode())
                response = ssock.recv(8192).decode('utf-8', errors='ignore')
                print(f"\nResponse:\n{response}")
                if 'flag' in response.lower():
                    print(f"*** FLAG FOUND IN RESPONSE ***")
            except:
                pass
        
        ssock.close()
    except Exception as e:
        print(f"Socket connection failed: {e}")

def analyze_domain():
    """Analyze domain name for encoded flags"""
    print("\n" + "=" * 60)
    print("Method 5: Domain Name Analysis")
    print("=" * 60)
    
    parts = HOST.split('.')
    for part in parts:
        print(f"\nAnalyzing: {part}")
        
        # Try base64
        for padding in ['', '=', '==', '===']:
            try:
                decoded = base64.b64decode(part + padding).decode('utf-8', errors='ignore')
                if any(c.isprintable() for c in decoded) and len(decoded) > 2:
                    print(f"  Base64 (padding '{padding}'): {decoded}")
            except:
                pass
        
        # Try hex
        try:
            if len(part) % 2 == 0:
                decoded = bytes.fromhex(part).decode('utf-8', errors='ignore')
                if any(c.isprintable() for c in decoded):
                    print(f"  Hex: {decoded}")
        except:
            pass
        
        # Try URL decode
        from urllib.parse import unquote
        try:
            decoded = unquote(part)
            if decoded != part:
                print(f"  URL decoded: {decoded}")
        except:
            pass

def main():
    print("CTF Flag Finder for nusock1-2447.ctf.nutanix.com")
    print("=" * 60)
    
    # Try all methods
    try_standard_request()
    try_custom_headers()
    try_different_paths()
    try_socket_connection()
    analyze_domain()
    
    print("\n" + "=" * 60)
    print("All methods completed. If no flag was found, the server")
    print("may not be accessible from this network, or requires")
    print("specific authentication/headers.")
    print("=" * 60)

if __name__ == "__main__":
    main()
