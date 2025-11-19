#!/usr/bin/env python3
"""
Dwarf Therapist Python Edition - VERSÃO COMPLETA
Lê TODOS os dados possíveis da memória do Dwarf Fortress

NOTA SOBRE VALORES SENTINELA:
    O valor 4294967295 (0xFFFFFFFF) é automaticamente convertido para -1
    Este valor representa "NULL" ou "não aplicável" no Dwarf Fortress
    
    Campos afetados:
    - squad_id: -1 = sem squad militar
    - squad_position: -1 = sem posição em squad  
    - pet_owner_id: -1 = não é pet de ninguém
    - equipment.quality: -1 = qualidade não definida
    - equipment.wear: -1 = desgaste não aplicável
    - wound.pain: -1 = sem dados de dor
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
    
    def to_dict(self, human_readable: bool = False):
        """Convert to dictionary for JSON serialization"""
        result = {}
        for key, value in asdict(self).items():
            if isinstance(value, list) and value and hasattr(value[0], '__dict__'):
                result[key] = [item.__dict__ if hasattr(item, '__dict__') else item for item in value]
            elif hasattr(value, '__dict__'):
                result[key] = value.__dict__
            else:
                result[key] = value
        
        # Adicionar campos decodificados se solicitado
        if human_readable:
            result['_decoded'] = {
                'flags': HumanReadableDecoder.decode_flags(self.flags1, self.flags2, self.flags3),
                'body': HumanReadableDecoder.interpret_body_size(self.body_size),
                'blood': HumanReadableDecoder.analyze_blood_level(self.blood_level),
                'history': HumanReadableDecoder.validate_hist_id(self.hist_id),
                'squad': HumanReadableDecoder.decode_squad_info(self.squad_id, self.squad_position),
                'pet': HumanReadableDecoder.decode_pet_owner(self.pet_owner_id),
                'equipment': [EquipmentDecoder.decode_equipment_item(item) for item in result.get('equipment', [])]
            }
        
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

class HumanReadableDecoder:
    """Decodifica dados numéricos em informações legíveis para humanos"""
    
    # Flags1 inválidas conhecidas
    INVALID_FLAGS1 = {
        0x00000002: "inactive",
        0x00000010: "marauder",
        0x00000040: "merchant",
        0x00000080: "part_of_caravan",
        0x00000800: "diplomat_or_liaison",
        0x00020000: "invader_hostile_1",
        0x00080000: "invader_hostile_2",
        0x00600000: "resident_invader_ambusher"
    }
    
    # Invalid Flags2 (based on C++ unithealth.cpp checks)
    INVALID_FLAGS2 = {
        0x00000080: "killed",
        0x00004000: "gutted",
        0x00040000: "underworld_creature",
        0x00080000: "resident",
        0x00400000: "uninvited_visitor",
        0x00800000: "visitor"
    }
    
    # Vision flags - these require INVERTED logic (based on C++ code)
    # In C++: !(flags2 & 0x02000000) means blind
    # So if bit is SET = has vision, if bit is CLEAR = blind
    VISION_FLAGS2 = {
        0x02000000: "has_vision",  # If CLEAR = completely_blind
        0x04000000: "vision_damaged",  # If SET = vision impaired
        0x08000000: "vision_slightly_damaged"  # If SET = vision slightly impaired
    }
    
    # Flags3 inválidas conhecidas
    INVALID_FLAGS3 = {
        0x00001000: "ghost"
    }
    
    @staticmethod
    def decode_flags(flags1: int, flags2: int, flags3: int) -> Dict[str, Any]:
        """Decodifica as flags em um dicionário legível"""
        result = {
            "flags1_raw": flags1,
            "flags2_raw": flags2,
            "flags3_raw": flags3,
            "flags1_hex": f"0x{flags1:08X}",
            "flags2_hex": f"0x{flags2:08X}",
            "flags3_hex": f"0x{flags3:08X}",
            "flags1_active": [],
            "flags2_active": [],
            "flags3_active": [],
            "is_valid_unit": True,
            "health_issues": [],
            "status_flags": []
        }
        
        # Verifica flags1
        for mask, name in HumanReadableDecoder.INVALID_FLAGS1.items():
            if flags1 & mask:
                result["flags1_active"].append(name)
                result["status_flags"].append(name)
                result["is_valid_unit"] = False
        
        # Check flags2 (invalid status flags)
        for mask, name in HumanReadableDecoder.INVALID_FLAGS2.items():
            if flags2 & mask:
                result["flags2_active"].append(name)
                # Separate health issues from invalid status
                if mask == 0x00004000:  # gutted
                    result["health_issues"].append(name)
                else:
                    result["status_flags"].append(name)
                    
                if mask in [0x00000080, 0x00040000, 0x00080000, 0x00400000, 0x00800000]:
                    result["is_valid_unit"] = False
        
        # Check vision flags (INVERTED logic - based on C++ unithealth.cpp)
        # In C++: add_info(eHealth::HI_VISION, !(m_dwarf->get_flag2() & 0x02000000), ...)
        # If bit 0x02000000 is CLEAR (NOT set) = completely blind
        if not (flags2 & 0x02000000):
            result["health_issues"].append("completely_blind")
            result["flags2_active"].append("completely_blind")
        
        # If bit 0x04000000 is SET = vision impaired
        if flags2 & 0x04000000:
            result["health_issues"].append("vision_impaired")
            result["flags2_active"].append("vision_impaired")
        
        # If bit 0x08000000 is SET = vision slightly impaired  
        if flags2 & 0x08000000:
            result["health_issues"].append("vision_slightly_impaired")
            result["flags2_active"].append("vision_slightly_impaired")
        
        # Verifica flags3
        for mask, name in HumanReadableDecoder.INVALID_FLAGS3.items():
            if flags3 & mask:
                result["flags3_active"].append(name)
                result["status_flags"].append(name)
                result["is_valid_unit"] = False
        
        return result
    
    @staticmethod
    def interpret_body_size(body_size: int) -> Dict[str, Any]:
        """Interpreta o tamanho do corpo"""
        # Multiplica por 10 para volume real
        volume_cm3 = body_size * 10
        volume_liters = volume_cm3 / 1000.0
        
        # Age categories
        if body_size < 3500:
            category = "baby"
            age_group = "baby"
        elif body_size < 5000:
            category = "child"
            age_group = "child"
        elif body_size < 6500:
            category = "adolescent"
            age_group = "adolescent"
        else:
            category = "adult"
            age_group = "adult"
        
        return {
            "raw_value": body_size,
            "volume_cm3": volume_cm3,
            "volume_liters": round(volume_liters, 3),
            "category": category,
            "age_group": age_group,
            "display_text": f"{volume_cm3:,} cm³ ({volume_liters:.2f} L) - {age_group}"
        }
    
    @staticmethod
    def analyze_blood_level(blood_level: int, blood_max: int = 6000) -> Dict[str, Any]:
        """Analisa o nível de sangue"""
        if blood_max == 0:
            blood_max = 6000  # fallback para valor padrão
            
        percentage = (blood_level / blood_max) * 100
        
        if percentage >= 75:
            status = "normal"
            severity = 0
            severity_name = "none"
        elif percentage >= 50:
            status = "mild_loss"
            severity = 1
            severity_name = "mild"
        elif percentage >= 25:
            status = "severe_loss"
            severity = 2
            severity_name = "severe"
        else:
            status = "critical_loss"
            severity = 3
            severity_name = "critical"
        
        return {
            "current": blood_level,
            "max": blood_max,
            "percentage": round(percentage, 1),
            "status": status,
            "severity": severity,
            "severity_name": severity_name,
            "critical": percentage <= 50,
            "display_text": f"{blood_level}/{blood_max} ({percentage:.1f}%) - {status}"
        }
    
    @staticmethod
    def validate_hist_id(hist_id: int) -> Dict[str, Any]:
        """Valida e interpreta o hist_id"""
        if hist_id < 0:
            return {
                "valid": False,
                "has_history": False,
                "id": hist_id,
                "description": "Creature without historical importance",
                "display_text": "N/A (no history)"
            }
        
        return {
            "valid": True,
            "has_history": True,
            "id": hist_id,
            "description": f"Figura histórica #{hist_id}",
            "display_text": f"Historical Figure #{hist_id:,}"
        }
    
    @staticmethod
    def decode_squad_info(squad_id: int, squad_position: int) -> Dict[str, Any]:
        """Decodifica informações de esquadrão"""
        if squad_id == -1:
            return {
                "has_squad": False,
                "squad_id": -1,
                "position": -1,
                "status": "civilian",
                "display_text": "Civilian (no squad)"
            }
        
        position_names = [
            "Leader", "Second", "Third", "Fourth", "Fifth",
            "Sixth", "Seventh", "Eighth", "Ninth", "Tenth"
        ]
        
        position_name = position_names[squad_position] if 0 <= squad_position < len(position_names) else f"Position {squad_position}"
        
        return {
            "has_squad": True,
            "squad_id": squad_id,
            "position": squad_position,
            "position_name": position_name,
            "status": "military",
            "display_text": f"Squad #{squad_id} - {position_name}"
        }
    
    @staticmethod
    def decode_pet_owner(pet_owner_id: int) -> Dict[str, Any]:
        """Decodifica informação de dono de pet"""
        if pet_owner_id == -1:
            return {
                "is_pet": False,
                "owner_id": -1,
                "display_text": "Not a pet"
            }
        
        return {
            "is_pet": True,
            "owner_id": pet_owner_id,
            "display_text": f"Pet owned by unit #{pet_owner_id}"
        }


class EquipmentDecoder:
    """Decodes equipment-related numeric fields into human-readable information"""
    
    # ITEM_TYPE enum from src/global_enums.h (lines 60-170)
    ITEM_TYPES = {
        -1: "NONE",
        0: "BAR", 1: "SMALLGEM", 2: "BLOCKS", 3: "ROUGH", 4: "BOULDER",
        5: "WOOD", 6: "DOOR", 7: "FLOODGATE", 8: "BED", 9: "CHAIR",
        10: "CHAIN", 11: "FLASK", 12: "GOBLET", 13: "INSTRUMENT", 14: "TOY",
        15: "WINDOW", 16: "CAGE", 17: "BARREL", 18: "BUCKET", 19: "ANIMALTRAP",
        20: "TABLE", 21: "COFFIN", 22: "STATUE", 23: "CORPSE", 24: "WEAPON",
        25: "ARMOR", 26: "SHOES", 27: "SHIELD", 28: "HELM", 29: "GLOVES",
        30: "BOX", 31: "BAG", 32: "BIN", 33: "ARMORSTAND", 34: "WEAPONRACK",
        35: "CABINET", 36: "FIGURINE", 37: "AMULET", 38: "SCEPTER", 39: "AMMO",
        40: "CROWN", 41: "RING", 42: "EARRING", 43: "BRACELET", 44: "GEM",
        45: "ANVIL", 46: "CORPSEPIECE", 47: "REMAINS", 48: "MEAT", 49: "FISH",
        50: "FISH_RAW", 51: "VERMIN", 52: "IS_PET", 53: "SEEDS", 54: "PLANT",
        55: "SKIN_TANNED", 56: "LEAVES_FRUIT", 57: "THREAD", 58: "CLOTH", 59: "TOTEM",
        60: "PANTS", 61: "BACKPACK", 62: "QUIVER", 63: "CATAPULTPARTS", 64: "BALLISTAPARTS",
        65: "SIEGEAMMO", 66: "BALLISTAARROWHEAD", 67: "TRAPPARTS", 68: "TRAPCOMP", 69: "DRINK",
        70: "POWDER_MISC", 71: "CHEESE", 72: "FOOD", 73: "LIQUID_MISC", 74: "COIN",
        75: "GLOB", 76: "ROCK", 77: "PIPE_SECTION", 78: "HATCH_COVER", 79: "GRATE",
        80: "QUERN", 81: "MILLSTONE", 82: "SPLINT", 83: "CRUTCH", 84: "TRACTION_BENCH",
        85: "ORTHOPEDIC_CAST", 86: "TOOL", 87: "SLAB", 88: "EGG", 89: "BOOK",
        90: "SHEET"
    }
    
    # Quality levels from src/item.cpp get_quality_symbol() (lines 200-300)
    QUALITY_LEVELS = {
        -1: {"name": "none", "symbol": "", "description": "No quality"},
        0: {"name": "normal", "symbol": "", "description": "Normal quality"},
        1: {"name": "well-crafted", "symbol": "-", "description": "Well-crafted"},
        2: {"name": "finely-crafted", "symbol": "+", "description": "Finely-crafted"},
        3: {"name": "superior", "symbol": "*", "description": "Superior quality"},
        4: {"name": "exceptional", "symbol": "≡", "description": "Exceptional quality"},
        5: {"name": "masterwork", "symbol": "☼", "description": "Masterwork"},
        6: {"name": "artifact", "symbol": "!", "description": "Artifact (unique legendary item)"}
    }
    
    # Wear levels from src/item.cpp build_display_name()
    WEAR_LEVELS = {
        0: {"name": "new", "symbol": "", "description": "New condition", "percentage": 100},
        1: {"name": "worn", "symbol": "x", "description": "Worn", "percentage": 66},
        2: {"name": "threadbare", "symbol": "X", "description": "Threadbare", "percentage": 33},
        3: {"name": "tattered", "symbol": "XX", "description": "Tattered (nearly destroyed)", "percentage": 10}
    }
    
    @staticmethod
    def decode_item_type(item_type: int) -> Dict[str, Any]:
        """Decodes item type from ITEM_TYPE enum"""
        if item_type in EquipmentDecoder.ITEM_TYPES:
            type_name = EquipmentDecoder.ITEM_TYPES[item_type]
            return {
                "valid": True,
                "type_id": item_type,
                "type_name": type_name,
                "display_text": type_name.replace("_", " ").title()
            }
        
        # Unknown or invalid item type
        return {
            "valid": False,
            "type_id": item_type,
            "type_name": "UNKNOWN",
            "display_text": f"Unknown Type ({item_type})"
        }
    
    @staticmethod
    def decode_quality(quality: int) -> Dict[str, Any]:
        """Decodes quality level (0-6 scale with -1 for none)"""
        # Check for sentinel value (might appear as 4294967295 or similar large number)
        if quality == 4294967295 or quality > 100:
            quality = -1
        
        if quality in EquipmentDecoder.QUALITY_LEVELS:
            q_info = EquipmentDecoder.QUALITY_LEVELS[quality]
            return {
                "valid": True,
                "level": quality,
                "name": q_info["name"],
                "symbol": q_info["symbol"],
                "description": q_info["description"],
                "display_text": f"{q_info['symbol']}{q_info['name']}{q_info['symbol']}" if q_info["symbol"] else q_info["name"]
            }
        
        return {
            "valid": False,
            "level": quality,
            "name": "invalid",
            "symbol": "?",
            "description": f"Invalid quality level: {quality}",
            "display_text": f"Invalid Quality ({quality})"
        }
    
    @staticmethod
    def decode_wear(wear: int) -> Dict[str, Any]:
        """Decodes wear level (0-3 scale)"""
        # Check for sentinel value
        if wear == 4294967295 or wear > 100:
            wear = 0  # Default to new condition
        
        if wear in EquipmentDecoder.WEAR_LEVELS:
            w_info = EquipmentDecoder.WEAR_LEVELS[wear]
            return {
                "valid": True,
                "level": wear,
                "name": w_info["name"],
                "symbol": w_info["symbol"],
                "description": w_info["description"],
                "condition_percentage": w_info["percentage"],
                "display_text": f"{w_info['symbol']} {w_info['name']} ({w_info['percentage']}%)" if w_info["symbol"] else f"{w_info['name']} ({w_info['percentage']}%)"
            }
        
        return {
            "valid": False,
            "level": wear,
            "name": "invalid",
            "symbol": "?",
            "description": f"Invalid wear level: {wear}",
            "condition_percentage": 0,
            "display_text": f"Invalid Wear ({wear})"
        }
    
    @staticmethod
    def decode_equipment_item(item: Dict[str, Any]) -> Dict[str, Any]:
        """Decodes all equipment fields for a single item"""
        decoded = {}
        
        # Decode item type
        if "item_type" in item:
            decoded["item_type"] = EquipmentDecoder.decode_item_type(item["item_type"])
        
        # Decode quality
        if "quality" in item:
            decoded["quality"] = EquipmentDecoder.decode_quality(item["quality"])
        
        # Decode wear
        if "wear" in item:
            decoded["wear"] = EquipmentDecoder.decode_wear(item["wear"])
        
        # Keep original values for reference
        decoded["raw_values"] = {
            "item_id": item.get("item_id", -1),
            "item_type": item.get("item_type", -1),
            "material_type": item.get("material_type", -1),
            "material_index": item.get("material_index", -1),
            "quality": item.get("quality", -1),
            "wear": item.get("wear", 0)
        }
        
        return decoded


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
            
            # Converter valores sentinela (4294967295 = 0xFFFFFFFF) para -1 (mais legível)
            UINT32_MAX = 4294967295
            squad_id_raw = self.memory_reader.read_int32(address + offsets.get('squad_id', 0))
            dwarf.squad_id = -1 if squad_id_raw == UINT32_MAX else squad_id_raw
            
            squad_position_raw = self.memory_reader.read_int32(address + offsets.get('squad_position', 0))
            dwarf.squad_position = -1 if squad_position_raw == UINT32_MAX else squad_position_raw
            
            pet_owner_id_raw = self.memory_reader.read_int32(address + offsets.get('pet_owner_id', 0))
            dwarf.pet_owner_id = -1 if pet_owner_id_raw == UINT32_MAX else pet_owner_id_raw
            
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
            UINT32_MAX = 4294967295
            
            wounds = []
            for wound_addr in wound_pointers[:20]:  # Limite de 20 ferimentos
                pain_raw = self.memory_reader.read_int32(wound_addr + wound_offsets.get('pain', 0))
                
                wound = Wound(
                    id=self.memory_reader.read_int32(wound_addr + wound_offsets.get('id', 0)),
                    body_part=self.memory_reader.read_int32(wound_addr + wound_offsets.get('parts', 0)),
                    layer=self.memory_reader.read_int32(wound_addr + wound_offsets.get('layer', 0)),
                    bleeding=self.memory_reader.read_int32(wound_addr + wound_offsets.get('bleeding', 0)),
                    pain=-1 if pain_raw == UINT32_MAX else pain_raw,
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
            
    def _read_item_type(self, item_addr: int) -> int:
        """
        Read item type from vtable (C++ polymorphism)
        Based on src/item.cpp line 119:
            VIRTADDR item_vtable = m_df->read_addr(m_addr);
            m_iType = static_cast<ITEM_TYPE>(m_df->read_int(
                m_df->read_addr(item_vtable) + m_df->VM_TYPE_OFFSET()));
        
        VM_TYPE_OFFSET values from dfinstance.h:
        - Windows default: 0x1
        - Linux: 0x5
        - OSX: varies
        """
        try:
            # Step 1: Read vtable pointer at item address
            vtable_addr = self.memory_reader.read_pointer(item_addr, self.pointer_size)
            
            if vtable_addr == 0 or vtable_addr < 0x1000:  # Invalid pointer
                return -1  # NONE
            
            # Step 2: Read type info pointer from vtable + VM_TYPE_OFFSET
            # Try Windows default: 0x1 (from dfinstance.h)
            vm_type_offset = 0x1
            type_info_addr = self.memory_reader.read_pointer(vtable_addr, self.pointer_size)
            
            if type_info_addr == 0 or type_info_addr < 0x1000:
                return -1
            
            # Step 3: Read actual type ID (int32) at type_info_addr + offset
            item_type = self.memory_reader.read_int32(type_info_addr + vm_type_offset)
            
            # Validate range (ITEM_TYPE enum is 0-90 approximately)
            if item_type < -1 or item_type > 100:
                # Try alternative: read directly from vtable structure
                # Some DF versions may store type differently
                for test_offset in [0, 4, 8, 12, 16, 20]:
                    test_type = self.memory_reader.read_int32(item_addr + test_offset)
                    if 0 <= test_type <= 90:
                        logger.debug(f"Found item_type {test_type} at offset {test_offset:x} for addr {item_addr:x}")
                        return test_type
                return -1
                
            return item_type
        except Exception as e:
            logger.debug(f"Failed to read item type at {item_addr:x}: {e}")
            return -1  # NONE
    
    def _read_equipment(self, inventory_addr: int) -> List[Equipment]:
        """
        Lê equipamentos/inventário
        Baseado em src/dwarf.cpp read_inventory() linha 1622:
            foreach(VIRTADDR inventory_item_addr, m_df->enumerate_vector(..., "inventory")){
                VIRTADDR item_ptr = m_df->read_addr(inventory_item_addr);
                Item *i = new Item(m_df,item_ptr,this);
        
        O vetor inventory contém inventory_item structures, não items diretos!
        """
        try:
            # Read inventory_item vector (NOT direct item pointers!)
            inventory_items = self.memory_reader.read_vector(inventory_addr, self.pointer_size)
            item_offsets = self.layout.offsets.get('item', {})
            SHORT_MAX = 65535  # 0xFFFF - sentinel value for 16-bit fields
            
            equipment = []
            for inventory_item_addr in inventory_items[:50]:  # Limite de 50 itens
                # CRITICAL FIX: Read item pointer from inventory_item structure
                # The inventory_item is a wrapper, actual item is at offset 0x0000
                item_addr = self.memory_reader.read_pointer(inventory_item_addr, self.pointer_size)
                
                if item_addr == 0 or item_addr < 0x1000:  # Invalid pointer
                    continue
                
                # Now read from the ACTUAL item address
                quality_raw = self.memory_reader.read_int16(item_addr + item_offsets.get('quality', 0))
                wear_raw = self.memory_reader.read_int16(item_addr + item_offsets.get('wear', 0))
                mat_type_raw = self.memory_reader.read_int16(item_addr + item_offsets.get('mat_type', 0))
                
                # Read item type via vtable (now should work correctly!)
                item_type = self._read_item_type(item_addr)
                
                item = Equipment(
                    item_id=self.memory_reader.read_int32(item_addr + item_offsets.get('id', 0)),
                    item_type=item_type,
                    material_type=mat_type_raw,
                    material_index=self.memory_reader.read_int32(item_addr + item_offsets.get('mat_index', 0)),
                    quality=-1 if quality_raw == SHORT_MAX else quality_raw,
                    wear=-1 if wear_raw == SHORT_MAX else wear_raw
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
                'dwarves': [dwarf.to_dict(human_readable=decode_data) for dwarf in self.dwarves]
            }
            
            # Aplicar decodificação adicional se solicitado
            if decode_data:
                logger.info("Aplicando decodificação adicional aos dados...")
                try:
                    # Importar decodificador externo se disponível
                    tools_path = Path(__file__).parent.parent / "tools"
                    sys.path.insert(0, str(tools_path))
                    from complete_decoder import DwarfDataDecoder
                    
                    decoder = DwarfDataDecoder()
                    
                    for i, dwarf_dict in enumerate(data['dwarves']):
                        if i % 50 == 0:
                            logger.info(f"Decodificando dwarf {i+1}/{len(data['dwarves'])}")
                        # Mesclar decodificação externa com a interna (evitar referências circulares)
                        try:
                            external_decoded = decoder.decode_dwarf(dict(dwarf_dict))
                            if '_decoded' in dwarf_dict and '_decoded' in external_decoded:
                                # Copiar apenas campos específicos para evitar circular reference
                                for key in ['profession_decoded', 'race_decoded', 'caste_decoded']:
                                    if key in external_decoded['_decoded']:
                                        dwarf_dict['_decoded'][key] = external_decoded['_decoded'][key]
                        except Exception as e:
                            logger.debug(f"Erro ao decodificar dwarf {i}: {e}")
                    
                    data['metadata']['decoder_version'] = '2.0-human-readable'
                    logger.info("Decodificação completa aplicada com sucesso")
                    
                except ImportError:
                    logger.info("Decodificador externo não encontrado, usando apenas decodificação interna")
                    data['metadata']['decoder_version'] = '2.0-internal-only'
                except Exception as e:
                    logger.warning(f"Erro na decodificação externa: {e}")
                    data['metadata']['decode_warning'] = str(e)
                    data['metadata']['decoder_version'] = '2.0-internal-only'
            
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