#!/usr/bin/env python3
import socket
import ssl
import time
import re

host = 'nusock1-2447.ctf.nutanix.com'
ports = [443, 80, 8080, 1337, 4444, 9999, 31337, 8443]

def try_connect(host, port, send_data=None, use_ssl=False):
    try:
        print(f"\n[*] Trying {host}:{port} (SSL: {use_ssl})...")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s.connect((host, port))
        print(f"[+] Connected to port {port}!")
        
        if use_ssl:
            try:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                s = context.wrap_socket(s, server_hostname=host)
                print("[+] SSL handshake successful")
            except Exception as e:
                print(f"[-] SSL error: {e}")
                s.close()
                return None
        
        # Try to receive initial data
        try:
            s.settimeout(2)
            data = s.recv(4096)
            if data:
                print(f"[*] Initial data received: {data.decode('utf-8', errors='ignore')[:500]}")
        except socket.timeout:
            print("[*] No initial data (timeout)")
        except Exception as e:
            print(f"[*] No initial data: {e}")
        
        # Send data if provided
        if send_data:
            print(f"[*] Sending: {send_data[:100]}")
            s.send(send_data.encode() if isinstance(send_data, str) else send_data)
            time.sleep(1)
        
        # Try to receive response
        try:
            s.settimeout(5)
            data = s.recv(4096)
            if data:
                response = data.decode('utf-8', errors='ignore')
                print(f"[+] Response received:\n{response[:2000]}")
                
                # Search for flags
                flags = re.findall(r'(flag\{[^}]+\}|CTF\{[^}]+\}|Nutanix\{[^}]+\}|FLAG\{[^}]+\})', response, re.IGNORECASE)
                if flags:
                    print(f"\n[!] FOUND FLAGS: {flags}")
                    return flags
        except socket.timeout:
            print("[*] No response (timeout)")
        except Exception as e:
            print(f"[*] No response: {e}")
        
        s.close()
        return None
    except socket.timeout:
        print(f"[-] Connection timeout")
        return None
    except Exception as e:
        print(f"[-] Connection failed: {e}")
        return None

# Try different ports and protocols
for port in ports:
    # Try without SSL first
    result = try_connect(host, port)
    if result:
        break
    
    # Try with SSL for HTTPS ports
    if port in [443, 8443]:
        result = try_connect(host, port, use_ssl=True)
        if result:
            break

# Try sending HTTP request
print("\n[*] Trying HTTP GET request...")
result = try_connect(host, 80, send_data=f"GET / HTTP/1.1\r\nHost: {host}\r\n\r\n")
if not result:
    result = try_connect(host, 443, send_data=f"GET / HTTP/1.1\r\nHost: {host}\r\n\r\n", use_ssl=True)

# Try sending raw socket data
print("\n[*] Trying raw socket interaction...")
for port in [1337, 4444, 9999]:
    result = try_connect(host, port, send_data="hello\n")
    if result:
        break

print("\n[*] Done")
