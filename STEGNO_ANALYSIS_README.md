# CTF Steganography Analysis Guide

## File Location
Your image file is at: `/Users/saumyadoogar/Downloads/stegno_1.jpg`

## Quick Start

### Option 1: Copy file to workspace (Recommended)
```bash
cp /Users/saumyadoogar/Downloads/stegno_1.jpg /workspace/stegno_1.jpg
```

Then run:
```bash
cd /workspace
python3 analyze_stegno.py stegno_1.jpg
# OR
./quick_steg_check.sh stegno_1.jpg
```

### Option 2: Run analysis directly on your machine
```bash
cd /workspace
python3 analyze_stegno.py /Users/saumyadoogar/Downloads/stegno_1.jpg
# OR
./quick_steg_check.sh /Users/saumyadoogar/Downloads/stegno_1.jpg
```

## Analysis Tools Created

1. **analyze_stegno.py** - Comprehensive Python script that:
   - Extracts metadata (EXIF data)
   - Extracts strings from the image
   - Performs LSB (Least Significant Bit) steganography extraction
   - Searches for CTF flag patterns
   - Decodes base64 data

2. **quick_steg_check.sh** - Quick bash script using basic tools:
   - Uses `strings` command
   - Checks file type
   - Looks for flag patterns
   - Shows hex dump

## What to Look For

The scripts will search for flags in these formats:
- `FLAG{...}`
- `flag{...}`
- `CTF{...}`
- `ctf{...}`
- `nutanix{...}`
- `NUTANIX{...}`

## Additional Tools (if needed)

If the basic analysis doesn't find the flag, try:
- `steghide` - For steghide-encrypted data
- `zsteg` - For PNG/BMP steganography
- `binwalk` - For embedded files
- `exiftool` - For detailed metadata
