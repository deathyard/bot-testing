#!/usr/bin/env python3
"""
Script to find flag in CTF URL
"""
import urllib.request
import urllib.error
import socket
import ssl
import sys

def try_urllib():
    """Try using urllib"""
    try:
        url = 'https://nusock1-2447.ctf.nutanix.com/'
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode()
            headers = dict(response.headers)
            print("=== urllib Response ===")
            print(f"Status: {response.status}")
            print(f"Headers: {headers}")
            print(f"Body: {html[:500]}")
            
            # Check for flag in headers
            for key, value in headers.items():
                if 'flag' in key.lower() or 'flag' in value.lower():
                    print(f"FLAG FOUND IN HEADER: {key}: {value}")
            
            # Check for flag in body
            if 'flag' in html.lower() or 'FLAG' in html:
                import re
                flags = re.findall(r'[Ff][Ll][Aa][Gg]\{.*?\}|Nutanix\{.*?\}', html)
                if flags:
                    print(f"FLAG FOUND IN BODY: {flags}")
            return html, headers
    except urllib.error.URLError as e:
        print(f"urllib error: {e}")
    except Exception as e:
        print(f"urllib exception: {e}")
    return None, None

def try_http_with_custom_headers():
    """Try HTTP with various headers"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        context = ssl.create_default_context()
        wrapped = context.wrap_socket(sock, server_hostname='nusock1-2447.ctf.nutanix.com')
        wrapped.connect(('nusock1-2447.ctf.nutanix.com', 443))
        
        # Try with various headers
        headers = [
            "GET / HTTP/1.1\r\nHost: nusock1-2447.ctf.nutanix.com\r\nUser-Agent: Mozilla/5.0\r\nAccept: */*\r\nConnection: close\r\n\r\n",
            "GET / HTTP/1.1\r\nHost: nusock1-2447.ctf.nutanix.com\r\nX-Forwarded-For: 127.0.0.1\r\nConnection: close\r\n\r\n",
            "GET /flag HTTP/1.1\r\nHost: nusock1-2447.ctf.nutanix.com\r\nConnection: close\r\n\r\n",
            "GET /?flag HTTP/1.1\r\nHost: nusock1-2447.ctf.nutanix.com\r\nConnection: close\r\n\r\n",
        ]
        
        for i, request in enumerate(headers):
            try:
                wrapped.send(request.encode())
                response = wrapped.recv(8192).decode('utf-8', errors='ignore')
                print(f"\n=== Request {i+1} Response ===")
                print(response[:1000])
                
                # Check for flag
                if 'flag' in response.lower() or 'FLAG' in response:
                    import re
                    flags = re.findall(r'[Ff][Ll][Aa][Gg]\{.*?\}|Nutanix\{.*?\}', response)
                    if flags:
                        print(f"\n*** FLAG FOUND: {flags} ***")
                        return flags
            except Exception as e:
                print(f"Request {i+1} failed: {e}")
        
        wrapped.close()
    except Exception as e:
        print(f"Socket error: {e}")
    return None

def analyze_url():
    """Analyze the URL for hidden information"""
    url = "nusock1-2447.ctf.nutanix.com"
    print("\n=== URL Analysis ===")
    print(f"Original: {url}")
    
    # Try to decode parts
    parts = url.split('.')
    for part in parts:
        print(f"\nPart: {part}")
        # Try base64 decode
        try:
            import base64
            decoded = base64.b64decode(part + '==')
            print(f"  Base64 decoded: {decoded}")
        except:
            pass
        
        # Try hex decode
        try:
            if len(part) % 2 == 0:
                decoded = bytes.fromhex(part)
                print(f"  Hex decoded: {decoded}")
        except:
            pass

if __name__ == "__main__":
    print("Attempting to find flag...")
    
    # Analyze URL first
    analyze_url()
    
    # Try urllib
    print("\n" + "="*50)
    try_urllib()
    
    # Try custom headers
    print("\n" + "="*50)
    try_http_with_custom_headers()
