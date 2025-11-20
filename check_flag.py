#!/usr/bin/env python3
# Check if flag might be in DNS TXT record or domain name
import subprocess

domain = "nusock1-2447.ctf.nutanix.com"

# Get all TXT records
result = subprocess.run(['dig', 'TXT', domain, '+short'], capture_output=True, text=True)
txt_records = result.stdout.strip().split('\n')
print("TXT Records:")
for txt in txt_records:
    if txt:
        print(f"  {txt}")
        # Remove quotes and check for flag-like patterns
        cleaned = txt.strip('"')
        if 'flag' in cleaned.lower() or 'ctf' in cleaned.lower() or cleaned.startswith('NTNX'):
            print(f"  → Potential flag: {cleaned}")

# Check A records
result = subprocess.run(['dig', 'A', domain, '+short'], capture_output=True, text=True)
ips = result.stdout.strip().split('\n')
print(f"\nIP Addresses: {', '.join(ips)}")

# Maybe the flag is encoded in the IPs or domain?
print(f"\nDomain: {domain}")
print(f"Port from URL: 2447")

# Check if 2447 in hex or other encoding might be relevant
print(f"\n2447 in hex: {hex(2447)}")
print(f"2447 in binary: {bin(2447)}")
