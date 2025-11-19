#!/usr/bin/env python3
import socket
import ssl
import sys

def try_http():
    """Try HTTP connection"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        context = ssl.create_default_context()
        wrapped = context.wrap_socket(sock, server_hostname='nusock1-2447.ctf.nutanix.com')
        wrapped.connect(('nusock1-2447.ctf.nutanix.com', 443))
        
        request = "GET / HTTP/1.1\r\nHost: nusock1-2447.ctf.nutanix.com\r\nConnection: close\r\n\r\n"
        wrapped.send(request.encode())
        
        response = wrapped.recv(4096).decode()
        print("HTTP Response:")
        print(response)
        wrapped.close()
        return response
    except Exception as e:
        print(f"HTTP failed: {e}")
        return None

def try_websocket():
    """Try WebSocket connection"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        context = ssl.create_default_context()
        wrapped = context.wrap_socket(sock, server_hostname='nusock1-2447.ctf.nutanix.com')
        wrapped.connect(('nusock1-2447.ctf.nutanix.com', 443))
        
        # WebSocket handshake
        key = "dGhlIHNhbXBsZSBub25jZQ=="
        request = (
            "GET / HTTP/1.1\r\n"
            "Host: nusock1-2447.ctf.nutanix.com\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            "Sec-WebSocket-Version: 13\r\n"
            "\r\n"
        )
        wrapped.send(request.encode())
        
        response = wrapped.recv(4096).decode()
        print("WebSocket Response:")
        print(response)
        wrapped.close()
        return response
    except Exception as e:
        print(f"WebSocket failed: {e}")
        return None

def try_ports():
    """Try different ports"""
    ports = [80, 443, 8080, 8443, 3000, 8000]
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex(('nusock1-2447.ctf.nutanix.com', port))
            if result == 0:
                print(f"Port {port} is open!")
                sock.close()
            else:
                print(f"Port {port} is closed")
        except Exception as e:
            print(f"Port {port} error: {e}")

if __name__ == "__main__":
    print("Trying HTTP...")
    try_http()
    print("\nTrying WebSocket...")
    try_websocket()
    print("\nTrying different ports...")
    try_ports()
