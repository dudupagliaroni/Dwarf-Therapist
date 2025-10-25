#!/usr/bin/env python3
"""
Dwarf Therapist Python Edition - Versão com Logs Detalhados
Inclui logs verbosos para debugging e correções de erro
"""

import ctypes
import ctypes.wintypes
import struct
import psutil
import configparser
import os
import sys
import json
import traceback
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import IntEnum
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('dwarf_therapist.log')
    ]
)
logger = logging.getLogger(__name__)

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
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return asdict(self)
    
class MemoryReader:
    """Low-level memory reading utilities for Windows"""
    
    def __init__(self):
        self.kernel32 = ctypes.windll.kernel32
        self.process_handle = None
        logger.info("MemoryReader inicializado")
        
    def open_process(self, pid: int) -> bool:
        """Open process handle for memory operations"""
        logger.info(f"Tentando abrir processo PID {pid}")
        access_rights = PROCESS_VM_READ | PROCESS_VM_WRITE | PROCESS_VM_OPERATION | PROCESS_QUERY_INFORMATION
        self.process_handle = self.kernel32.OpenProcess(access_rights, False, pid)
        
        if self.process_handle:
            logger.info(f"Processo {pid} aberto com sucesso. Handle: {self.process_handle}")
            return True
        else:
            error = ctypes.windll.kernel32.GetLastError()
            logger.error(f"Falha ao abrir processo {pid}. Erro: {error}")
            return False
        
    def close_process(self):
        """Close process handle"""
        if self.process_handle:
            logger.info("Fechando handle do processo")
            self.kernel32.CloseHandle(self.process_handle)
            self.process_handle = None
            
    def read_memory(self, address: int, size: int) -> bytes:
        """Read raw memory from process"""
        if not self.process_handle:
            logger.error("Tentativa de leitura sem handle do processo")
            return b''
            
        buffer = ctypes.create_string_buffer(size)
        bytes_read = ctypes.c_size_t()
        
        success = self.kernel32.ReadProcessMemory(
            self.process_handle,
            ctypes.c_void_p(address),
            buffer,
            size,
            ctypes.byref(bytes_read)
        )
        
        if success:
            logger.debug(f"Lidos {bytes_read.value} bytes do endereço 0x{address:x}")
            return buffer.raw
        else:
            error = ctypes.windll.kernel32.GetLastError()
            logger.warning(f"Falha ao ler memória 0x{address:x}, tamanho {size}. Erro: {error}")
            return b''
        
    def read_int32(self, address: int) -> int:
        """Read 32-bit integer from memory"""
        data = self.read_memory(address, 4)
        if len(data) == 4:
            value = struct.unpack('<I', data)[0]
            logger.debug(f"Int32 em 0x{address:x}: {value}")
            return value
        return 0
        
    def read_int64(self, address: int) -> int:
        """Read 64-bit integer from memory"""
        data = self.read_memory(address, 8)
        if len(data) == 8:
            value = struct.unpack('<Q', data)[0]
            logger.debug(f"Int64 em 0x{address:x}: {value}")
            return value
        return 0
        
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
            result = data.decode('utf-8', errors='ignore')
            logger.debug(f"String em 0x{address:x}: '{result}'")
            return result
        except:
            logger.warning(f"Erro ao decodificar string em 0x{address:x}")
            return ""
            
    def read_df_string(self, address: int, pointer_size: int = 8) -> str:
        """Read Dwarf Fortress string structure"""
        STRING_BUFFER_LENGTH = 16
        
        try:
            len_offset = STRING_BUFFER_LENGTH
            cap_offset = STRING_BUFFER_LENGTH + pointer_size
            
            length = self.read_int64(address + len_offset) if pointer_size == 8 else self.read_int32(address + len_offset)
            capacity = self.read_int64(address + cap_offset) if pointer_size == 8 else self.read_int32(address + cap_offset)
            
            logger.debug(f"DF String em 0x{address:x}: length={length}, capacity={capacity}")
            
            if capacity == 0 or length == 0:
                return ""
                
            if length > capacity or length > 1024:
                logger.warning(f"String DF suspeita: length={length}, capacity={capacity}")
                return ""
                
            if capacity >= STRING_BUFFER_LENGTH:
                buffer_addr = self.read_pointer(address, pointer_size)
                logger.debug(f"String heap-allocated em 0x{buffer_addr:x}")
            else:
                buffer_addr = address
                logger.debug(f"String usando buffer interno")
                
            return self.read_string(buffer_addr, min(length, 1024))
            
        except Exception as e:
            logger.error(f"Erro ao ler DF string em 0x{address:x}: {e}")
            return ""

