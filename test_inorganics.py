#!/usr/bin/env python3
"""Simple test to read inorganics vector directly"""

import sys
sys.path.insert(0, 'python_implementation/src')

from complete_dwarf_reader import MemoryReader
import psutil

# Find DF
df_proc = None
for proc in psutil.process_iter(['pid', 'name']):
    if 'Dwarf Fortress' in proc.info['name']:
        df_proc = proc
        break

if not df_proc:
    print("ERROR: DF not running")
    sys.exit(1)

print(f"Found DF: PID {df_proc.pid}")

# Open process
mr = MemoryReader()
mr.open_process(df_proc.pid)

# Try to read inorganics_vector at hardcoded address
inorg_vec_addr = 0x142454b58  # From layout
pointer_size = 8

print(f"\nReading inorganics_vector at 0x{inorg_vec_addr:x}")

try:
    start = mr.read_pointer(inorg_vec_addr, pointer_size)
    end = mr.read_pointer(inorg_vec_addr + pointer_size, pointer_size)
    
    print(f"  start: 0x{start:x}")
    print(f"  end: 0x{end:x}")
    
    if start and end and end > start:
        count = (end - start) // pointer_size
        print(f"  count: {count}")
        
        if count > 0 and count < 1000:
            print(f"  Reading first 3 pointers...")
            for i in range(min(3, count)):
                ptr = mr.read_pointer(start + i * pointer_size, pointer_size)
                print(f"    [{i}]: 0x{ptr:x}")
                
                # Try to read material name from this inorganic
                if ptr:
                    # inorganic has materials_vector at offset 0x01a8
                    mat_vec_addr = ptr + 0x01a8
                    mat_start = mr.read_pointer(mat_vec_addr, pointer_size)
                    mat_end = mr.read_pointer(mat_vec_addr + pointer_size, pointer_size)
                    
                    if mat_start and mat_end and mat_end > mat_start:
                        mat_count = (mat_end - mat_start) // pointer_size
                        if mat_count > 0:
                            # Read first material
                            first_mat = mr.read_pointer(mat_start, pointer_size)
                            if first_mat:
                                # Read solid_name at offset 0x00b8
                                name = mr.read_string(first_mat + 0x00b8)
                                if name:
                                    print(f"      Material name: '{name}'")
    else:
        print("  ERROR: Invalid vector pointers")
        
except Exception as e:
    print(f"  ERROR: {e}")
    import traceback
    traceback.print_exc()

mr.close_handle()
print("\nDone")
