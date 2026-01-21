#!/usr/bin/env python3
"""
DF Version Scanner - Detecta versão e checksum do Dwarf Fortress em execução
Para usar na criação de novos memory layouts para Dwarf Therapist
"""

import ctypes
import ctypes.wintypes
import struct
import psutil
import hashlib
import os
from pathlib import Path

# Windows API constants
PROCESS_VM_READ = 0x0010
PROCESS_QUERY_INFORMATION = 0x0400

def find_df_process():
    """Encontra o processo do Dwarf Fortress"""
    df_names = ['dwarf fortress', 'dwarfort', 'dwarffortress', 'dwarfort.exe', 'dwarffortress.exe']
    
    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            proc_name = proc.info['name'].lower()
            if any(df_name in proc_name for df_name in df_names):
                return {
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'exe': proc.info['exe']
                }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return None

def calculate_pe_checksum(exe_path):
    """Calcula o checksum do executável (mesmo método usado pelo DT)"""
    try:
        with open(exe_path, 'rb') as f:
            # Ler DOS header para encontrar o offset do PE header
            dos_header = f.read(64)
            if dos_header[:2] != b'MZ':
                return None, "Não é um executável PE válido"
            
            pe_offset = struct.unpack('<I', dos_header[60:64])[0]
            
            # Ler PE header
            f.seek(pe_offset)
            pe_sig = f.read(4)
            if pe_sig != b'PE\x00\x00':
                return None, "PE signature inválida"
            
            # Ler COFF header
            coff_header = f.read(20)
            machine = struct.unpack('<H', coff_header[0:2])[0]
            num_sections = struct.unpack('<H', coff_header[2:4])[0]
            timestamp = struct.unpack('<I', coff_header[4:8])[0]
            
            # O Dwarf Therapist usa o timestamp como checksum
            checksum = timestamp
            
            arch = "x64" if machine == 0x8664 else "x86" if machine == 0x14c else f"unknown(0x{machine:x})"
            
            return checksum, {
                'timestamp': timestamp,
                'architecture': arch,
                'num_sections': num_sections,
                'pe_offset': pe_offset
            }
    except Exception as e:
        return None, str(e)

def get_base_address(pid):
    """Obtém o endereço base do processo"""
    try:
        kernel32 = ctypes.windll.kernel32
        psapi = ctypes.windll.psapi
        
        process_handle = kernel32.OpenProcess(
            PROCESS_VM_READ | PROCESS_QUERY_INFORMATION, False, pid
        )
        
        if not process_handle:
            return None
        
        hModules = (ctypes.wintypes.HMODULE * 1024)()
        cb = ctypes.wintypes.DWORD()
        
        if psapi.EnumProcessModules(process_handle, hModules, ctypes.sizeof(hModules), ctypes.byref(cb)):
            base_addr = hModules[0]
            kernel32.CloseHandle(process_handle)
            return base_addr
        
        kernel32.CloseHandle(process_handle)
        return None
    except Exception as e:
        print(f"Erro ao obter endereço base: {e}")
        return None

def scan_for_known_patterns(pid, base_addr):
    """Escaneia padrões conhecidos na memória para ajudar a localizar offsets"""
    try:
        kernel32 = ctypes.windll.kernel32
        
        process_handle = kernel32.OpenProcess(
            PROCESS_VM_READ | PROCESS_QUERY_INFORMATION, False, pid
        )
        
        if not process_handle:
            return {}
        
        def read_memory(addr, size):
            buffer = ctypes.create_string_buffer(size)
            bytes_read = ctypes.c_size_t()
            if kernel32.ReadProcessMemory(process_handle, addr, buffer, size, ctypes.byref(bytes_read)):
                return buffer.raw[:bytes_read.value]
            return b''
        
        results = {}
        
        # Tentar ler algumas regiões conhecidas
        # Estas são heurísticas que podem ajudar na descoberta
        
        kernel32.CloseHandle(process_handle)
        return results
        
    except Exception as e:
        print(f"Erro ao escanear memória: {e}")
        return {}

def check_existing_layouts(checksum):
    """Verifica se já existe um layout para este checksum"""
    layouts_dir = Path(__file__).parent.parent.parent / "share" / "memory_layouts" / "windows"
    
    if not layouts_dir.exists():
        return None
    
    for ini_file in layouts_dir.glob("*.ini"):
        try:
            with open(ini_file, 'r') as f:
                content = f.read()
                if f"checksum=0x{checksum:x}" in content.lower() or f"checksum=0x{checksum:08x}" in content.lower():
                    return ini_file.name
        except:
            pass
    
    return None

