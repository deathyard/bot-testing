#!/usr/bin/env python3
"""
Parse MP4 file structure and check all atoms/boxes for hidden data
"""
import struct
import re

def parse_mp4_atoms(data, offset=0, depth=0):
    """Recursively parse MP4 atoms"""
    atoms = []
    i = offset
    
    while i < len(data) - 8:
        if i + 8 > len(data):
            break
        
        # Read atom size and type
        size = struct.unpack('>I', data[i:i+4])[0]
        atom_type = data[i+4:i+8]
        
        if size == 0:
            # Size 0 means extends to end of file
            size = len(data) - i
        elif size == 1:
            # Size 1 means extended size follows
            if i + 16 > len(data):
                break
            size = struct.unpack('>Q', data[i+8:i+16])[0]
            atom_start = i + 16
        else:
            atom_start = i + 8
        
        if size < 8 or i + size > len(data):
            i += 1
            continue
        
        atom_data = data[atom_start:i+size]
        atom_type_str = atom_type.decode('utf-8', errors='ignore')
        
        atoms.append({
            'type': atom_type_str,
            'offset': i,
            'size': size,
            'data': atom_data
        })
        
        # Check for text in this atom
        text = atom_data.decode('utf-8', errors='ignore')
        
        # Look for flag patterns
        flag_patterns = [
            r'flag\{[A-Za-z0-9_]{10,}\}',
            r'FLAG\{[A-Za-z0-9_]{10,}\}',
            r'picoCTF\{[A-Za-z0-9_]{10,}\}',
        ]
        
        for pattern in flag_patterns:
            matches = re.findall(pattern, text)
            if matches:
                print(f"\n*** FLAG FOUND in atom '{atom_type_str}' at offset {i}: {matches} ***")
        
        # Print interesting atoms
        if atom_type_str in ['udta', 'meta', 'ilst', 'data', 'free', 'skip']:
            readable_text = re.findall(rb'[ -~]{20,}', atom_data)
            for rt in readable_text[:3]:
                decoded = rt.decode('utf-8', errors='ignore')
                if len(decoded) > 10 and any(c.isalnum() for c in decoded):
                    print(f"Atom '{atom_type_str}' at {i}: {decoded[:100]}")
        
        # Recursively parse child atoms (if this is a container atom)
        if atom_type_str in ['moov', 'trak', 'mdia', 'minf', 'stbl', 'udta', 'meta']:
            if len(atom_data) > 8:
                child_atoms = parse_mp4_atoms(atom_data, 0, depth+1)
                atoms.extend(child_atoms)
        
        i += size
        if i >= len(data) - 8:
            break
    
    return atoms

def main():
    with open('nature.mp4', 'rb') as f:
        data = f.read()
    
    print("=== Parsing MP4 atoms ===")
    atoms = parse_mp4_atoms(data)
    
    print(f"\nFound {len(atoms)} atoms")
    
    # Summary of atom types
    atom_types = {}
    for atom in atoms:
        atom_type = atom['type']
        atom_types[atom_type] = atom_types.get(atom_type, 0) + 1
    
    print("\nAtom type summary:")
    for atom_type, count in sorted(atom_types.items()):
        print(f"  {atom_type}: {count}")

if __name__ == '__main__':
    main()
