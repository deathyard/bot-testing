#!/usr/bin/env python3
import socket

def try_udp(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(3)
        
        # Send a simple message
        message = b"GET / HTTP/1.1\r\nHost: " + host.encode() + b"\r\n\r\n"
        sock.sendto(message, (host, port))
        print(f"Sent UDP packet to {host}:{port}")
        
        # Try to receive response
        try:
            data, addr = sock.recvfrom(4096)
            print(f"Received from {addr}:")
            print(data.decode('utf-8', errors='ignore'))
            return True
        except socket.timeout:
            print("No response received")
            return False
        
    except Exception as e:
        print(f"Error: {e}")
        return False

host = "nusock1-2447.ctf.nutanix.com"
ips = ["52.201.139.216", "3.95.117.251", "54.90.7.206"]

print("=== Trying UDP on port 2447 ===")
for ip in ips:
    print(f"\nTrying {ip}:2447")
    try_udp(ip, 2447)

print("\n=== Trying UDP on common ports ===")
ports = [53, 123, 161, 2447, 9999]
for port in ports:
    print(f"\nPort {port}:")
    try_udp(ips[0], port)