def create_layout_template(checksum, info, output_path):
    """Cria um template de layout para a nova versão"""
    # Usar o layout mais recente como base
    layouts_dir = Path(__file__).parent.parent.parent / "share" / "memory_layouts" / "windows"
    
    # Encontrar o layout mais recente
    latest_layout = None
    for ini_file in sorted(layouts_dir.glob("*.ini"), reverse=True):
        if "steam" in ini_file.name.lower():
            latest_layout = ini_file
            break
    
    if not latest_layout:
        print("Não foi possível encontrar um layout base")
        return False
    
    print(f"\nUsando {latest_layout.name} como template base")
    
    with open(latest_layout, 'r') as f:
        content = f.read()
    
    # Substituir informações do cabeçalho
    import re
    content = re.sub(r'checksum=0x[0-9a-fA-F]+', f'checksum=0x{checksum:08x}', content)
    content = re.sub(r'version_name=.*', f'version_name=v0.53.10 win64 STEAM', content)
    content = re.sub(r'complete=true', 'complete=false  ; TEMPLATE - offsets precisam ser atualizados!', content)
    
    # Adicionar comentário de aviso
    header = f"""; ========================================
; TEMPLATE PARA DF v0.53.10
; Criado automaticamente - OFFSETS NÃO VERIFICADOS!
; Checksum: 0x{checksum:08x}
; Data: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}
; ========================================
; 
; Os offsets abaixo são copiados do layout anterior e
; PRECISAM SER ATUALIZADOS para a nova versão do DF.
;
; Use ferramentas como:
; - Ghidra ou IDA Pro para análise estática
; - export-dt-ini.lua (DFHack) para exportar offsets automaticamente
; - Comparar com df-structures do DFHack
;
; ========================================

"""
    content = header + content
    
    with open(output_path, 'w') as f:
        f.write(content)
    
    return True

def main():
    print("=" * 60)
    print("DWARF FORTRESS VERSION SCANNER")
    print("Para criação de Memory Layouts do Dwarf Therapist")
    print("=" * 60)
    print()
    
    # 1. Encontrar processo DF
    print("[1] Procurando processo do Dwarf Fortress...")
    df_proc = find_df_process()
    
    if not df_proc:
        print("    ERRO: Dwarf Fortress não está rodando!")
        print("    Por favor, inicie o jogo antes de executar este script.")
        return
    
    print(f"    Encontrado: {df_proc['name']} (PID: {df_proc['pid']})")
    print(f"    Executável: {df_proc['exe']}")
    print()
    
    # 2. Calcular checksum
    print("[2] Calculando checksum do executável...")
    checksum, info = calculate_pe_checksum(df_proc['exe'])
    
    if checksum is None:
        print(f"    ERRO: {info}")
        return
    
    print(f"    Checksum (timestamp): 0x{checksum:08x}")
    print(f"    Arquitetura: {info['architecture']}")
    print(f"    Seções PE: {info['num_sections']}")
    print()
    
    # 3. Verificar layouts existentes
    print("[3] Verificando layouts existentes...")
    existing = check_existing_layouts(checksum)
    
    if existing:
        print(f"    Layout encontrado: {existing}")
        print("    O Dwarf Therapist já suporta esta versão!")
        return
    else:
        print("    Nenhum layout encontrado para este checksum")
    print()
    
    # 4. Obter endereço base
    print("[4] Obtendo endereço base do processo...")
    base_addr = get_base_address(df_proc['pid'])
    
    if base_addr:
        print(f"    Endereço base: 0x{base_addr:016x}")
        
        # Calcular offset adjustment para x64
        if info['architecture'] == 'x64':
            adjustment = base_addr - 0x140000000
            print(f"    Ajuste para offsets: 0x{adjustment:x}")
    else:
        print("    Não foi possível obter o endereço base")
    print()
    
    # 5. Criar template
    print("[5] Criar template de layout?")
    output_path = Path(__file__).parent.parent.parent / "share" / "memory_layouts" / "windows" / f"v0.53.10-steam_win64.ini"
    
    response = input(f"    Criar template em {output_path.name}? (s/n): ").strip().lower()
    
    if response == 's':
        if create_layout_template(checksum, info, output_path):
            print(f"    Template criado: {output_path}")
            print()
            print("=" * 60)
            print("PRÓXIMOS PASSOS:")
            print("=" * 60)
            print("1. Os offsets no template são CÓPIAS da versão anterior")
            print("2. Use DFHack + export-dt-ini.lua para exportar offsets corretos")
            print("3. Ou compare com df-structures no GitHub do DFHack")
            print("4. Atualize os offsets manualmente no arquivo INI")
            print("5. Teste com o Dwarf Therapist")
        else:
            print("    Erro ao criar template")
    
    print()
    print("=" * 60)
    print("INFORMAÇÕES PARA DESCOBERTA DE OFFSETS:")
    print("=" * 60)
    print(f"Checksum para [info]: checksum=0x{checksum:08x}")
    print(f"Version name sugerido: version_name=v0.53.10 win64 STEAM")
    print()
    print("Recursos úteis:")
    print("- DFHack df-structures: github.com/DFHack/df-structures")
    print("- Script export-dt-ini.lua no DFHack")
    print("- Ghidra com symbols do DFHack")

if __name__ == "__main__":
    main()