class MemoryLayout:
    """Handles memory layout configuration for specific DF versions"""
    
    def __init__(self, layout_file: Path):
        logger.info(f"Carregando layout de memória: {layout_file}")
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
            logger.info(f"Info do layout: {self.info}")
            
        if 'addresses' in self.config:
            self.addresses = {k: int(v, 16) for k, v in self.config['addresses'].items()}
            logger.info(f"Carregados {len(self.addresses)} endereços globais")
            
        if 'dwarf_offsets' in self.config:
            self.offsets['dwarf'] = {k: int(v, 16) for k, v in self.config['dwarf_offsets'].items()}
            logger.info(f"Carregados {len(self.offsets['dwarf'])} offsets de dwarf")
            
        for section in ['race_offsets', 'caste_offsets', 'hist_figure_offsets']:
            if section in self.config:
                key = section.replace('_offsets', '')
                self.offsets[key] = {k: int(v, 16) for k, v in self.config[section].items()}
                logger.info(f"Carregados {len(self.offsets[key])} offsets de {key}")
                
    def get_address(self, key: str) -> int:
        """Get global address for a key"""
        addr = self.addresses.get(key, 0)
        if addr:
            logger.debug(f"Endereço {key}: 0x{addr:x}")
        return addr
        
    def get_offset(self, section: str, key: str) -> int:
        """Get offset for a specific section and key"""
        offset = self.offsets.get(section, {}).get(key, 0)
        if offset:
            logger.debug(f"Offset {section}.{key}: 0x{offset:x}")
        return offset
        
    def get_checksum(self) -> str:
        """Get the expected checksum for this layout"""
        return self.info.get('checksum', '')

