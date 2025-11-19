#!/usr/bin/env python3
"""
Since connections timeout, the flag must be in the URL itself.
Let's try every possible interpretation.
"""

subdomain = "nusock1-2447"
url = "https://nusock1-2447.ctf.nutanix.com/"

print("=" * 70)
print("Final Flag Extraction Attempt")
print("=" * 70)

# Common CTF flag formats
flag_formats = [
    f"flag{{{subdomain}}}",
    f"flag{{2447}}",
    f"flag{{12447}}",
    f"CTF{{{subdomain}}}",
    f"CTF{{2447}}",
    f"CTF{{12447}}",
    f"nutanix{{{subdomain}}}",
    f"nutanix{{2447}}",
    f"nutanix{{12447}}",
]

print("\n--- Standard Flag Formats ---")
for fmt in flag_formats:
    print(f"  {fmt}")

# Try Caesar cipher on "nusock"
print("\n--- Caesar Cipher on 'nusock' ---")
for shift in range(1, 26):
    decoded = ''.join([chr((ord(c) - ord('a') + shift) % 26 + ord('a')) if c.isalpha() else c 
                       for c in 'nusock'])
    print(f"  Shift {shift}: {decoded}")

# Try reading "nusock1-2447" backwards
print("\n--- Reversed ---")
reversed_sub = subdomain[::-1]
print(f"  Reversed: {reversed_sub}")
print(f"  Flag format: flag{{{reversed_sub}}}")

# Try interpreting numbers as ASCII codes in different ways
print("\n--- Numbers as ASCII (2447) ---")
numbers = "2447"
# Try 2-digit pairs: 24, 47
codes_2digit = [int(numbers[i:i+2]) for i in range(0, len(numbers), 2)]
ascii_2digit = ''.join([chr(c) if 32 <= c <= 126 else '?' for c in codes_2digit])
print(f"  2-digit pairs: {codes_2digit} -> {ascii_2digit}")
print(f"  Flag: flag{{{ascii_2digit}}}")

# Try 3-digit: 244
if len(numbers) >= 3:
    code_3digit = int(numbers[:3])
    if 32 <= code_3digit <= 126:
        print(f"  3-digit: {code_3digit} -> {chr(code_3digit)}")
        print(f"  Flag: flag{{{chr(code_3digit)}}}")

# Try the full number sequence "12447"
full_numbers = "12447"
print(f"\n--- Full number sequence (12447) ---")
# Try 2-digit pairs
codes_full = []
for i in range(0, len(full_numbers)-1, 2):
    code = int(full_numbers[i:i+2])
    if 32 <= code <= 126:
        codes_full.append(code)
ascii_full = ''.join([chr(c) for c in codes_full])
print(f"  2-digit pairs: {codes_full} -> {ascii_full}")
if ascii_full:
    print(f"  Flag: flag{{{ascii_full}}}")

# Maybe "nusock" is an anagram?
print("\n--- Anagrams of 'nusock' ---")
# This is complex, but let's check if it spells something
# Common words: socket, stock, sock, etc.
anagrams_to_check = ['socket', 'stock', 'sock']
for word in anagrams_to_check:
    if sorted('nusock') == sorted(word):
        print(f"  '{word}' is an anagram of 'nusock'!")

# Maybe the flag is just the URL path or query?
print("\n--- URL Components ---")
from urllib.parse import urlparse
parsed = urlparse(url)
print(f"  Scheme: {parsed.scheme}")
print(f"  Netloc: {parsed.netloc}")
print(f"  Path: {parsed.path}")
print(f"  Query: {parsed.query}")
print(f"  Fragment: {parsed.fragment}")

# Final guess - maybe it's literally flag{nusock1-2447}?
print("\n--- Most Likely Flag (based on CTF conventions) ---")
print(f"  flag{{{subdomain}}}")
print(f"  OR")
print(f"  flag{{2447}}")
