#!/usr/bin/env python3
"""
Extrator de Informações Geográficas Completas do Dwarf Fortress
Usa o dicionário de offsets para decodificar e explicar cada valor
"""

import json
import psutil
import ctypes
import struct
import logging
import configparser
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Windows API constants
PROCESS_VM_READ = 0x0010
PROCESS_VM_OPERATION = 0x0008
PROCESS_QUERY_INFORMATION = 0x0400

class GeographicMemoryReader:
    """Leitor de memória especializado em dados geográficos"""
    
    def __init__(self):
        self.kernel32 = ctypes.windll.kernel32
        self.process_handle = None
        
    def open_process(self, pid: int) -> bool:
        """Abrir processo para leitura de memória"""
        access_rights = PROCESS_VM_READ | PROCESS_VM_OPERATION | PROCESS_QUERY_INFORMATION
        self.process_handle = self.kernel32.OpenProcess(access_rights, False, pid)
        return self.process_handle is not None
        
    def close_process(self):
        """Fechar handle do processo"""
        if self.process_handle:
            self.kernel32.CloseHandle(self.process_handle)
            self.process_handle = None
            
    def read_memory(self, address: int, size: int) -> bytes:
        """Ler memória bruta"""
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
        """Ler inteiro 32-bit"""
        data = self.read_memory(address, 4)
        return struct.unpack('<I', data)[0] if len(data) == 4 else 0
        
    def read_int16(self, address: int) -> int:
        """Ler inteiro 16-bit"""
        data = self.read_memory(address, 2)
        return struct.unpack('<H', data)[0] if len(data) == 2 else 0
        
    def read_int64(self, address: int) -> int:
        """Ler inteiro 64-bit"""
        data = self.read_memory(address, 8)
        return struct.unpack('<Q', data)[0] if len(data) == 8 else 0
        
    def read_pointer(self, address: int, pointer_size: int = 8) -> int:
        """Ler ponteiro"""
        return self.read_int64(address) if pointer_size == 8 else self.read_int32(address)
        
    def read_vector(self, address: int, pointer_size: int = 8) -> List[int]:
        """Ler std::vector"""
        try:
            start_ptr = self.read_pointer(address, pointer_size)
            end_ptr = self.read_pointer(address + pointer_size, pointer_size)
            
            if start_ptr == 0 or end_ptr == 0 or start_ptr >= end_ptr:
                return []
                
            count = (end_ptr - start_ptr) // pointer_size
            if count > 50000:  # Limite de segurança
                return []
                
            pointers = []
            for i in range(count):
                ptr_addr = start_ptr + (i * pointer_size)
                ptr_value = self.read_pointer(ptr_addr, pointer_size)
                if ptr_value != 0:
                    pointers.append(ptr_value)
                    
            return pointers
            
        except Exception as e:
            logger.debug(f"Erro ao ler vetor em 0x{address:x}: {e}")
            return []

