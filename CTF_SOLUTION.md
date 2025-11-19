# CTF Challenge: nusock1-2447.ctf.nutanix.com

## Problem
Find the flag at: https://nusock1-2447.ctf.nutanix.com/

## Current Status
**The server is not accessible from this environment** - all connection attempts timeout. This is likely due to network restrictions or firewall rules.

## What I've Tried

1. **Standard HTTPS requests** - Timeout
2. **HTTP requests** - Timeout  
3. **Raw socket connections** - Timeout
4. **Different ports** (80, 443, 8080, 2447, etc.) - Timeout
5. **Custom headers** - Cannot test (connection fails)
6. **Different URL paths** - Cannot test (connection fails)
7. **DNS queries** - Successfully resolves to:
   - 52.201.139.216
   - 54.90.7.206
   - 3.95.117.251
8. **Domain name analysis** - No obvious flag encoding found

## Solution Scripts Created

I've created two Python scripts you can run from your own environment:

1. **`find_flag.py`** - Comprehensive script that tries:
   - Standard HTTP/HTTPS requests
   - Custom headers
   - Different URL paths
   - Raw socket connections
   - Domain name analysis

2. **`check_url_encoding.py`** - Checks if flag is encoded in the domain name

## Next Steps

Since the server is not accessible from this environment, you should:

1. **Run the scripts from your local machine** or an environment that can access the CTF network:
   ```bash
   python3 find_flag.py
   ```

2. **Try accessing the URL directly** in a web browser and check:
   - Page source
   - HTTP headers (use browser dev tools)
   - Cookies
   - JavaScript console

3. **Try common CTF techniques**:
   - Check `/robots.txt`
   - Check `/flag` or `/flag.txt`
   - Check response headers for flags
   - Try different HTTP methods (POST, PUT, etc.)
   - Check if authentication is required

4. **Given the challenge name "nusock1"**, it might require:
   - A specific socket connection method
   - A custom protocol
   - Specific headers or authentication

## DNS Information
- **Hostname**: nusock1-2447.ctf.nutanix.com
- **IP Addresses**: 52.201.139.216, 54.90.7.206, 3.95.117.251
- **TXT Record**: heritage=external-dns,external-dns/owner=default,external-dns/resource=ingress/challenges/challenges-ingress

## Note
The number "2447" in the hostname might be significant - it could be:
- A port number
- Part of the flag
- An encoded value

Run the provided scripts from an environment that can access the CTF network to find the actual flag.
