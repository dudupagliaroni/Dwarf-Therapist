#!/usr/bin/env python3
"""
Debug script to test material resolution directly
"""

import sys
sys.path.insert(0, 'python_implementation/src')

from complete_dwarf_reader import CompleteDFInstance
import logging

# Enable detailed logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

print("=" * 80)
print("MATERIAL RESOLUTION DEBUG")
print("=" * 80)

# Initialize and connect
df = CompleteDFInstance()

# Find DF process
import psutil
df_proc = None
for proc in psutil.process_iter(['pid', 'name']):
    if 'Dwarf Fortress' in proc.info['name']:
        df_proc = proc
        break

if not df_proc:
    print("ERROR: Dwarf Fortress not running")
    sys.exit(1)

print(f"\nConnecting to DF (PID {df_proc.pid})...")
df.memory_reader.open_process(df_proc.pid)
df.pid = df_proc.pid

# Get base address
df.base_addr = df.memory_reader.get_module_base_address(df.pid, "Dwarf Fortress.exe")
print(f"Base address: 0x{df.base_addr:x}")

# Load layout
from pathlib import Path
layout_file = Path("share/memory_layouts/windows/v0.52.05-steam_win64.ini")
from complete_dwarf_reader import MemoryLayout
df.layout = MemoryLayout(layout_file)

# Initialize MaterialResolver
from complete_dwarf_reader import MaterialResolver
df.material_resolver = MaterialResolver(
    df.memory_reader,
    df.layout,
    df.base_addr,
    df.pointer_size
)

print("\n" + "=" * 80)
print("TESTING VECTOR READING")
print("=" * 80)

# Test reading inorganics_vector
inorg_addr = df.layout.get_address('inorganics_vector')
print(f"\ninorganics_vector address from layout: 0x{inorg_addr:x}")

if inorg_addr:
    print(f"Reading vector at 0x{inorg_addr:x}...")
    inorganics = df.material_resolver._read_vector(inorg_addr)
    print(f"Found {len(inorganics)} inorganic materials")
    if inorganics:
        print(f"First 5 pointers: {[hex(p) for p in inorganics[:5]]}")

# Test reading plants_vector
plants_addr = df.layout.get_address('plants_vector')
print(f"\nplants_vector address from layout: 0x{plants_addr:x}")

if plants_addr:
    print(f"Reading vector at 0x{plants_addr:x}...")
    plants = df.material_resolver._read_vector(plants_addr)
    print(f"Found {len(plants)} plants")
    if plants:
        print(f"First 5 pointers: {[hex(p) for p in plants[:5]]}")

# Test reading races_vector
races_addr = df.layout.get_address('races_vector')
print(f"\nraces_vector address from layout: 0x{races_addr:x}")

if races_addr:
    print(f"Reading vector at 0x{races_addr:x}...")
    races = df.material_resolver._read_vector(races_addr)
    print(f"Found {len(races)} races")
    if races:
        print(f"First 5 pointers: {[hex(p) for p in races[:5]]}")

print("\n" + "=" * 80)
print("TESTING MATERIAL RESOLUTION")
print("=" * 80)

# Test cases from actual equipment
test_cases = [
    (0, 26, -1, "inorganic_26 (should be IRON or similar)"),
    (38, 308, -1, "creature_308_mat_19 (creature material)"),
    (422, 174, -1, "plant_174_mat_3 (plant material)"),
]

for mat_type, mat_index, item_type, description in test_cases:
    print(f"\nTest: {description}")
    print(f"  mat_type={mat_type}, mat_index={mat_index}, item_type={item_type}")
    result = df.material_resolver.resolve_material_name(mat_type, mat_index, item_type)
    print(f"  Result: '{result}'")

df.memory_reader.close_handle()
print("\n" + "=" * 80)
print("DEBUG COMPLETE")
print("=" * 80)
