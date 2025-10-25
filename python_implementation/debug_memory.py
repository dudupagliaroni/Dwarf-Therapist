#!/usr/bin/env python3
"""
Debug script para verificar leitura de memória em um dwarf específico
"""

import os
import sys
import psutil
import ctypes
import struct

# Adicionar o diretório src ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

from complete_dwarf_reader import MemoryReader, MemoryLayout

def debug_dwarf_memory():
    """Debug da leitura de memória de um dwarf específico"""
    
    # Encontrar processo do Dwarf Fortress
    df_processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if 'dwarf' in proc.info['name'].lower() and 'fortress' in proc.info['name'].lower():
                df_processes.append(proc.info)
        except:
            continue
            
    if not df_processes:
        print("Dwarf Fortress não encontrado!")
        return
        
    df_pid = df_processes[0]['pid']
    print(f"Dwarf Fortress encontrado: PID {df_pid}")
    
    # Carregar layout
    layout_path = os.path.join(current_dir, '..', 'share', 'memory_layouts', 'windows', 'v0.52.05-steam_win64.ini')
    from pathlib import Path
    layout = MemoryLayout(Path(layout_path))
    
    if not layout.offsets:
        print("Falha ao carregar layout!")
        return
        
    # Criar memory reader
    memory_reader = MemoryReader()
    if not memory_reader.open_process(df_pid):
        print("Falha ao abrir processo!")
        return
        
    try:
        # Obter endereço do vetor de criaturas
        creatures_vector_addr = layout.get_address('creature_vector')
        if not creatures_vector_addr:
            print("Endereço do vetor de criaturas não encontrado!")
            return
            
        print(f"Endereço do vetor de criaturas: 0x{creatures_vector_addr:x}")
        
        # Ler o vetor
        start_ptr = memory_reader.read_pointer(creatures_vector_addr)
        end_ptr = memory_reader.read_pointer(creatures_vector_addr + 8)
        
        print(f"Start pointer: 0x{start_ptr:x} ({start_ptr})")
        print(f"End pointer: 0x{end_ptr:x} ({end_ptr})")
        
        if not start_ptr or not end_ptr:
            print("Falha ao ler ponteiros do vetor!")
            # Vamos tentar ler os dados raw para debug
            raw_data = memory_reader.read_memory(creatures_vector_addr, 16)
            print(f"Raw data at vector address: {raw_data.hex()}")
            return
            
        creature_count = (end_ptr - start_ptr) // 8
        print(f"Criaturas encontradas: {creature_count}")
        
        if creature_count == 0:
            print("Nenhuma criatura encontrada!")
            return
            
        # Pegar o primeiro dwarf
        first_creature_ptr_addr = start_ptr
        first_creature_addr = memory_reader.read_pointer(first_creature_ptr_addr)
        
        if not first_creature_addr:
            print("Falha ao ler endereço da primeira criatura!")
            return
            
        print(f"Endereço da primeira criatura: 0x{first_creature_addr:x}")
        
        # Debug dos offsets
        dwarf_offsets = layout.offsets.get('dwarf', {})
        
        print("\n=== DEBUG DOS VALORES ===")
        print(f"Endereço base do dwarf: 0x{first_creature_addr:x}")
        
        # Testar diferentes offsets
        test_offsets = {
            'profession': dwarf_offsets.get('profession', 0),
            'sex': dwarf_offsets.get('sex', 0), 
            'race': dwarf_offsets.get('race', 0),
            'id': dwarf_offsets.get('id', 0),
            'flags1': dwarf_offsets.get('flags1', 0),
            'caste': dwarf_offsets.get('caste', 0)
        }
        
        for field, offset in test_offsets.items():
            if offset:
                addr = first_creature_addr + offset
                
                # Ler como diferentes tipos
                raw_data = memory_reader.read_memory(addr, 8)
                if len(raw_data) >= 4:
                    int8_val = struct.unpack('<b', raw_data[:1])[0] if len(raw_data) >= 1 else 0
                    uint8_val = struct.unpack('<B', raw_data[:1])[0] if len(raw_data) >= 1 else 0
                    int16_val = struct.unpack('<h', raw_data[:2])[0] if len(raw_data) >= 2 else 0
                    uint16_val = struct.unpack('<H', raw_data[:2])[0] if len(raw_data) >= 2 else 0
                    int32_val = struct.unpack('<i', raw_data[:4])[0] if len(raw_data) >= 4 else 0
                    uint32_val = struct.unpack('<I', raw_data[:4])[0] if len(raw_data) >= 4 else 0
                    
                    print(f"\n{field} (offset 0x{offset:x}, addr 0x{addr:x}):")
                    print(f"  Raw bytes: {raw_data[:4].hex()}")
                    print(f"  int8:  {int8_val}")
                    print(f"  uint8: {uint8_val}")
                    print(f"  int16: {int16_val}")
                    print(f"  uint16: {uint16_val}")
                    print(f"  int32: {int32_val}")
                    print(f"  uint32: {uint32_val}")
                    
        # Verificar se é realmente um dwarf (race deveria ser dwarf_race_id)
        dwarf_race_id = layout.get_address('dwarf_race_id')
        if dwarf_race_id:
            race_offset = dwarf_offsets.get('race', 0)
            if race_offset:
                race_addr = first_creature_addr + race_offset
                actual_race = memory_reader.read_int32(race_addr)
                print(f"\nRace da criatura: {actual_race}")
                print(f"Dwarf race ID esperado: {dwarf_race_id}")
                print(f"É um dwarf: {'SIM' if actual_race == dwarf_race_id else 'NÃO'}")
                
    finally:
        memory_reader.close_process()

if __name__ == '__main__':
    debug_dwarf_memory()