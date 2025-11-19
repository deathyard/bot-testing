#!/usr/bin/env python3
import sys
import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3NoHeaderError
from pydub import AudioSegment
import numpy as np

def check_metadata(file_path):
    """Check for hidden data in metadata"""
    print("=" * 60)
    print("1. Checking Metadata...")
    print("=" * 60)
    try:
        audio = MP3(file_path)
        print(f"Length: {audio.info.length} seconds")
        print(f"Bitrate: {audio.info.bitrate} bps")
        
        if audio.tags:
            print("\nTags found:")
            for key, value in audio.tags.items():
                print(f"  {key}: {value}")
        else:
            print("No ID3 tags found")
    except Exception as e:
        print(f"Error reading metadata: {e}")

def analyze_raw_bytes(file_path):
    """Analyze raw file bytes for hidden data"""
    print("\n" + "=" * 60)
    print("2. Analyzing Raw File Bytes...")
    print("=" * 60)
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        
        print(f"File size: {len(data)} bytes")
        
        # Check for common flag patterns
        flag_patterns = [b'flag{', b'FLAG{', b'ctf{', b'CTF{', b'flag:', b'FLAG:']
        for pattern in flag_patterns:
            if pattern in data:
                idx = data.find(pattern)
                print(f"\nFound pattern '{pattern.decode()}' at offset {idx}")
                # Extract potential flag
                end_idx = data.find(b'}', idx)
                if end_idx != -1:
                    potential_flag = data[idx:end_idx+1]
                    print(f"Potential flag: {potential_flag.decode('utf-8', errors='ignore')}")
        
        # Check for text strings
        print("\nSearching for readable strings...")
        strings = []
        current_string = b''
        for byte in data:
            if 32 <= byte <= 126:  # Printable ASCII
                current_string += bytes([byte])
            else:
                if len(current_string) >= 4:
                    strings.append(current_string)
                current_string = b''
        
        # Show interesting strings
        interesting = [s for s in strings if any(b in s.lower() for b in [b'flag', b'ctf', b'hidden', b'secret'])]
        if interesting:
            print("Interesting strings found:")
            for s in interesting[:10]:
                print(f"  {s.decode('utf-8', errors='ignore')}")
        
        # Check file header/footer for appended data
        print("\nChecking for appended data...")
        # MP3 files typically end with certain patterns
        # Check last 1000 bytes for non-MP3 data
        if len(data) > 1000:
            tail = data[-1000:]
            # Look for text patterns in tail
            text_in_tail = b''.join([bytes([b]) if 32 <= b <= 126 else b' ' for b in tail])
            if b'flag' in text_in_tail.lower() or b'ctf' in text_in_tail.lower():
                print("Found potential flag in file tail!")
                print(text_in_tail.decode('utf-8', errors='ignore'))
        
    except Exception as e:
        print(f"Error analyzing raw bytes: {e}")

def extract_lsb(file_path):
    """Try LSB steganography extraction"""
    print("\n" + "=" * 60)
    print("3. Attempting LSB Extraction...")
    print("=" * 60)
    try:
        # Convert MP3 to WAV for easier processing
        audio = AudioSegment.from_mp3(file_path)
        samples = np.array(audio.get_array_of_samples())
        
        if len(audio.channels) == 2:
            samples = samples.reshape((-1, 2))
            samples = samples[:, 0]  # Use left channel
        
        print(f"Number of samples: {len(samples)}")
        
        # Extract LSBs
        lsbs = samples & 1
        lsbs_str = ''.join([str(b) for b in lsbs[:10000]])  # First 10000 bits
        
        # Try to find flag pattern in LSBs
        # Convert bits to bytes
        if len(lsbs) >= 8:
            bytes_data = []
            for i in range(0, min(len(lsbs), 10000), 8):
                byte_val = 0
                for j in range(8):
                    if i + j < len(lsbs):
                        byte_val |= (lsbs[i + j] << j)
                bytes_data.append(byte_val)
            
            # Try to decode as text
            text = ''.join([chr(b) if 32 <= b <= 126 else '.' for b in bytes_data])
            if 'flag' in text.lower() or 'ctf' in text.lower():
                print("Found potential flag in LSBs!")
                # Find flag pattern
                idx = text.lower().find('flag')
                if idx != -1:
                    end_idx = text.find('}', idx)
                    if end_idx != -1:
                        print(f"Flag: {text[idx:end_idx+1]}")
                    else:
                        print(f"Potential flag start: {text[idx:idx+50]}")
            else:
                print("No obvious flag pattern found in LSBs")
                print(f"First 200 characters: {text[:200]}")
        
    except Exception as e:
        print(f"Error in LSB extraction: {e}")
        import traceback
        traceback.print_exc()

def check_spectrogram(file_path):
    """Generate spectrogram to check for visual patterns"""
    print("\n" + "=" * 60)
    print("4. Checking Spectrogram...")
    print("=" * 60)
    try:
        from scipy import signal
        from scipy.io import wavfile
        
        # Convert to WAV first
        audio = AudioSegment.from_mp3(file_path)
        wav_path = "/tmp/temp_audio.wav"
        audio.export(wav_path, format="wav")
        
        sample_rate, samples = wavfile.read(wav_path)
        if len(samples.shape) > 1:
            samples = samples[:, 0]  # Use first channel
        
        # Generate spectrogram
        frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate)
        
        print(f"Sample rate: {sample_rate} Hz")
        print(f"Spectrogram shape: {spectrogram.shape}")
        print("(Visual inspection of spectrogram image would be needed)")
        
        os.remove(wav_path)
        
    except Exception as e:
        print(f"Error generating spectrogram: {e}")

def main():
    file_path = "steg_audio.mp3"
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found!")
        return
    
    check_metadata(file_path)
    analyze_raw_bytes(file_path)
    extract_lsb(file_path)
    check_spectrogram(file_path)
    
    print("\n" + "=" * 60)
    print("Analysis Complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