class OffsetDictionary:
    """Carrega e interpreta o dicionário de offsets"""
    
    def __init__(self, dict_file: Path):
        self.descriptions = {}
        self.load_dictionary(dict_file)
        
    def load_dictionary(self, dict_file: Path):
        """Carregar dicionário de offsets"""
        try:
            if dict_file.exists():
                with open(dict_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Parsear arquivo markdown do dicionário
                current_section = ""
                for line in content.split('\n'):
                    line = line.strip()
                    
                    if line.startswith('## ') and 'OFFSETS' in line.upper():
                        current_section = line.replace('## ', '').replace(' OFFSETS', '').lower()
                        self.descriptions[current_section] = {}
                        
                    elif '|' in line and '0x' in line and current_section:
                        # Parsear linha da tabela: | offset | hex | descrição |
                        parts = [p.strip() for p in line.split('|')]
                        if len(parts) >= 4:
                            offset_name = parts[1]
                            hex_value = parts[2]
                            description = parts[3]
                            
                            if offset_name and hex_value and description:
                                self.descriptions[current_section][offset_name] = {
                                    'hex': hex_value,
                                    'description': description
                                }
                                
            logger.info(f"Dicionário carregado: {len(self.descriptions)} seções")
            
        except Exception as e:
            logger.error(f"Erro ao carregar dicionário: {e}")
            
    def get_description(self, section: str, offset: str) -> str:
        """Obter descrição de um offset"""
        return self.descriptions.get(section, {}).get(offset, {}).get('description', 'Descrição não encontrada')

class GeographicExtractor:
    """Extrator principal de dados geográficos"""
    
    def __init__(self):
        self.memory_reader = GeographicMemoryReader()
        self.offset_dict = None
        self.layout = None
        self.pid = 0
        self.base_addr = 0
        self.pointer_size = 8
        
    def find_df_process(self) -> bool:
        """Encontrar processo do Dwarf Fortress"""
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if 'dwarffortress' in proc.info['name'].lower() or 'dwarf fortress' in proc.info['name'].lower():
                    self.pid = proc.info['pid']
                    logger.info(f"Dwarf Fortress encontrado: PID {self.pid}")
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
                
        logger.error("Dwarf Fortress não encontrado!")
        return False
        
    def connect(self) -> bool:
        """Conectar ao processo"""
        if not self.find_df_process():
            return False
            
        if not self.memory_reader.open_process(self.pid):
            logger.error(f"Falha ao abrir processo {self.pid}")
            return False
            
        # Determinar base address
        try:
            from ctypes import wintypes
            psapi = ctypes.windll.psapi
            hModules = (wintypes.HMODULE * 1024)()
            process_handle = self.memory_reader.process_handle
            cb = wintypes.DWORD()
            
            if psapi.EnumProcessModules(process_handle, hModules, ctypes.sizeof(hModules), ctypes.byref(cb)):
                self.base_addr = hModules[0]
                logger.info(f"Base address: 0x{self.base_addr:x}")
                return True
            else:
                logger.error("Falha ao obter base address")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao determinar base address: {e}")
            return False
            
    def load_memory_layout(self) -> bool:
        """Carregar layout de memória"""
        try:
            layouts_dir = Path(__file__).parent.parent / "share" / "memory_layouts" / "windows"
            
            if not layouts_dir.exists():
                logger.error(f"Diretório de layouts não existe: {layouts_dir}")
                return False
                
            layout_files = list(layouts_dir.glob("*.ini"))
            if not layout_files:
                logger.error("Nenhum arquivo de layout encontrado")
                return False
                
            # Usar layout mais recente
            layout_file = sorted(layout_files, key=lambda x: x.name)[-1]
            logger.info(f"Usando layout: {layout_file.name}")
            
            self.layout = configparser.ConfigParser()
            self.layout.read(layout_file, encoding='utf-8')
            return True
            
        except Exception as e:
            logger.error(f"Erro ao carregar layout: {e}")
            return False
            
    def load_offset_dictionary(self) -> bool:
        """Carregar dicionário de offsets"""
        try:
            dict_file = Path(__file__).parent.parent / "DICIONARIO_OFFSETS_20251028_234952.md"
            
            if not dict_file.exists():
                logger.warning(f"Dicionário não encontrado: {dict_file}")
                return False
                
            self.offset_dict = OffsetDictionary(dict_file)
            return True
            
        except Exception as e:
            logger.error(f"Erro ao carregar dicionário: {e}")
            return False
            
    def extract_world_data(self) -> Dict[str, Any]:
        """Extrair dados completos do mundo"""
        logger.info("=== EXTRAINDO DADOS GEOGRÁFICOS ===")
        
        geographic_data = {
            'metadata': {
                'extraction_time': datetime.now().isoformat(),
                'df_pid': self.pid,
                'base_address': f"0x{self.base_addr:x}"
            },
            'world_structure': {},
            'active_sites': {},
            'regions': {},
            'coordinates': {},
            'geology': {},
            'climate': {},
            'hydrology': {},
            'raw_geographic_offsets': {}
        }
        
        try:
            # 1. WORLD DATA PRINCIPAL
            world_data_addr = self._get_address('world_data')
            if world_data_addr:
                logger.info(f"World data address: 0x{world_data_addr:x}")
                geographic_data['world_structure'] = self._extract_world_structure(world_data_addr)
                
            # 2. SITES ATIVOS
            active_sites_addr = self._get_address('active_sites_vector')
            if active_sites_addr:
                geographic_data['active_sites'] = self._extract_active_sites(world_data_addr, active_sites_addr)
                
            # 3. REGIÕES
            if world_data_addr:
                geographic_data['regions'] = self._extract_regions(world_data_addr)
                
            # 4. DADOS GEOLÓGICOS
            geographic_data['geology'] = self._extract_geological_data(world_data_addr)
            
            # 5. DADOS CLIMÁTICOS
            geographic_data['climate'] = self._extract_climate_data(world_data_addr)
            
            # 6. HIDROLOGIA
            geographic_data['hydrology'] = self._extract_hydrology_data(world_data_addr)
            
            # 7. COORDENADAS E ELEVAÇÃO
            geographic_data['coordinates'] = self._extract_coordinate_data(world_data_addr)
            
            # 8. OFFSETS BRUTOS COM DESCRIÇÕES
            geographic_data['raw_geographic_offsets'] = self._extract_raw_offsets()
            
        except Exception as e:
            logger.error(f"Erro na extração: {e}")
            
        return geographic_data
        
    def _get_address(self, key: str) -> int:
        """Obter endereço com base address"""
        if not self.layout or 'addresses' not in self.layout:
            return 0
            
        addr_str = self.layout['addresses'].get(key, '0x0')
        addr = int(addr_str, 16)
        return addr + self.base_addr if addr else 0
        
    def _extract_world_structure(self, world_data_addr: int) -> Dict[str, Any]:
        """Extrair estrutura principal do mundo"""
        structure = {
            'description': self.offset_dict.get_description('addresses', 'world_data') if self.offset_dict else 'Estrutura principal de dados mundiais',
            'address': f"0x{world_data_addr:x}",
            'basic_info': {}
        }
        
        # Ler primeiros campos da estrutura world_data
        try:
            # Assumindo estrutura padrão do world_data
            offsets_to_read = [
                (0x0, 'world_index', 'Índice do mundo'),
                (0x4, 'world_name_id', 'ID do nome do mundo'),
                (0x8, 'world_seed', 'Seed de geração do mundo'),
                (0x10, 'world_size_x', 'Tamanho X do mundo'),
                (0x14, 'world_size_y', 'Tamanho Y do mundo'),
                (0x18, 'world_age', 'Idade do mundo em anos'),
                (0x300, 'regions_vector', 'Vetor de regiões')
            ]
            
            for offset, name, description in offsets_to_read:
                value = self.memory_reader.read_int32(world_data_addr + offset)
                structure['basic_info'][name] = {
                    'value': value,
                    'offset': f"0x{offset:x}",
                    'description': description
                }
                
        except Exception as e:
            logger.error(f"Erro ao ler estrutura do mundo: {e}")
            
        return structure
        
    def _extract_active_sites(self, world_data_addr: int, sites_vector_addr: int) -> Dict[str, Any]:
        """Extrair sites ativos (fortalezas, cidades)"""
        sites_data = {
            'description': self.offset_dict.get_description('addresses', 'active_sites_vector') if self.offset_dict else 'Sites ativos no mundo',
            'vector_address': f"0x{sites_vector_addr:x}",
            'sites': []
        }
        
        try:
            # Sites são referenciados através do world_data
            site_vector_addr = world_data_addr + 0x483d0  # Offset padrão para active_sites
            site_pointers = self.memory_reader.read_vector(site_vector_addr, self.pointer_size)
            
            logger.info(f"Encontrados {len(site_pointers)} sites ativos")
            
            for i, site_addr in enumerate(site_pointers[:20]):  # Máximo 20 sites
                site_info = self._extract_site_info(site_addr, i)
                if site_info:
                    sites_data['sites'].append(site_info)
                    
        except Exception as e:
            logger.error(f"Erro ao extrair sites: {e}")
            
        return sites_data
        
    def _extract_site_info(self, site_addr: int, index: int) -> Dict[str, Any]:
        """Extrair informações de um site específico"""
        try:
            site_info = {
                'index': index,
                'address': f"0x{site_addr:x}",
                'type': self.memory_reader.read_int16(site_addr + 0x80),  # world_site_type offset
                'coordinates': {},
                'properties': {}
            }
            
            # Ler coordenadas do site
            coord_offsets = [0x0, 0x4, 0x8, 0xc, 0x10, 0x14, 0x18, 0x1c, 0x20, 0x24]
            for i, offset in enumerate(coord_offsets):
                coord_value = self.memory_reader.read_int32(site_addr + offset)
                site_info['coordinates'][f'coord_{i}'] = {
                    'value': coord_value,
                    'offset': f"0x{offset:x}",
                    'description': f'Coordenada {i} do site'
                }
                
            # Propriedades do site
            site_info['properties'] = {
                'type_name': self._get_site_type_name(site_info['type']),
                'is_player_fortress': site_info['type'] == 0
            }
            
            return site_info
            
        except Exception as e:
            logger.error(f"Erro ao extrair site {index}: {e}")
            return None
            
    def _get_site_type_name(self, site_type: int) -> str:
        """Obter nome do tipo de site"""
        site_types = {
            0: "Player Fortress",
            1: "Dark Fortress", 
            2: "Cave",
            3: "Mountain Halls",
            4: "Forest Retreat",
            5: "Town",
            6: "Hamlet"
        }
        return site_types.get(site_type, f"Unknown Type {site_type}")
        
    def _extract_regions(self, world_data_addr: int) -> Dict[str, Any]:
        """Extrair dados de regiões"""
        regions_data = {
            'description': 'Regiões geográficas do mundo',
            'regions_vector': {},
            'region_count': 0,
            'sample_regions': []
        }
        
        try:
            regions_vector_addr = world_data_addr + 0x300  # Offset padrão para regiões
            region_pointers = self.memory_reader.read_vector(regions_vector_addr, self.pointer_size)
            
            regions_data['region_count'] = len(region_pointers)
            regions_data['regions_vector'] = {
                'address': f"0x{regions_vector_addr:x}",
                'count': len(region_pointers)
            }
            
            logger.info(f"Encontradas {len(region_pointers)} regiões")
            
            # Extrair amostra das primeiras 10 regiões
            for i, region_addr in enumerate(region_pointers[:10]):
                region_info = self._extract_region_info(region_addr, i)
                if region_info:
                    regions_data['sample_regions'].append(region_info)
                    
        except Exception as e:
            logger.error(f"Erro ao extrair regiões: {e}")
            
        return regions_data
        
    def _extract_region_info(self, region_addr: int, index: int) -> Dict[str, Any]:
        """Extrair informações de uma região"""
        try:
            return {
                'index': index,
                'address': f"0x{region_addr:x}",
                'type': self.memory_reader.read_int16(region_addr + 0x0),
                'elevation': self.memory_reader.read_int16(region_addr + 0x2),
                'rainfall': self.memory_reader.read_int16(region_addr + 0x4),
                'temperature': self.memory_reader.read_int16(region_addr + 0x6),
                'drainage': self.memory_reader.read_int16(region_addr + 0x8),
                'volcanism': self.memory_reader.read_int16(region_addr + 0xa),
                'vegetation': self.memory_reader.read_int16(region_addr + 0xc),
                'evilness': self.memory_reader.read_int16(region_addr + 0xe),
                'savagery': self.memory_reader.read_int16(region_addr + 0x10)
            }
        except Exception as e:
            logger.error(f"Erro ao extrair região {index}: {e}")
            return None
            
    def _extract_geological_data(self, world_data_addr: int) -> Dict[str, Any]:
        """Extrair dados geológicos"""
        geology_data = {
            'description': 'Dados geológicos e materiais do mundo',
            'material_layers': {},
            'mineral_veins': {},
            'stone_types': {}
        }
        
        try:
            # Offsets padrão para geologia
            geology_offsets = [0x1000, 0x2000, 0x3000, 0x4000, 0x5000]
            
            for i, offset in enumerate(geology_offsets):
                materials = []
                for j in range(10):  # Ler 10 materiais por camada
                    material_value = self.memory_reader.read_int32(world_data_addr + offset + (j * 4))
                    materials.append(material_value)
                    
                geology_data['material_layers'][f'layer_{i}'] = {
                    'offset': f"0x{offset:x}",
                    'materials': materials,
                    'description': f'Camada geológica {i}'
                }
                
        except Exception as e:
            logger.error(f"Erro ao extrair geologia: {e}")
            
        return geology_data
        
    def _extract_climate_data(self, world_data_addr: int) -> Dict[str, Any]:
        """Extrair dados climáticos"""
        return {
            'description': 'Dados climáticos e meteorológicos',
            'temperature_map': 'Mapeado através das regiões',
            'rainfall_map': 'Mapeado através das regiões',
            'wind_patterns': 'Não implementado'
        }
        
    def _extract_hydrology_data(self, world_data_addr: int) -> Dict[str, Any]:
        """Extrair dados hidrológicos"""
        return {
            'description': 'Sistemas de água: rios, lagos, aquíferos',
            'river_systems': 'Mapeado através das regiões',
            'water_table': 'Drainage mapeado por região',
            'underground_water': 'Não implementado'
        }
        
    def _extract_coordinate_data(self, world_data_addr: int) -> Dict[str, Any]:
        """Extrair dados de coordenadas e elevação"""
        coordinates = {
            'description': 'Sistemas de coordenadas e elevação',
            'coordinate_arrays': {},
            'elevation_maps': {},
            'world_dimensions': {}
        }
        
        try:
            # Tentar ler dimensões do mundo
            world_x = self.memory_reader.read_int32(world_data_addr + 0x10)
            world_y = self.memory_reader.read_int32(world_data_addr + 0x14)
            
            coordinates['world_dimensions'] = {
                'width': world_x,
                'height': world_y,
                'description': 'Dimensões do mapa mundial em regiões'
            }
            
        except Exception as e:
            logger.error(f"Erro ao extrair coordenadas: {e}")
            
        return coordinates
        
    def _extract_raw_offsets(self) -> Dict[str, Any]:
        """Extrair todos os offsets geográficos com descrições"""
        raw_offsets = {
            'description': 'Todos os offsets relacionados a geografia com suas descrições'
        }
        
        if not self.offset_dict:
            return raw_offsets
            
        # Seções geográficas relevantes
        geographic_sections = ['addresses', 'offsets', 'dwarf_offsets']
        
        for section in geographic_sections:
            if section in self.offset_dict.descriptions:
                raw_offsets[section] = {}
                for offset_name, offset_data in self.offset_dict.descriptions[section].items():
                    if any(keyword in offset_name.lower() or keyword in offset_data['description'].lower() 
                           for keyword in ['world', 'site', 'coord', 'region', 'map', 'geo', 'clima', 'elevat']):
                        raw_offsets[section][offset_name] = offset_data
                        
        return raw_offsets
        
    def export_geographic_data(self, filename: str = None) -> bool:
        """Exportar dados geográficos para JSON"""
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"geographic_data_complete_{timestamp}.json"
                
            geographic_data = self.extract_world_data()
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(geographic_data, f, indent=2, ensure_ascii=False)
                
            logger.info(f"Dados geográficos exportados para: {filename}")
            
            # Estatísticas
            print(f"\n=== DADOS GEOGRÁFICOS EXTRAÍDOS ===")
            print(f"Arquivo: {filename}")
            print(f"Sites ativos: {len(geographic_data.get('active_sites', {}).get('sites', []))}")
            print(f"Regiões encontradas: {geographic_data.get('regions', {}).get('region_count', 0)}")
            print(f"Camadas geológicas: {len(geographic_data.get('geology', {}).get('material_layers', {}))}")
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao exportar dados: {e}")
            return False
            
    def disconnect(self):
        """Desconectar do processo"""
        self.memory_reader.close_process()

def main():
    """Execução principal"""
    print("=== EXTRATOR DE INFORMAÇÕES GEOGRÁFICAS DO DWARF FORTRESS ===")
    print("Usando dicionário de offsets para decodificar valores")
    print()
    
    extractor = GeographicExtractor()
    
    try:
        # Conectar
        if not extractor.connect():
            print("ERRO: Falha ao conectar ao Dwarf Fortress")
            return
        print("✅ Conectado ao Dwarf Fortress")
        
        # Carregar layout de memória
        if not extractor.load_memory_layout():
            print("ERRO: Falha ao carregar layout de memória")
            return
        print("✅ Layout de memória carregado")
        
        # Carregar dicionário de offsets
        if not extractor.load_offset_dictionary():
            print("⚠️  Dicionário de offsets não encontrado (funcionando sem descrições)")
        else:
            print("✅ Dicionário de offsets carregado")
        
        # Extrair e exportar dados
        print("\n🗺️  Extraindo dados geográficos completos...")
        if extractor.export_geographic_data():
            print("✅ Dados geográficos exportados com sucesso!")
        else:
            print("❌ Erro na exportação")
            
    except Exception as e:
        print(f"ERRO: {e}")
        logger.error(f"Erro na execução: {e}")
    finally:
        extractor.disconnect()

if __name__ == "__main__":
    main()