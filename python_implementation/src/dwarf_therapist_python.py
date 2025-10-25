#!/usr/bin/env python3
"""
Dwarf Therapist Python Edition
A Python implementation that reads Dwarf Fortress memory directly
"""

import ctypes
import ctypes.wintypes
import struct
import psutil
import configparser
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import IntEnum

# Windows API constants
PROCESS_VM_READ = 0x0010
PROCESS_VM_WRITE = 0x0020
PROCESS_VM_OPERATION = 0x0008
PROCESS_QUERY_INFORMATION = 0x0400

class DFStatus(IntEnum):
    DISCONNECTED = -1
    CONNECTED = 0
    LAYOUT_OK = 1
    GAME_LOADED = 2

@dataclass
class DwarfData:
    """Basic dwarf information structure"""
    id: int = 0
    name: str = ""
    custom_profession: str = ""
    profession: int = 0
    race: int = 0
    caste: int = 0
    sex: int = 0
    age: int = 0
    mood: int = 0
    happiness: int = 0
    address: int = 0
    
class MemoryReader:
    """Low-level memory reading utilities for Windows"""
    
    def __init__(self):
        self.kernel32 = ctypes.windll.kernel32
        self.process_handle = None
        
    def open_process(self, pid: int) -> bool:
        """Open process handle for memory operations"""
        access_rights = PROCESS_VM_READ | PROCESS_VM_WRITE | PROCESS_VM_OPERATION | PROCESS_QUERY_INFORMATION
        self.process_handle = self.kernel32.OpenProcess(access_rights, False, pid)
        return self.process_handle is not None
        
    def close_process(self):
        """Close process handle"""
        if self.process_handle:
            self.kernel32.CloseHandle(self.process_handle)
            self.process_handle = None
            
    def read_memory(self, address: int, size: int) -> bytes:
        """Read raw memory from process"""
        if not self.process_handle:
            return b''
            
        buffer = ctypes.create_string_buffer(size)
        bytes_read = ctypes.wintypes.SIZE_T()
        
        success = self.kernel32.ReadProcessMemory(
            self.process_handle,
            ctypes.c_void_p(address),
            buffer,
            size,
            ctypes.byref(bytes_read)
        )
        
        return buffer.raw if success else b''
        
    def read_int32(self, address: int) -> int:
        """Read 32-bit integer from memory"""
        data = self.read_memory(address, 4)
        return struct.unpack('<I', data)[0] if len(data) == 4 else 0
        
    def read_int64(self, address: int) -> int:
        """Read 64-bit integer from memory"""
        data = self.read_memory(address, 8)
        return struct.unpack('<Q', data)[0] if len(data) == 8 else 0
        
    def read_pointer(self, address: int, pointer_size: int = 8) -> int:
        """Read pointer value from memory"""
        if pointer_size == 8:
            return self.read_int64(address)
        else:
            return self.read_int32(address)
            
    def read_string(self, address: int, max_length: int = 256) -> str:
        """Read null-terminated string from memory"""
        data = self.read_memory(address, max_length)
        if not data:
            return ""
            
        null_pos = data.find(b'\x00')
        if null_pos >= 0:
            data = data[:null_pos]
            
        try:
            return data.decode('utf-8', errors='ignore')
        except:
            return ""
            
    def read_df_string(self, address: int, pointer_size: int = 8) -> str:
        """Read Dwarf Fortress string structure"""
        # DF uses std::string with small string optimization
        STRING_BUFFER_LENGTH = 16
        
        # Read the string structure
        len_offset = STRING_BUFFER_LENGTH
        cap_offset = STRING_BUFFER_LENGTH + pointer_size
        
        length = self.read_int64(address + len_offset) if pointer_size == 8 else self.read_int32(address + len_offset)
        capacity = self.read_int64(address + cap_offset) if pointer_size == 8 else self.read_int32(address + cap_offset)
        
        if capacity == 0 or length == 0:
            return ""
            
        if length > capacity or length > 1024:  # Sanity check
            return ""
            
        # Determine where the actual string data is
        if capacity >= STRING_BUFFER_LENGTH:
            # String is heap-allocated
            buffer_addr = self.read_pointer(address, pointer_size)
        else:
            # String uses internal buffer
            buffer_addr = address
            
        return self.read_string(buffer_addr, min(length, 1024))

