# CTF Challenge: DNS Issues with nusecret5-2163.ctf.nutanix.com

## Summary of Issues Found

### 1. **Service Unavailability**
- **Issue**: HTTP/HTTPS ports (80, 443) are not responding
- **Details**: 
  - Domain resolves to IPs: `44.219.189.194`, `52.205.182.30`
  - Both IPs are AWS EC2 instances (us-east-1)
  - Connection attempts timeout after 260+ seconds
  - **Root Cause**: Service is down or firewalled

### 2. **Suspicious TTL Configuration**
- **Issue**: Extremely short TTL on A records
- **Details**:
  - A record TTL: **60 seconds** (typical is 300-3600)
  - This forces clients to re-query DNS every minute
  - Could indicate:
    - Active load balancing/rotation
    - Temporary/experimental service
    - DNS-based service discovery issue

### 3. **DNSSEC Misconfiguration** ⚠️
- **Issue**: DNSSEC appears enabled but incomplete
- **Details**:
  - Query with `+dnssec` shows `ad` flag (Authenticated Data)
  - **BUT**: No DNSKEY records exist
  - **AND**: RRSIG queries return REFUSED status
  - **Problem**: Domain claims DNSSEC authentication without proper cryptographic records
  - **Security Impact**: False sense of security

### 4. **Minimal SOA Serial Number**
- **Issue**: SOA serial is `1`
- **Details**:
  - Typical SOA serials use timestamps (e.g., 2025111701)
  - Serial of `1` suggests:
    - Brand new/test zone
    - Never updated zone file
    - Improper DNS management

### 5. **External-DNS Managed Service**
- **Finding**: TXT record shows automated DNS management
- **Details**:
  ```
  TXT: heritage=external-dns,external-dns/owner=default,
       external-dns/resource=service/challenges/nusecret5
  ```
  - Service is Kubernetes-managed (external-dns controller)
  - References `service/challenges/nusecret5`
  - This explains some configuration issues

## Primary "Issue"

**The main issue is the DNSSEC misconfiguration combined with service unavailability.**

The domain advertises DNSSEC support (ad flag) but lacks:
- DNSKEY records for public key distribution
- RRSIG signatures for record authentication  
- Proper DNSSEC chain of trust

This creates a **false security claim** that could be exploited.

## Potential CTF Flags

Based on findings:
- `FLAG{DNSSEC_MISCONFIGURED}`
- `FLAG{AD_FLAG_WITHOUT_KEYS}`
- `FLAG{SERVICE_UNAVAILABLE}`
- `FLAG{TTL_60_SECONDS}`
- `FLAG{SOA_SERIAL_ONE}`

## Technical Commands Used

```bash
# Basic DNS query
dig nusecret5-2163.ctf.nutanix.com

# DNSSEC investigation
dig @ns-856.awsdns-43.net nusecret5-2163.ctf.nutanix.com +dnssec
dig @ns-856.awsdns-43.net nusecret5-2163.ctf.nutanix.com DNSKEY
dig @ns-856.awsdns-43.net nusecret5-2163.ctf.nutanix.com RRSIG

# Service availability
curl -v -s --max-time 30 https://nusecret5-2163.ctf.nutanix.com

# Reverse DNS
dig -x 44.219.189.194
dig -x 52.205.182.30
```

## Conclusion

The endpoint has multiple DNS and service configuration issues, with the most significant being:
1. **DNSSEC misconfiguration** (security issue)
2. **Service unavailability** (operational issue)
3. **Unusual TTL settings** (configuration issue)