class DFInstance:
    """Main class for interacting with Dwarf Fortress memory"""
    
    def __init__(self):
        logger.info("Inicializando DFInstance")
        self.memory_reader = MemoryReader()
        self.layout: Optional[MemoryLayout] = None
        self.pid = 0
        self.base_addr = 0
        self.pointer_size = 8
        self.status = DFStatus.DISCONNECTED
        self.dwarves: List[DwarfData] = []
        
    def find_df_process(self) -> bool:
        """Find running Dwarf Fortress process"""
        logger.info("Procurando processo do Dwarf Fortress...")
        
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                proc_name = proc.info['name'].lower()
                if 'dwarf fortress' in proc_name or proc_name == 'dwarffortress.exe':
                    self.pid = proc.info['pid']
                    logger.info(f"Encontrado processo DF: {proc.info['name']} (PID {self.pid})")
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                logger.debug(f"Erro ao acessar processo: {e}")
                continue
        
        logger.error("Processo do Dwarf Fortress não encontrado")
        return False
        
    def connect(self) -> bool:
        """Connect to Dwarf Fortress process"""
        logger.info("=== INICIANDO CONEXÃO COM DWARF FORTRESS ===")
        
        if not self.find_df_process():
            return False
            
        if not self.memory_reader.open_process(self.pid):
            return False
            
        if not self._read_pe_header():
            return False
            
        self.status = DFStatus.CONNECTED
        logger.info(f"Conectado ao DF. Base address: 0x{self.base_addr:x}, Pointer size: {self.pointer_size}")
        return True
        
    def _read_pe_header(self) -> bool:
        """Read PE header to determine base address and architecture"""
        logger.info("Lendo PE header...")
        
        try:
            # Usar método alternativo: EnumProcessModules para obter endereço base
            import ctypes
            from ctypes import wintypes
            
            # Definir estruturas necessárias
            psapi = ctypes.windll.psapi
            kernel32 = ctypes.windll.kernel32
            
            # Enumerar módulos do processo
            hModules = (wintypes.HMODULE * 1024)()
            process_handle = self.memory_reader.process_handle
            cb = wintypes.DWORD()
            
            # Chamar EnumProcessModules
            if psapi.EnumProcessModules(process_handle, hModules, ctypes.sizeof(hModules), ctypes.byref(cb)):
                module_count = cb.value // ctypes.sizeof(wintypes.HMODULE)
                logger.info(f"Encontrados {module_count} módulos")
                
                # O primeiro módulo é geralmente o executável principal
                base_addr = hModules[0]
                logger.info(f"Endereço base do módulo principal: 0x{base_addr:x}")
            else:
                logger.error("Falha ao enumerar módulos")
                return False
            logger.info(f"Endereço base bruto: 0x{base_addr:x}")
            
            # Ler DOS header
            dos_header = self.memory_reader.read_memory(base_addr, 64)
            if len(dos_header) < 64:
                logger.error("Falha ao ler DOS header")
                return False
                
            if dos_header[:2] != b'MZ':
                logger.error("Assinatura DOS inválida")
                return False
                
            logger.info("DOS header válido encontrado")
            
            # Obter offset do PE header
            pe_offset = struct.unpack('<I', dos_header[60:64])[0]
            logger.info(f"PE offset: 0x{pe_offset:x}")
            
            # Ler PE header
            pe_header = self.memory_reader.read_memory(base_addr + pe_offset, 24)
            if len(pe_header) < 24:
                logger.error("Falha ao ler PE header")
                return False
                
            if pe_header[:4] != b'PE\x00\x00':
                logger.error("Assinatura PE inválida")
                return False
                
            logger.info("PE header válido encontrado")
            
            # Obter tipo de máquina
            machine_type = struct.unpack('<H', pe_header[4:6])[0]
            logger.info(f"Tipo de máquina: 0x{machine_type:x}")
            
            if machine_type == 0x8664:  # AMD64
                self.pointer_size = 8
                self.base_addr = base_addr - 0x140000000
                logger.info("Arquitetura: AMD64 (64-bit)")
            elif machine_type == 0x14c:  # i386
                self.pointer_size = 4
                self.base_addr = base_addr - 0x400000
                logger.info("Arquitetura: i386 (32-bit)")
            else:
                logger.warning(f"Tipo de máquina desconhecido: 0x{machine_type:x}, usando padrões")
                self.pointer_size = 8
                self.base_addr = base_addr - 0x140000000
                
            logger.info(f"Base address calculado: 0x{self.base_addr:x}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao ler PE header: {e}")
            logger.error(traceback.format_exc())
            return False
            
    def load_memory_layout(self, layout_file: Path = None) -> bool:
        """Load memory layout for current DF version"""
        logger.info("=== CARREGANDO LAYOUT DE MEMÓRIA ===")
        
        if layout_file is None:
            layouts_dir = Path(__file__).parent / "share" / "memory_layouts" / "windows"
            if not layouts_dir.exists():
                logger.error(f"Diretório de layouts não encontrado: {layouts_dir}")
                return False
                
            layout_files = list(layouts_dir.glob("*.ini"))
            if not layout_files:
                logger.error("Nenhum arquivo de layout encontrado")
                return False
                
            # Usar o layout mais recente (simplificado)
            layout_file = sorted(layout_files)[-1]
            logger.info(f"Usando layout: {layout_file.name}")
            
        try:
            self.layout = MemoryLayout(layout_file)
            self.status = DFStatus.LAYOUT_OK
            logger.info("Layout de memória carregado com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro ao carregar layout: {e}")
            return False
            
    def read_dwarves(self) -> List[DwarfData]:
        """Read all dwarves from memory"""
        logger.info("=== LENDO DADOS DOS DWARVES ===")
        
        if self.status < DFStatus.LAYOUT_OK:
            logger.error("Não conectado ou layout não carregado")
            return []
            
        try:
            creature_vector_addr = self.layout.get_address('creature_vector')
            if not creature_vector_addr:
                logger.error("Endereço creature_vector não encontrado no layout")
                return []
                
            # Ajustar para endereço base
            creature_vector_addr += self.base_addr
            logger.info(f"Endereço do vetor de criaturas: 0x{creature_vector_addr:x}")
            
            # Ler ponteiros do vetor
            start_ptr = self.memory_reader.read_pointer(creature_vector_addr, self.pointer_size)
            end_ptr = self.memory_reader.read_pointer(creature_vector_addr + self.pointer_size, self.pointer_size)
            
            logger.info(f"Vetor de criaturas: início=0x{start_ptr:x}, fim=0x{end_ptr:x}")
            
            if start_ptr == 0 or end_ptr == 0 or start_ptr >= end_ptr:
                logger.error("Ponteiros do vetor de criaturas inválidos")
                return []
                
            creature_count = (end_ptr - start_ptr) // self.pointer_size
            logger.info(f"Encontradas {creature_count} criaturas")
            
            dwarves = []
            for i in range(min(creature_count, 1000)):
                creature_ptr_addr = start_ptr + (i * self.pointer_size)
                creature_addr = self.memory_reader.read_pointer(creature_ptr_addr, self.pointer_size)
                
                if creature_addr == 0:
                    continue
                    
                logger.debug(f"Lendo criatura {i+1}/{creature_count} em 0x{creature_addr:x}")
                dwarf = self._read_dwarf(creature_addr)
                if dwarf and dwarf.name:
                    dwarves.append(dwarf)
                    logger.debug(f"Dwarf adicionado: {dwarf.name} (ID: {dwarf.id})")
                    
            self.dwarves = dwarves
            self.status = DFStatus.GAME_LOADED
            logger.info(f"=== LEITURA CONCLUÍDA: {len(dwarves)} dwarves carregados ===")
            return dwarves
            
        except Exception as e:
            logger.error(f"Erro ao ler dwarves: {e}")
            logger.error(traceback.format_exc())
            return []
            
    def _read_dwarf(self, address: int) -> Optional[DwarfData]:
        """Read single dwarf data from memory"""
        try:
            offsets = self.layout.offsets.get('dwarf', {})
            if not offsets:
                logger.warning("Offsets de dwarf não encontrados")
                return None
                
            dwarf = DwarfData(address=address)
            
            # Ler campos básicos
            dwarf.id = self.memory_reader.read_int32(address + offsets.get('id', 0))
            dwarf.race = self.memory_reader.read_int32(address + offsets.get('race', 0))
            dwarf.caste = self.memory_reader.read_int32(address + offsets.get('caste', 0))
            dwarf.sex = self.memory_reader.read_int32(address + offsets.get('sex', 0))
            dwarf.profession = self.memory_reader.read_int32(address + offsets.get('profession', 0))
            dwarf.mood = self.memory_reader.read_int32(address + offsets.get('mood', 0))
            
            # Ler nome
            name_offset = offsets.get('name', 0)
            if name_offset:
                dwarf.name = self.memory_reader.read_df_string(address + name_offset, self.pointer_size)
                
            # Ler profissão customizada
            custom_prof_offset = offsets.get('custom_profession', 0)
            if custom_prof_offset:
                dwarf.custom_profession = self.memory_reader.read_df_string(address + custom_prof_offset, self.pointer_size)
                
            # Calcular idade
            birth_year_offset = offsets.get('birth_year', 0)
            if birth_year_offset:
                birth_year = self.memory_reader.read_int32(address + birth_year_offset)
                current_year_addr = self.layout.get_address('current_year')
                if current_year_addr:
                    current_year = self.memory_reader.read_int32(current_year_addr + self.base_addr)
                    dwarf.age = current_year - birth_year
                    
            logger.debug(f"Dwarf lido: {dwarf.name} (ID: {dwarf.id}, Idade: {dwarf.age})")
            return dwarf
            
        except Exception as e:
            logger.warning(f"Erro ao ler dwarf em 0x{address:x}: {e}")
            return None
            
    def export_to_json(self, filename: str = "dwarves_data.json") -> bool:
        """Export dwarf data to JSON file"""
        try:
            logger.info(f"Exportando dados para {filename}")
            
            data = {
                'metadata': {
                    'version': '1.0',
                    'timestamp': str(pd.Timestamp.now()),
                    'dwarf_count': len(self.dwarves),
                    'base_address': f"0x{self.base_addr:x}",
                    'pointer_size': self.pointer_size,
                    'layout_info': self.layout.info if self.layout else {}
                },
                'dwarves': [dwarf.to_dict() for dwarf in self.dwarves]
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            logger.info(f"Dados exportados com sucesso para {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao exportar para JSON: {e}")
            return False
            
    def disconnect(self):
        """Disconnect from process"""
        logger.info("Desconectando do processo")
        self.memory_reader.close_process()
        self.status = DFStatus.DISCONNECTED
        
    def __del__(self):
        self.disconnect()

def main():
    """Example usage with detailed logging"""
    print("=" * 60)
    print("DWARF THERAPIST PYTHON EDITION - VERSÃO COM LOGS")
    print("=" * 60)
    
    df = DFInstance()
    
    try:
        # Conectar ao DF
        if not df.connect():
            print("\n❌ Falha ao conectar ao Dwarf Fortress")
            print("Verifique se o jogo está rodando e tente novamente")
            return
            
        print("✅ Conectado ao Dwarf Fortress")
        
        # Carregar layout de memória
        if not df.load_memory_layout():
            print("❌ Falha ao carregar layout de memória")
            return
            
        print("✅ Layout de memória carregado")
        
        # Ler dwarves
        print("\n📖 Lendo dados dos dwarves...")
        dwarves = df.read_dwarves()
        
        if not dwarves:
            print("❌ Nenhum dwarf encontrado ou falha na leitura")
            return
            
        print(f"✅ {len(dwarves)} dwarves carregados com sucesso")
        
        # Mostrar informações dos dwarves
        print(f"\n{'='*80}")
        print(f"{'ID':<6} {'Nome':<25} {'Profissão':<15} {'Idade':<5} {'Humor':<5}")
        print(f"{'='*80}")
        
        for dwarf in dwarves[:20]:  # Mostrar primeiros 20
            profession = dwarf.custom_profession if dwarf.custom_profession else str(dwarf.profession)
            print(f"{dwarf.id:<6} {dwarf.name:<25} {profession:<15} {dwarf.age:<5} {dwarf.mood:<5}")
            
        if len(dwarves) > 20:
            print(f"\n(Mostrando primeiros 20 de {len(dwarves)} dwarves)")
        
        # Exportar para JSON
        print(f"\n💾 Exportando dados para JSON...")
        if df.export_to_json():
            print("✅ Dados exportados para 'dwarves_data.json'")
        else:
            print("❌ Falha ao exportar dados")
            
        # Estatísticas
        print(f"\n📊 ESTATÍSTICAS:")
        print(f"   • Total de dwarves: {len(dwarves)}")
        print(f"   • Dwarves com nome: {len([d for d in dwarves if d.name])}")
        print(f"   • Profissões customizadas: {len([d for d in dwarves if d.custom_profession])}")
        
        ages = [d.age for d in dwarves if d.age > 0]
        if ages:
            print(f"   • Idade média: {sum(ages) / len(ages):.1f} anos")
            print(f"   • Dwarf mais novo: {min(ages)} anos")
            print(f"   • Dwarf mais velho: {max(ages)} anos")
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrompido pelo usuário")
    except Exception as e:
        logger.error(f"Erro não tratado: {e}")
        logger.error(traceback.format_exc())
        print(f"\n❌ Erro: {e}")
    finally:
        df.disconnect()
        print("\n🔌 Desconectado do Dwarf Fortress")

# Adicionar pandas para timestamp (fallback se não disponível)
try:
    import pandas as pd
except ImportError:
    import datetime
    class pd:
        class Timestamp:
            @staticmethod
            def now():
                return datetime.datetime.now()

if __name__ == "__main__":
    main()