class MemoryLayout:
    """Handles memory layout configuration for specific DF versions"""
    
    def __init__(self, layout_file: Path):
        self.config = configparser.ConfigParser()
        self.config.read(layout_file)
        self.offsets = {}
        self.addresses = {}
        self.info = {}
        
        self._load_sections()
        
    def _load_sections(self):
        """Load all relevant sections from memory layout"""
        if 'info' in self.config:
            self.info = dict(self.config['info'])
            
        if 'addresses' in self.config:
            self.addresses = {k: int(v, 16) for k, v in self.config['addresses'].items()}
            
        if 'dwarf_offsets' in self.config:
            self.offsets['dwarf'] = {k: int(v, 16) for k, v in self.config['dwarf_offsets'].items()}
            
        # Load other offset sections as needed
        for section in ['race_offsets', 'caste_offsets', 'hist_figure_offsets']:
            if section in self.config:
                key = section.replace('_offsets', '')
                self.offsets[key] = {k: int(v, 16) for k, v in self.config[section].items()}
                
    def get_address(self, key: str) -> int:
        """Get global address for a key"""
        return self.addresses.get(key, 0)
        
    def get_offset(self, section: str, key: str) -> int:
        """Get offset for a specific section and key"""
        return self.offsets.get(section, {}).get(key, 0)
        
    def get_checksum(self) -> str:
        """Get the expected checksum for this layout"""
        return self.info.get('checksum', '')

