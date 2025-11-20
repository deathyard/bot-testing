# CTF Challenge Analysis: nusock1-2447.ctf.nutanix.com

## Challenge URL
https://nusock1-2447.ctf.nutanix.com/

## Findings

### DNS Resolution
- **Domain**: nusock1-2447.ctf.nutanix.com
- **IP Addresses**:
  - 52.201.139.216
  - 3.95.117.251
  - 54.90.7.206

### DNS Records
- **TXT Record**: "heritage=external-dns,external-dns/owner=default,external-dns/resource=ingress/challenges/challenges-ingress"
- **A Records**: 3 IPs resolved successfully
- **No CNAME, MX, or other special records found**

### Connection Attempts
All connection attempts to the server result in timeouts:
- HTTPS (port 443): Connection timeout
- HTTP (port 80): Connection timeout
- Port 2447 (from URL): Connection timeout
- Other common ports (8080, 8443, 3000, 8000, 1337, 9999): All timeout
- UDP connections: No response
- SSL/TLS handshake: Timeout

### Analysis
1. **Challenge Name**: "nusock1" suggests this is a socket programming challenge
2. **Port 2447**: Present in the URL, may be significant
3. **Network Access**: Server appears to be blocking connections from this environment
   - May require VPN access
   - May only be accessible from specific networks
   - May require authentication or specific headers

### Encoded Values (for reference)
- Base64: bnVzb2NrMS0yNDQ3LmN0Zi5udXRhbml4LmNvbQ==
- Hex: 6e75736f636b312d323434372e6374662e6e7574616e69782e636f6d
- MD5: e4aefb6cd4a26f3f5269482d79f86bc3
- SHA256: 7aee8ac7a8c8ade688e0827546464e02dc4e7d4875f822661ebbae72062ee6f1

## Conclusion
Unable to retrieve the flag due to connection timeouts. The server may require:
- VPN access
- Specific network location
- Special authentication
- Different connection method/protocol
