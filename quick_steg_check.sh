#!/bin/bash
# Quick steganography check using basic tools

IMAGE_FILE="$1"

if [ -z "$IMAGE_FILE" ]; then
    echo "Usage: $0 <image_file>"
    exit 1
fi

if [ ! -f "$IMAGE_FILE" ]; then
    echo "Error: File not found: $IMAGE_FILE"
    exit 1
fi

echo "=== Basic Steganography Analysis ==="
echo "File: $IMAGE_FILE"
echo "Size: $(stat -f%z "$IMAGE_FILE" 2>/dev/null || stat -c%s "$IMAGE_FILE" 2>/dev/null) bytes"
echo ""

echo "=== File Type ==="
file "$IMAGE_FILE"
echo ""

echo "=== Strings Extraction ==="
strings "$IMAGE_FILE" | grep -iE "(FLAG|flag|CTF|ctf|nutanix|NUTANIX)" | head -20
echo ""

echo "=== All Strings (longer than 10 chars) ==="
strings -n 10 "$IMAGE_FILE" | head -50
echo ""

echo "=== Hex Dump (first 200 bytes) ==="
hexdump -C "$IMAGE_FILE" | head -10
echo ""

echo "=== Checking for embedded files ==="
# Check for common file signatures
grep -ao "PNG\|JFIF\|GIF\|PDF" "$IMAGE_FILE" | head -5 || echo "No embedded file signatures found"
echo ""

echo "=== Base64-like patterns ==="
strings "$IMAGE_FILE" | grep -E "^[A-Za-z0-9+/]{20,}={0,2}$" | head -10
