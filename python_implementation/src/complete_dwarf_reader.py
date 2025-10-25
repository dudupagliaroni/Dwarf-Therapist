#!/usr/bin/env python3
"""
Dwarf Therapist Python Edition - VERSÃO COMPLETA
Lê TODOS os dados possíveis da memória do Dwarf Fortress
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
from dataclasses import dataclass, asdict, field
from enum import IntEnum
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('dwarf_therapist_complete.log')
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
class Skill:
    """Skill information"""
    id: int = 0
    level: int = 0
    experience: int = 0
    name: str = ""

@dataclass
class Attribute:
    """Physical or mental attribute"""
    id: int = 0
    value: int = 0
    max_value: int = 0
    name: str = ""

@dataclass
class Labor:
    """Labor assignment"""
    id: int = 0
    enabled: bool = False
    name: str = ""

@dataclass
class Wound:
    """Wound information"""
    id: int = 0
    body_part: int = 0
    layer: int = 0
    bleeding: int = 0
    pain: int = 0
    flags: int = 0

@dataclass
class Equipment:
    """Equipment/item information"""
    item_id: int = 0
    item_type: int = 0
    material_type: int = 0
    material_index: int = 0
    quality: int = 0
    wear: int = 0

@dataclass
class Syndrome:
    """Active syndrome/disease"""
    syndrome_id: int = 0
    severity: int = 0
    duration: int = 0

@dataclass
class Personality:
    """Personality traits"""
    traits: Dict[int, int] = field(default_factory=dict)
    stress_level: int = 0
    focus_level: int = 0

@dataclass
class CompletelyDwarfData:
    """ESTRUTURA COMPLETA com TODOS os dados possíveis"""
    # Dados básicos
    id: int = 0
    name: str = ""
    custom_profession: str = ""
    profession: int = 0
    race: int = 0
    caste: int = 0
    sex: int = 0
    age: int = 0
    birth_year: int = 0
    birth_time: int = 0
    
    # Status e flags
    mood: int = 0
    temp_mood: int = 0
    happiness: int = 0
    flags1: int = 0
    flags2: int = 0
    flags3: int = 0
    
    # Físico
    body_size: int = 0
    blood_level: int = 0
    
    # IDs e referências
    hist_id: int = 0
    civ_id: int = 0
    squad_id: int = 0
    squad_position: int = 0
    pet_owner_id: int = 0
    
    # Dados complexos
    skills: List[Skill] = field(default_factory=list)
    physical_attributes: List[Attribute] = field(default_factory=list)
    mental_attributes: List[Attribute] = field(default_factory=list)
    labors: List[Labor] = field(default_factory=list)
    wounds: List[Wound] = field(default_factory=list)
    equipment: List[Equipment] = field(default_factory=list)
    syndromes: List[Syndrome] = field(default_factory=list)
    personality: Optional[Personality] = None
    
    # Contadores e status
    turn_count: int = 0
    counters: Dict[str, int] = field(default_factory=dict)
    
    # Endereços técnicos
    address: int = 0
    soul_address: int = 0
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        result = {}
        for key, value in asdict(self).items():
            if isinstance(value, list) and value and hasattr(value[0], '__dict__'):
                result[key] = [item.__dict__ if hasattr(item, '__dict__') else item for item in value]
            elif hasattr(value, '__dict__'):
                result[key] = value.__dict__
            else:
                result[key] = value
        return result

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
        
        return buffer.raw if success else b''
        
    def read_int32(self, address: int) -> int:
        """Read 32-bit integer from memory"""
        data = self.read_memory(address, 4)
        return struct.unpack('<I', data)[0] if len(data) == 4 else 0
        
    def read_int16(self, address: int) -> int:
        """Read 16-bit integer from memory"""
        data = self.read_memory(address, 2)
        return struct.unpack('<H', data)[0] if len(data) == 2 else 0
        
    def read_int16_signed(self, address: int) -> int:
        """Read signed 16-bit integer from memory"""
        data = self.read_memory(address, 2)
        return struct.unpack('<h', data)[0] if len(data) == 2 else 0
        
    def read_int8(self, address: int) -> int:
        """Read 8-bit integer from memory"""
        data = self.read_memory(address, 1)
        return struct.unpack('<B', data)[0] if len(data) == 1 else 0
        
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
            
    def read_df_string(self, address: int, pointer_size: int = 8) -> str:
        """Read Dwarf Fortress string structure"""
        STRING_BUFFER_LENGTH = 16
        
        try:
            len_offset = STRING_BUFFER_LENGTH
            cap_offset = STRING_BUFFER_LENGTH + pointer_size
            
            length = self.read_int64(address + len_offset) if pointer_size == 8 else self.read_int32(address + len_offset)
            capacity = self.read_int64(address + cap_offset) if pointer_size == 8 else self.read_int32(address + cap_offset)
            
            if capacity == 0 or length == 0:
                return ""
                
            if length > capacity or length > 1024:
                return ""
                
            if capacity >= STRING_BUFFER_LENGTH:
                buffer_addr = self.read_pointer(address, pointer_size)
            else:
                buffer_addr = address
                
            data = self.read_memory(buffer_addr, min(length, 1024))
            if not data:
                return ""
                
            null_pos = data.find(b'\x00')
            if null_pos >= 0:
                data = data[:null_pos]
                
            return data.decode('utf-8', errors='ignore')
            
        except Exception as e:
            logger.debug(f"Erro ao ler DF string em 0x{address:x}: {e}")
            return ""

    def read_vector(self, address: int, pointer_size: int = 8) -> List[int]:
        """Read std::vector of pointers"""
        try:
            start_ptr = self.read_pointer(address, pointer_size)
            end_ptr = self.read_pointer(address + pointer_size, pointer_size)
            
            if start_ptr == 0 or end_ptr == 0 or start_ptr >= end_ptr:
                return []
                
            count = (end_ptr - start_ptr) // pointer_size
            if count > 10000:  # Sanity check
                return []
                
            pointers = []
            for i in range(count):
                ptr_addr = start_ptr + (i * pointer_size)
                ptr = self.read_pointer(ptr_addr, pointer_size)
                if ptr != 0:
                    pointers.append(ptr)
                    
            return pointers
            
        except Exception as e:
            logger.debug(f"Erro ao ler vetor em 0x{address:x}: {e}")
            return []

class MemoryLayout:
    """Handles memory layout configuration for specific DF versions"""
    
    def __init__(self, layout_file: Path):
        logger.info(f"Carregando layout de memória: {layout_file}")
        
        if not layout_file.exists():
            raise FileNotFoundError(f"Arquivo de layout não existe: {layout_file}")
            
        self.config = configparser.ConfigParser()
        
        try:
            self.config.read(layout_file, encoding='utf-8')
            logger.info(f"Arquivo de layout lido. Seções encontradas: {list(self.config.sections())}")
        except Exception as e:
            logger.error(f"Erro ao ler arquivo de layout: {e}")
            raise
            
        self.offsets = {}
        self.addresses = {}
        self.info = {}
        
        self._load_sections()
        
    def _load_sections(self):
        """Load all relevant sections from memory layout"""
        if 'info' in self.config:
            self.info = dict(self.config['info'])
            logger.info(f"Info carregado: {self.info}")
            
        if 'addresses' in self.config:
            self.addresses = {k: int(v, 16) for k, v in self.config['addresses'].items()}
            logger.info(f"Endereços carregados: {len(self.addresses)} itens")
            logger.debug(f"Endereços principais: creature_vector=0x{self.addresses.get('creature_vector', 0):x}")
            
        # Carregar todas as seções de offsets - usando nomes corretos do arquivo
        offset_sections = [
            'offsets', 'dwarf_offsets', 'soul_details', 'unit_wound_offsets',
            'race_offsets', 'caste_offsets', 'hist_figure_offsets',
            'item_offsets', 'syndrome_offsets', 'emotion_offsets',
            'need_offsets', 'job_details', 'squad_offsets', 'activity_offsets'
        ]
        
        for section in offset_sections:
            if section in self.config:
                # Mapear nomes de seções para chaves mais simples
                key_map = {
                    'offsets': 'general',
                    'dwarf_offsets': 'dwarf', 
                    'soul_details': 'soul',
                    'unit_wound_offsets': 'unit_wound',
                    'race_offsets': 'race',
                    'caste_offsets': 'caste',
                    'hist_figure_offsets': 'hist_figure',
                    'item_offsets': 'item',
                    'syndrome_offsets': 'syndrome',
                    'emotion_offsets': 'emotion',
                    'need_offsets': 'need',
                    'job_details': 'job',
                    'squad_offsets': 'squad',
                    'activity_offsets': 'activity'
                }
                
                key = key_map.get(section, section.replace('_offsets', '').replace('_details', ''))
                self.offsets[key] = {k: int(v, 16) for k, v in self.config[section].items()}
                logger.info(f"Seção {section} carregada como '{key}': {len(self.offsets[key])} offsets")
            else:
                logger.warning(f"Seção {section} não encontrada no layout")
                
        logger.info(f"Total de seções de offset carregadas: {len(self.offsets)}")
        logger.info(f"Seções disponíveis: {list(self.offsets.keys())}")
                
    def get_address(self, key: str) -> int:
        """Get global address for a key"""
        return self.addresses.get(key, 0)
        
    def get_offset(self, section: str, key: str) -> int:
        """Get offset for a specific section and key"""
        return self.offsets.get(section, {}).get(key, 0)
        """Get global address for a key"""
        return self.addresses.get(key, 0)
        
    def get_offset(self, section: str, key: str) -> int:
        """Get offset for a specific section and key"""
        return self.offsets.get(section, {}).get(key, 0)

class CompleteDFInstance:
    """Instância completa que lê TODOS os dados possíveis"""
    
    def __init__(self):
        logger.info("Inicializando CompleteDFInstance")
        self.memory_reader = MemoryReader()
        self.layout: Optional[MemoryLayout] = None
        self.pid = 0
        self.base_addr = 0
        self.pointer_size = 8
        self.status = DFStatus.DISCONNECTED
        self.dwarves: List[CompletelyDwarfData] = []
        
        # Dados de referência
        self.skill_names = self._load_skill_names()
        self.attribute_names = self._load_attribute_names()
        self.labor_names = self._load_labor_names()
        
    def _load_skill_names(self) -> Dict[int, str]:
        """Load skill names"""
        return {
            0: "Mining", 1: "Woodcutting", 2: "Carpentry", 3: "Stoneworking", 
            4: "Engraving", 5: "Masonry", 6: "Animal Care", 7: "Animal Training",
            8: "Hunting", 9: "Fishing", 10: "Butchery", 11: "Trapping",
            12: "Tanning", 13: "Leatherworking", 14: "Brewing", 15: "Cooking",
            16: "Herbalism", 17: "Threshing", 18: "Milling", 19: "Processing",
            20: "Cheesemaking", 21: "Milking", 22: "Shearing", 23: "Spinning",
            24: "Weaving", 25: "Clothesmaking", 26: "Glassmaking", 27: "Potting"
        }
        
    def _load_attribute_names(self) -> Dict[int, str]:
        """Load attribute names"""
        return {
            0: "Strength", 1: "Agility", 2: "Toughness", 3: "Endurance",
            4: "Recuperation", 5: "Disease Resistance", 6: "Analytical Ability",
            7: "Focus", 8: "Willpower", 9: "Creativity", 10: "Intuition",
            11: "Patience", 12: "Memory", 13: "Linguistic Ability"
        }
        
    def _load_labor_names(self) -> Dict[int, str]:
        """Load labor names"""
        return {
            0: "Mine", 1: "Cut Wood", 2: "Carpentry", 3: "Stonework",
            4: "Engraving", 5: "Masonry", 6: "Animal Care", 7: "Animal Train",
            8: "Hunt", 9: "Fish", 10: "Butcher", 11: "Trap"
        }
        
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
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        logger.warning("Processo do Dwarf Fortress nao encontrado!")
        return False
    
    @staticmethod
    def is_df_running() -> bool:
        """Verifica se o Dwarf Fortress esta rodando"""
        for proc in psutil.process_iter(['name']):
            try:
                proc_name = proc.info['name'].lower()
                if 'dwarf fortress' in proc_name or proc_name == 'dwarffortress.exe':
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return False
        
    def connect(self) -> bool:
        """Connect to Dwarf Fortress process"""
        logger.info("=== CONECTANDO AO DWARF FORTRESS ===")
        
        if not self.find_df_process():
            return False
            
        if not self.memory_reader.open_process(self.pid):
            return False
            
        if not self._read_pe_header():
            return False
            
        self.status = DFStatus.CONNECTED
        return True
        
    def _read_pe_header(self) -> bool:
        """Read PE header to determine base address and architecture"""
        try:
            import ctypes
            from ctypes import wintypes
            
            psapi = ctypes.windll.psapi
            hModules = (wintypes.HMODULE * 1024)()
            process_handle = self.memory_reader.process_handle
            cb = wintypes.DWORD()
            
            if psapi.EnumProcessModules(process_handle, hModules, ctypes.sizeof(hModules), ctypes.byref(cb)):
                base_addr = hModules[0]
                logger.info(f"Endereço base: 0x{base_addr:x}")
            else:
                return False
                
            # Ler DOS header
            dos_header = self.memory_reader.read_memory(base_addr, 64)
            if len(dos_header) < 64 or dos_header[:2] != b'MZ':
                return False
                
            pe_offset = struct.unpack('<I', dos_header[60:64])[0]
            pe_header = self.memory_reader.read_memory(base_addr + pe_offset, 24)
            
            if len(pe_header) < 24 or pe_header[:4] != b'PE\x00\x00':
                return False
                
            machine_type = struct.unpack('<H', pe_header[4:6])[0]
            
            if machine_type == 0x8664:  # AMD64
                self.pointer_size = 8
                self.base_addr = base_addr - 0x140000000
            elif machine_type == 0x14c:  # i386
                self.pointer_size = 4
                self.base_addr = base_addr - 0x400000
            else:
                self.pointer_size = 8
                self.base_addr = base_addr - 0x140000000
                
            return True
        except Exception as e:
            logger.error(f"Erro ao ler PE header: {e}")
            return False
            
    def load_memory_layout(self, layout_file: Path = None) -> bool:
        """Load memory layout for current DF version"""
        if layout_file is None:
            # Corrigir o caminho para os layouts de memória
            layouts_dir = Path(__file__).parent.parent.parent / "share" / "memory_layouts" / "windows"
            logger.info(f"Procurando layouts em: {layouts_dir}")
            
            if not layouts_dir.exists():
                logger.error(f"Diretório de layouts não existe: {layouts_dir}")
                return False
                
            layout_files = list(layouts_dir.glob("*.ini"))
            if not layout_files:
                logger.error(f"Nenhum arquivo de layout encontrado em: {layouts_dir}")
                return False
                
            # Usar o layout mais recente (ordenar por nome - versões mais recentes vêm por último)
            layout_file = sorted(layout_files, key=lambda x: x.name)[-1]
            logger.info(f"Usando layout: {layout_file.name}")
            
        try:
            self.layout = MemoryLayout(layout_file)
            self.status = DFStatus.LAYOUT_OK
            logger.info("Layout carregado com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro ao carregar layout: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return False
            
    def read_complete_dwarves(self) -> List[CompletelyDwarfData]:
        """Lê TODOS os dados possíveis dos dwarves"""
        logger.info("=== LENDO DADOS COMPLETOS DOS DWARVES ===")
        
        if self.status < DFStatus.LAYOUT_OK:
            logger.error(f"Status inadequado para leitura: {self.status}")
            return []
            
        try:
            creature_vector_addr = self.layout.get_address('creature_vector')
            if not creature_vector_addr:
                logger.error("Endereço creature_vector não encontrado no layout")
                logger.error(f"Endereços disponíveis: {list(self.layout.addresses.keys())}")
                return []
                
            logger.info(f"creature_vector base: 0x{creature_vector_addr:x}")
            creature_vector_addr += self.base_addr
            logger.info(f"creature_vector final: 0x{creature_vector_addr:x}")
            
            creature_pointers = self.memory_reader.read_vector(creature_vector_addr, self.pointer_size)
            
            logger.info(f"Encontradas {len(creature_pointers)} criaturas")
            
            if not creature_pointers:
                logger.warning("Nenhuma criatura encontrada no vetor")
                return []
            
            complete_dwarves = []
            for i, creature_addr in enumerate(creature_pointers[:500]):  # Limite para performance
                logger.debug(f"Processando criatura {i+1}/{len(creature_pointers)} em 0x{creature_addr:x}")
                dwarf = self._read_complete_dwarf(creature_addr)
                if dwarf and dwarf.name:
                    complete_dwarves.append(dwarf)
                    logger.debug(f"Dwarf carregado: {dwarf.name} (ID: {dwarf.id})")
                    
            self.dwarves = complete_dwarves
            
            if complete_dwarves:
                self.status = DFStatus.GAME_LOADED
                logger.info(f"=== CARREGADOS {len(complete_dwarves)} DWARVES COMPLETOS ===")
            else:
                logger.warning("Nenhum dwarf válido foi carregado")
                
            return complete_dwarves
            
        except Exception as e:
            logger.error(f"Erro ao ler dwarves completos: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return []
            
    def _read_complete_dwarf(self, address: int) -> Optional[CompletelyDwarfData]:
        """Lê TODOS os dados de um dwarf"""
        try:
            offsets = self.layout.offsets.get('dwarf', {})
            if not offsets:
                return None
                
            dwarf = CompletelyDwarfData(address=address)
            
            # 1. DADOS BÁSICOS
            dwarf.id = self.memory_reader.read_int32(address + offsets.get('id', 0))
            dwarf.race = self.memory_reader.read_int32(address + offsets.get('race', 0))
            dwarf.caste = self.memory_reader.read_int16(address + offsets.get('caste', 0))
            dwarf.sex = self.memory_reader.read_int8(address + offsets.get('sex', 0))
            dwarf.profession = self.memory_reader.read_int8(address + offsets.get('profession', 0))
            dwarf.mood = self.memory_reader.read_int16_signed(address + offsets.get('mood', 0))
            dwarf.temp_mood = self.memory_reader.read_int16_signed(address + offsets.get('temp_mood', 0))
            
            # 2. FLAGS E STATUS
            dwarf.flags1 = self.memory_reader.read_int32(address + offsets.get('flags1', 0))
            dwarf.flags2 = self.memory_reader.read_int32(address + offsets.get('flags2', 0))
            dwarf.flags3 = self.memory_reader.read_int32(address + offsets.get('flags3', 0))
            
            # 3. DADOS FÍSICOS
            dwarf.body_size = self.memory_reader.read_int32(address + offsets.get('size_info', 0))
            dwarf.blood_level = self.memory_reader.read_int32(address + offsets.get('blood', 0))
            
            # 4. IDS E REFERÊNCIAS
            dwarf.hist_id = self.memory_reader.read_int32(address + offsets.get('hist_id', 0))
            dwarf.civ_id = self.memory_reader.read_int32(address + offsets.get('civ', 0))
            dwarf.squad_id = self.memory_reader.read_int32(address + offsets.get('squad_id', 0))
            dwarf.squad_position = self.memory_reader.read_int32(address + offsets.get('squad_position', 0))
            dwarf.pet_owner_id = self.memory_reader.read_int32(address + offsets.get('pet_owner_id', 0))
            
            # 5. CONTADORES
            dwarf.turn_count = self.memory_reader.read_int32(address + offsets.get('turn_count', 0))
            dwarf.counters = {
                'counter1': self.memory_reader.read_int32(address + offsets.get('counters1', 0)),
                'counter2': self.memory_reader.read_int32(address + offsets.get('counters2', 0)),
                'counter3': self.memory_reader.read_int32(address + offsets.get('counters3', 0))
            }
            
            # 6. STRINGS
            name_offset = offsets.get('name', 0)
            if name_offset:
                dwarf.name = self.memory_reader.read_df_string(address + name_offset, self.pointer_size)
                
            custom_prof_offset = offsets.get('custom_profession', 0)
            if custom_prof_offset:
                dwarf.custom_profession = self.memory_reader.read_df_string(address + custom_prof_offset, self.pointer_size)
            
            # 7. IDADE
            birth_year_offset = offsets.get('birth_year', 0)
            birth_time_offset = offsets.get('birth_time', 0)
            if birth_year_offset:
                dwarf.birth_year = self.memory_reader.read_int32(address + birth_year_offset)
                if birth_time_offset:
                    dwarf.birth_time = self.memory_reader.read_int32(address + birth_time_offset)
                    
                current_year_addr = self.layout.get_address('current_year')
                if current_year_addr:
                    current_year = self.memory_reader.read_int32(current_year_addr + self.base_addr)
                    dwarf.age = current_year - dwarf.birth_year
            
            # 8. DADOS COMPLEXOS - SKILLS
            souls_offset = offsets.get('souls', 0)
            if souls_offset:
                dwarf.soul_address, dwarf.skills = self._read_skills(address + souls_offset)
                
            # 9. ATRIBUTOS FÍSICOS
            phys_attrs_offset = offsets.get('physical_attrs', 0)
            if phys_attrs_offset:
                dwarf.physical_attributes = self._read_attributes(address + phys_attrs_offset, is_physical=True)
                
            # 10. LABORS
            labors_offset = offsets.get('labors', 0)
            if labors_offset:
                dwarf.labors = self._read_labors(address + labors_offset)
                
            # 11. FERIMENTOS
            wounds_offset = offsets.get('wounds_vector', 0)
            if wounds_offset:
                dwarf.wounds = self._read_wounds(address + wounds_offset)
                
            # 12. SÍNDROMES
            syndrome_offset = offsets.get('active_syndrome_vector', 0)
            if syndrome_offset:
                dwarf.syndromes = self._read_syndromes(address + syndrome_offset)
                
            # 13. EQUIPAMENTOS
            inventory_offset = offsets.get('inventory', 0)
            if inventory_offset:
                dwarf.equipment = self._read_equipment(address + inventory_offset)
                
            # 14. PERSONALIDADE (da alma)
            if dwarf.soul_address:
                dwarf.personality = self._read_personality(dwarf.soul_address)
                dwarf.mental_attributes = self._read_mental_attributes(dwarf.soul_address)
                
            return dwarf
            
        except Exception as e:
            logger.debug(f"Erro ao ler dwarf completo em 0x{address:x}: {e}")
            return None
            
    def _read_skills(self, souls_vector_addr: int) -> Tuple[int, List[Skill]]:
        """Lê skills da alma do dwarf"""
        try:
            soul_pointers = self.memory_reader.read_vector(souls_vector_addr, self.pointer_size)
            if not soul_pointers:
                return 0, []
                
            soul_addr = soul_pointers[0]  # Primeira alma
            soul_offsets = self.layout.offsets.get('soul', {})
            skills_offset = soul_offsets.get('skills', 0)
            
            if not skills_offset:
                return soul_addr, []
                
            skills_vector_addr = soul_addr + skills_offset
            skill_pointers = self.memory_reader.read_vector(skills_vector_addr, self.pointer_size)
            
            skills = []
            for i, skill_addr in enumerate(skill_pointers[:50]):  # Limite de 50 skills
                # Estrutura de skill conforme código C++:
                # offset 0x00: skill_id (short/16 bits)
                # offset 0x04: rating/level (short/16 bits)  
                # offset 0x08: experience (int/32 bits)
                # offset 0x10: rust (int/32 bits)
                skill_id = self.memory_reader.read_int16(skill_addr)
                skill_level = self.memory_reader.read_int16(skill_addr + 4)
                skill_exp = self.memory_reader.read_int32(skill_addr + 8)
                
                skill = Skill(
                    id=skill_id,
                    level=skill_level,
                    experience=skill_exp,
                    name=self.skill_names.get(skill_id, f"Skill_{skill_id}")
                )
                skills.append(skill)
                
            return soul_addr, skills
            
        except Exception as e:
            logger.debug(f"Erro ao ler skills: {e}")
            return 0, []
            
    def _read_attributes(self, attr_addr: int, is_physical: bool = True) -> List[Attribute]:
        """Lê atributos físicos ou mentais"""
        try:
            attributes = []
            attr_names = self.attribute_names if not is_physical else self.attribute_names
            
            # Atributos são arrays de estruturas (current, max, ?)
            for attr_id in range(6 if is_physical else 7):  # 6 físicos, 7 mentais
                base_addr = attr_addr + (attr_id * 12)  # 12 bytes por atributo
                current_val = self.memory_reader.read_int32(base_addr)
                max_val = self.memory_reader.read_int32(base_addr + 4)
                
                attr = Attribute(
                    id=attr_id,
                    value=current_val,
                    max_value=max_val,
                    name=attr_names.get(attr_id, f"Attribute_{attr_id}")
                )
                attributes.append(attr)
                
            return attributes
        except Exception as e:
            logger.debug(f"Erro ao ler atributos: {e}")
            return []
            
    def _read_mental_attributes(self, soul_addr: int) -> List[Attribute]:
        """Lê atributos mentais da alma"""
        try:
            soul_offsets = self.layout.offsets.get('soul', {})
            mental_attrs_offset = soul_offsets.get('mental_attrs', 0)
            
            if not mental_attrs_offset:
                return []
                
            return self._read_attributes(soul_addr + mental_attrs_offset, is_physical=False)
        except Exception as e:
            logger.debug(f"Erro ao ler atributos mentais: {e}")
            return []
            
    def _read_labors(self, labors_addr: int) -> List[Labor]:
        """Lê trabalhos habilitados/desabilitados"""
        try:
            # Labors são um bitfield de ~30 bytes
            labor_data = self.memory_reader.read_memory(labors_addr, 32)
            if not labor_data:
                return []
                
            labors = []
            for labor_id in range(min(len(self.labor_names), 32 * 8)):
                byte_index = labor_id // 8
                bit_index = labor_id % 8
                
                if byte_index < len(labor_data):
                    enabled = bool(labor_data[byte_index] & (1 << bit_index))
                    
                    labor = Labor(
                        id=labor_id,
                        enabled=enabled,
                        name=self.labor_names.get(labor_id, f"Labor_{labor_id}")
                    )
                    labors.append(labor)
                    
            return labors
        except Exception as e:
            logger.debug(f"Erro ao ler labors: {e}")
            return []
            
    def _read_wounds(self, wounds_vector_addr: int) -> List[Wound]:
        """Lê ferimentos"""
        try:
            wound_pointers = self.memory_reader.read_vector(wounds_vector_addr, self.pointer_size)
            wound_offsets = self.layout.offsets.get('unit_wound', {})
            
            wounds = []
            for wound_addr in wound_pointers[:20]:  # Limite de 20 ferimentos
                wound = Wound(
                    id=self.memory_reader.read_int32(wound_addr + wound_offsets.get('id', 0)),
                    body_part=self.memory_reader.read_int32(wound_addr + wound_offsets.get('parts', 0)),
                    layer=self.memory_reader.read_int32(wound_addr + wound_offsets.get('layer', 0)),
                    bleeding=self.memory_reader.read_int32(wound_addr + wound_offsets.get('bleeding', 0)),
                    pain=self.memory_reader.read_int32(wound_addr + wound_offsets.get('pain', 0)),
                    flags=self.memory_reader.read_int32(wound_addr + wound_offsets.get('flags1', 0))
                )
                wounds.append(wound)
                
            return wounds
        except Exception as e:
            logger.debug(f"Erro ao ler ferimentos: {e}")
            return []
            
    def _read_syndromes(self, syndrome_vector_addr: int) -> List[Syndrome]:
        """Lê síndromes ativas"""
        try:
            syndrome_pointers = self.memory_reader.read_vector(syndrome_vector_addr, self.pointer_size)
            
            syndromes = []
            for syndrome_addr in syndrome_pointers[:10]:  # Limite de 10 síndromes
                syndrome = Syndrome(
                    syndrome_id=self.memory_reader.read_int32(syndrome_addr),
                    severity=self.memory_reader.read_int32(syndrome_addr + 4),
                    duration=self.memory_reader.read_int32(syndrome_addr + 8)
                )
                syndromes.append(syndrome)
                
            return syndromes
        except Exception as e:
            logger.debug(f"Erro ao ler síndromes: {e}")
            return []
            
    def _read_equipment(self, inventory_addr: int) -> List[Equipment]:
        """Lê equipamentos/inventário"""
        try:
            equipment_pointers = self.memory_reader.read_vector(inventory_addr, self.pointer_size)
            item_offsets = self.layout.offsets.get('item', {})
            
            equipment = []
            for item_addr in equipment_pointers[:50]:  # Limite de 50 itens
                item = Equipment(
                    item_id=self.memory_reader.read_int32(item_addr + item_offsets.get('id', 0)),
                    material_type=self.memory_reader.read_int32(item_addr + item_offsets.get('mat_type', 0)),
                    material_index=self.memory_reader.read_int32(item_addr + item_offsets.get('mat_index', 0)),
                    quality=self.memory_reader.read_int32(item_addr + item_offsets.get('quality', 0)),
                    wear=self.memory_reader.read_int32(item_addr + item_offsets.get('wear', 0))
                )
                equipment.append(item)
                
            return equipment
        except Exception as e:
            logger.debug(f"Erro ao ler equipamentos: {e}")
            return []
            
    def _read_personality(self, soul_addr: int) -> Optional[Personality]:
        """Lê personalidade da alma"""
        try:
            soul_offsets = self.layout.offsets.get('soul', {})
            
            stress_offset = soul_offsets.get('stress_level', 0)
            focus_offset = soul_offsets.get('current_focus', 0)
            traits_offset = soul_offsets.get('personality', 0)
            
            personality = Personality(
                stress_level=self.memory_reader.read_int32(soul_addr + stress_offset) if stress_offset else 0,
                focus_level=self.memory_reader.read_int32(soul_addr + focus_offset) if focus_offset else 0
            )
            
            # Ler traits (array de valores)
            if traits_offset:
                for trait_id in range(25):  # ~25 traits de personalidade
                    trait_addr = soul_addr + traits_offset + (trait_id * 4)
                    trait_value = self.memory_reader.read_int32(trait_addr)
                    personality.traits[trait_id] = trait_value
                    
            return personality
        except Exception as e:
            logger.debug(f"Erro ao ler personalidade: {e}")
            return None
            
    def export_complete_json(self, filename: str = None, decode_data: bool = True) -> bool:
        """Exporta TODOS os dados para JSON com decodificação opcional"""
        try:
            # Se não especificado, criar nome com timestamp na pasta exports
            if filename is None:
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                # Caminho relativo à pasta raiz do projeto
                exports_dir = Path(__file__).parent.parent.parent / "exports"
                exports_dir.mkdir(exist_ok=True)
                filename = exports_dir / f"complete_dwarves_data_{timestamp}.json"
            
            logger.info(f"Exportando dados completos para {filename}")
            
            # Calcular estatísticas
            total_skills = sum(len(d.skills) for d in self.dwarves)
            total_wounds = sum(len(d.wounds) for d in self.dwarves)
            total_equipment = sum(len(d.equipment) for d in self.dwarves)
            
            data = {
                'metadata': {
                    'version': '2.0-COMPLETE',
                    'timestamp': '2025-10-25T02:00:00Z',
                    'dwarf_count': len(self.dwarves),
                    'base_address': f"0x{self.base_addr:x}",
                    'pointer_size': self.pointer_size,
                    'layout_info': self.layout.info if self.layout else {},
                    'decoded': decode_data,
                    'statistics': {
                        'total_skills_read': total_skills,
                        'total_wounds_read': total_wounds,
                        'total_equipment_read': total_equipment,
                        'dwarves_with_skills': len([d for d in self.dwarves if d.skills]),
                        'dwarves_with_wounds': len([d for d in self.dwarves if d.wounds]),
                        'dwarves_with_equipment': len([d for d in self.dwarves if d.equipment])
                    }
                },
                'dwarves': [dwarf.to_dict() for dwarf in self.dwarves]
            }
            
            # Aplicar decodificação se solicitado
            if decode_data:
                logger.info("Aplicando decodificação aos dados...")
                try:
                    # Importar decodificador
                    tools_path = Path(__file__).parent.parent / "tools"
                    sys.path.insert(0, str(tools_path))
                    from complete_decoder import DwarfDataDecoder
                    
                    decoder = DwarfDataDecoder()
                    decoded_dwarves = []
                    
                    for i, dwarf_dict in enumerate(data['dwarves']):
                        if i % 50 == 0:
                            logger.info(f"Decodificando dwarf {i+1}/{len(data['dwarves'])}")
                        decoded_dwarf = decoder.decode_dwarf(dwarf_dict)
                        decoded_dwarves.append(decoded_dwarf)
                    
                    data['dwarves'] = decoded_dwarves
                    data['metadata']['decoder_version'] = '1.0'
                    logger.info("Decodificação aplicada com sucesso")
                    
                except Exception as e:
                    logger.warning(f"Erro na decodificação, salvando dados brutos: {e}")
                    data['metadata']['decoded'] = False
                    data['metadata']['decode_error'] = str(e)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            logger.info(f"Dados completos exportados: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao exportar JSON completo: {e}")
            return False
            
    def disconnect(self):
        """Disconnect from process"""
        self.memory_reader.close_process()
        self.status = DFStatus.DISCONNECTED

def main():
    """Execução principal com dados COMPLETOS"""
    print("DWARF THERAPIST PYTHON - VERSÃO COMPLETA")
    print("=" * 60)
    print("Lendo TODOS os dados possíveis da memória do DF!")
    
    # Verificar se o Dwarf Fortress está rodando
    if not CompleteDFInstance.is_df_running():
        print("ERRO: Dwarf Fortress não está em execução!")
        print("Por favor, inicie o Dwarf Fortress com um save carregado antes de executar este script.")
        return
    
    print("OK: Dwarf Fortress detectado em execução")
    
    df = CompleteDFInstance()
    
    try:
        # Conectar
        if not df.connect():
            print("ERRO: Falha ao conectar")
            return
        print("SUCESSO: Conectado ao DF")
        
        # Carregar layout
        if not df.load_memory_layout():
            print("ERRO: Falha ao carregar layout")
            return
        print("SUCESSO: Layout carregado")
        
        # Ler dados COMPLETOS
        print("\nLendo dados COMPLETOS dos dwarves...")
        dwarves = df.read_complete_dwarves()
        
        if not dwarves:
            print("ERRO: Nenhum dwarf encontrado")
            return
            
        # Estatísticas detalhadas
        print(f"\nDADOS CARREGADOS:")
        print(f"   Dwarves: {len(dwarves)}")
        print(f"   Com skills: {len([d for d in dwarves if d.skills])}")
        print(f"   Com ferimentos: {len([d for d in dwarves if d.wounds])}")
        print(f"   Com equipamentos: {len([d for d in dwarves if d.equipment])}")
        print(f"   Com personalidade: {len([d for d in dwarves if d.personality])}")
        
        # Primeiro dwarf como exemplo
        if dwarves:
            first = dwarves[0]
            print(f"\nEXEMPLO - {first.name}:")
            print(f"   ID: {first.id}, Idade: {first.age}")
            print(f"   Skills: {len(first.skills)}")
            print(f"   Atributos físicos: {len(first.physical_attributes)}")
            print(f"   Atributos mentais: {len(first.mental_attributes)}")
            print(f"   Labors: {len(first.labors)}")
            print(f"   Ferimentos: {len(first.wounds)}")
            print(f"   Equipamentos: {len(first.equipment)}")
            
        # Exportar tudo
        print(f"\nExportando dados completos...")
        if df.export_complete_json():
            print("SUCESSO: Dados exportados para a pasta 'exports/' com timestamp e decodificação")
        else:
            print("ERRO: Falha ao exportar")
            
    except Exception as e:
        logger.error(f"Erro: {e}")
        print(f"ERRO: {e}")
    finally:
        df.disconnect()

if __name__ == "__main__":
    main()