class DFInstance:
    """Main class for interacting with Dwarf Fortress memory"""
    
    def __init__(self):
        self.memory_reader = MemoryReader()
        self.layout: Optional[MemoryLayout] = None
        self.pid = 0
        self.base_addr = 0
        self.pointer_size = 8  # Assume 64-bit by default
        self.status = DFStatus.DISCONNECTED
        self.dwarves: List[DwarfData] = []
        
    def find_df_process(self) -> bool:
        """Find running Dwarf Fortress process"""
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'].lower() == 'dwarf fortress.exe':
                    self.pid = proc.info['pid']
                    print(f"Found Dwarf Fortress process: PID {self.pid}")
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return False
        
    def connect(self) -> bool:
        """Connect to Dwarf Fortress process"""
        if not self.find_df_process():
            print("Could not find Dwarf Fortress process")
            return False
            
        if not self.memory_reader.open_process(self.pid):
            print(f"Could not open process {self.pid}")
            return False
            
        # Read PE header to get base address
        if not self._read_pe_header():
            print("Could not read PE header")
            return False
            
        self.status = DFStatus.CONNECTED
        print(f"Connected to DF process. Base address: 0x{self.base_addr:x}")
        return True
        
    def _read_pe_header(self) -> bool:
        """Read PE header to determine base address and architecture"""
        try:
            proc = psutil.Process(self.pid)
            # Get the main module (executable)
            main_module = proc.memory_maps()[0]
            base_addr = int(main_module.addr.split('-')[0], 16)
            
            # Read DOS header
            dos_header = self.memory_reader.read_memory(base_addr, 64)
            if len(dos_header) < 64 or dos_header[:2] != b'MZ':
                return False
                
            # Get PE header offset
            pe_offset = struct.unpack('<I', dos_header[60:64])[0]
            
            # Read PE header
            pe_header = self.memory_reader.read_memory(base_addr + pe_offset, 24)
            if len(pe_header) < 24 or pe_header[:4] != b'PE\x00\x00':
                return False
                
            # Get machine type to determine architecture
            machine_type = struct.unpack('<H', pe_header[4:6])[0]
            
            if machine_type == 0x8664:  # AMD64
                self.pointer_size = 8
                self.base_addr = base_addr - 0x140000000
            elif machine_type == 0x14c:  # i386
                self.pointer_size = 4
                self.base_addr = base_addr - 0x400000
            else:
                print(f"Unknown machine type: 0x{machine_type:x}")
                return False
                
            return True
        except Exception as e:
            print(f"Error reading PE header: {e}")
            return False
            
    def load_memory_layout(self, layout_file: Path = None) -> bool:
        """Load memory layout for current DF version"""
        if layout_file is None:
            # Try to find appropriate layout file
            layouts_dir = Path(__file__).parent / "share" / "memory_layouts" / "windows"
            if not layouts_dir.exists():
                print(f"Memory layouts directory not found: {layouts_dir}")
                return False
                
            # For now, use a recent layout file
            layout_files = list(layouts_dir.glob("*.ini"))
            if not layout_files:
                print("No memory layout files found")
                return False
                
            # Use the most recent layout (this is simplified - in reality we'd match checksum)
            layout_file = sorted(layout_files)[-1]
            print(f"Using memory layout: {layout_file.name}")
            
        try:
            self.layout = MemoryLayout(layout_file)
            self.status = DFStatus.LAYOUT_OK
            return True
        except Exception as e:
            print(f"Error loading memory layout: {e}")
            return False
            
    def read_dwarves(self) -> List[DwarfData]:
        """Read all dwarves from memory"""
        if self.status < DFStatus.LAYOUT_OK:
            print("Not connected or layout not loaded")
            return []
            
        try:
            # Get creature vector address
            creature_vector_addr = self.layout.get_address('creature_vector')
            if not creature_vector_addr:
                print("Could not find creature_vector address")
                return []
                
            # Adjust for base address
            creature_vector_addr += self.base_addr
            
            # Read vector (start, end pointers)
            start_ptr = self.memory_reader.read_pointer(creature_vector_addr, self.pointer_size)
            end_ptr = self.memory_reader.read_pointer(creature_vector_addr + self.pointer_size, self.pointer_size)
            
            if start_ptr == 0 or end_ptr == 0 or start_ptr >= end_ptr:
                print("Invalid creature vector pointers")
                return []
                
            # Calculate number of creatures
            creature_count = (end_ptr - start_ptr) // self.pointer_size
            print(f"Found {creature_count} creatures")
            
            dwarves = []
            for i in range(min(creature_count, 1000)):  # Limit to prevent runaway
                creature_ptr_addr = start_ptr + (i * self.pointer_size)
                creature_addr = self.memory_reader.read_pointer(creature_ptr_addr, self.pointer_size)
                
                if creature_addr == 0:
                    continue
                    
                dwarf = self._read_dwarf(creature_addr)
                if dwarf and dwarf.name:  # Only add if we got valid data
                    dwarves.append(dwarf)
                    
            self.dwarves = dwarves
            self.status = DFStatus.GAME_LOADED
            print(f"Successfully read {len(dwarves)} dwarves")
            return dwarves
            
        except Exception as e:
            print(f"Error reading dwarves: {e}")
            return []
            
    def _read_dwarf(self, address: int) -> Optional[DwarfData]:
        """Read single dwarf data from memory"""
        try:
            offsets = self.layout.offsets.get('dwarf', {})
            if not offsets:
                return None
                
            dwarf = DwarfData(address=address)
            
            # Read basic fields
            dwarf.id = self.memory_reader.read_int32(address + offsets.get('id', 0))
            dwarf.race = self.memory_reader.read_int32(address + offsets.get('race', 0))
            dwarf.caste = self.memory_reader.read_int32(address + offsets.get('caste', 0))
            dwarf.sex = self.memory_reader.read_int32(address + offsets.get('sex', 0))
            dwarf.profession = self.memory_reader.read_int32(address + offsets.get('profession', 0))
            dwarf.mood = self.memory_reader.read_int32(address + offsets.get('mood', 0))
            
            # Read name (DF string structure)
            name_offset = offsets.get('name', 0)
            if name_offset:
                dwarf.name = self.memory_reader.read_df_string(address + name_offset, self.pointer_size)
                
            # Read custom profession
            custom_prof_offset = offsets.get('custom_profession', 0)
            if custom_prof_offset:
                dwarf.custom_profession = self.memory_reader.read_df_string(address + custom_prof_offset, self.pointer_size)
                
            # Calculate age from birth year
            birth_year_offset = offsets.get('birth_year', 0)
            if birth_year_offset:
                birth_year = self.memory_reader.read_int32(address + birth_year_offset)
                current_year_addr = self.layout.get_address('current_year')
                if current_year_addr:
                    current_year = self.memory_reader.read_int32(current_year_addr + self.base_addr)
                    dwarf.age = current_year - birth_year
                    
            return dwarf
            
        except Exception as e:
            print(f"Error reading dwarf at 0x{address:x}: {e}")
            return None
            
    def disconnect(self):
        """Disconnect from process"""
        self.memory_reader.close_process()
        self.status = DFStatus.DISCONNECTED
        
    def __del__(self):
        self.disconnect()

def main():
    """Example usage of the Dwarf Therapist Python edition"""
    df = DFInstance()
    
    print("Dwarf Therapist Python Edition")
    print("=" * 40)
    
    # Connect to DF
    if not df.connect():
        print("Failed to connect to Dwarf Fortress")
        return
        
    # Load memory layout
    if not df.load_memory_layout():
        print("Failed to load memory layout")
        return
        
    # Read dwarves
    dwarves = df.read_dwarves()
    
    if not dwarves:
        print("No dwarves found or failed to read data")
        return
        
    # Display dwarf information
    print(f"\nFound {len(dwarves)} dwarves:")
    print("-" * 80)
    print(f"{'ID':<6} {'Name':<20} {'Profession':<15} {'Age':<4} {'Mood':<4}")
    print("-" * 80)
    
    for dwarf in dwarves[:20]:  # Show first 20
        profession = dwarf.custom_profession if dwarf.custom_profession else str(dwarf.profession)
        print(f"{dwarf.id:<6} {dwarf.name:<20} {profession:<15} {dwarf.age:<4} {dwarf.mood:<4}")
        
    print(f"\n(Showing first 20 of {len(dwarves)} dwarves)")

if __name__ == "__main__":
    main()