#!/usr/bin/env python3
"""
World Data Explorer - Análise Completa da Estrutura world_data=0x142453de8
Explora todas as estruturas e sub-estruturas do world_data no Dwarf Fortress
"""

import os
import sys
from pathlib import Path
import logging
import struct
from typing import Dict, List, Optional, Tuple, Any
import json
from datetime import datetime

# Adicionar o caminho do complete_dwarf_reader
sys.path.insert(0, str(Path(__file__).parent))
from complete_dwarf_reader import CompleteDFInstance, MemoryLayout

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('world_data_explorer.log')
    ]
)
logger = logging.getLogger(__name__)

class WorldDataExplorer:
    """Explorador da estrutura world_data do Dwarf Fortress"""
    
    def __init__(self):
        self.dwarf_reader = CompleteDFInstance()
        self.layout = None
        self.base_addr = 0
        self.world_data_addr = 0
        
        # Endereços conhecidos da estrutura world_data
        self.known_fields = {
            # Offset +0x000483b0 - active_sites_vector
            'active_sites_vector': 0x000483b0,
            # Outros offsets potenciais baseados na análise
            'site_list': 0x0000,  # Base do world_data
            'world_map': 0x1000,  # Provável localização do mapa
            'regions': 0x2000,    # Regiões do mundo
            'geology': 0x3000,    # Dados geológicos
            'hydrology': 0x4000,  # Rios e água
            'temperature': 0x5000, # Dados de temperatura
            'rainfall': 0x6000,   # Dados de chuva
        }
        
    def connect_to_df(self) -> bool:
        """Conecta ao Dwarf Fortress"""
        try:
            # Usar o método connect() do CompletelyDwarfData que já faz tudo
            if not self.dwarf_reader.connect():
                logger.error("Falha ao conectar ao Dwarf Fortress")
                return False
                
            # Carregar layout de memória  
            current_dir = Path(__file__).parent
            layout_path = current_dir.parent.parent / 'share' / 'memory_layouts' / 'windows' / 'v0.52.05-steam_win64.ini'
            
            self.layout = MemoryLayout(layout_path)
            if not self.layout.addresses:
                logger.error("Falha ao carregar layout de memória")
                return False
                
            # Obter endereço base do processo
            self.base_addr = self.dwarf_reader.base_addr
            
            # Calcular endereço do world_data
            world_data_offset = self.layout.get_address('world_data')
            if not world_data_offset:
                logger.error("world_data não encontrado no layout")
                return False
                
            self.world_data_addr = self.base_addr + world_data_offset
            
            logger.info(f"Conectado ao DF. PID: {self.dwarf_reader.pid}")
            logger.info(f"Base address: 0x{self.base_addr:x}")
            logger.info(f"World data address: 0x{self.world_data_addr:x}")
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao conectar: {e}")
            return False
    
    def read_world_data_pointer(self) -> int:
        """Lê o ponteiro real para world_data"""
        try:
            # world_data é um ponteiro, então lemos o endereço que ele aponta
            pointer = self.dwarf_reader.memory_reader.read_pointer(self.world_data_addr, 8)
            logger.info(f"World data pointer: 0x{pointer:x}")
            return pointer
        except Exception as e:
            logger.error(f"Erro ao ler ponteiro world_data: {e}")
            return 0
    
    def explore_active_sites(self, world_data_ptr: int) -> Dict:
        """Explora o vetor de sites ativos"""
        logger.info("Explorando active sites...")
        
        sites_data = {
            'vector_address': 0,
            'site_count': 0,
            'sites': []
        }
        
        try:
            # Calcular endereço do active_sites_vector
            sites_vector_addr = world_data_ptr + self.known_fields['active_sites_vector']
            sites_data['vector_address'] = sites_vector_addr
            
            # Ler o vetor (start, end pointers)
            start_ptr = self.dwarf_reader.memory_reader.read_pointer(sites_vector_addr, 8)
            end_ptr = self.dwarf_reader.memory_reader.read_pointer(sites_vector_addr + 8, 8)
            
            if start_ptr and end_ptr and end_ptr > start_ptr:
                site_count = (end_ptr - start_ptr) // 8  # Cada ponteiro é 8 bytes
                sites_data['site_count'] = site_count
                
                logger.info(f"Active sites vector: 0x{sites_vector_addr:x}")
                logger.info(f"Sites encontrados: {site_count}")
                
                # Ler cada site
                for i in range(min(site_count, 10)):  # Máximo 10 sites
                    site_ptr_addr = start_ptr + (i * 8)
                    site_addr = self.dwarf_reader.memory_reader.read_pointer(site_ptr_addr, 8)
                    
                    if site_addr:
                        site_info = self.analyze_site_structure(site_addr, i)
                        sites_data['sites'].append(site_info)
                        
        except Exception as e:
            logger.error(f"Erro ao explorar active sites: {e}")
            
        return sites_data
    
    def analyze_site_structure(self, site_addr: int, index: int) -> Dict:
        """Analisa a estrutura de um site específico"""
        site_info = {
            'index': index,
            'address': hex(site_addr),
            'type': 'unknown',
            'name': '',
            'coordinates': {},
            'raw_data': {}
        }
        
        try:
            # Ler tipo do site (offset +0x80 baseado no layout)
            site_type = self.dwarf_reader.memory_reader.read_int16(site_addr + 0x80)
            site_info['type'] = site_type
            site_info['raw_data']['type'] = site_type
            
            # Se for tipo 0 (player fortress), explorar mais
            if site_type == 0:
                site_info['name'] = 'Player Fortress'
                logger.info(f"  Site {index}: Player Fortress encontrada!")
                
                # Tentar ler coordenadas do site
                coords = self.read_site_coordinates(site_addr)
                site_info['coordinates'] = coords
                
                # Ler nome da fortaleza
                fortress_name = self.read_fortress_name(site_addr)
                if fortress_name:
                    site_info['name'] = fortress_name
                    
            else:
                site_info['name'] = f'Site Type {site_type}'
                logger.info(f"  Site {index}: Tipo {site_type}")
                
            # Ler dados adicionais da estrutura
            site_info['raw_data'].update(self.read_site_raw_data(site_addr))
            
        except Exception as e:
            logger.error(f"Erro ao analisar site {index}: {e}")
            
        return site_info
    
    def read_site_coordinates(self, site_addr: int) -> Dict:
        """Lê coordenadas de um site"""
        coords = {}
        
        try:
            # Offsets típicos para coordenadas em estruturas de site
            coord_offsets = [0x04, 0x08, 0x0C, 0x10, 0x14, 0x18]
            
            for i, offset in enumerate(coord_offsets):
                value = self.dwarf_reader.memory_reader.read_int32(site_addr + offset)
                coords[f'coord_{i}'] = value
                
                # Verificar se parece coordenada válida
                if 0 <= value <= 1000:
                    coords[f'valid_coord_{i}'] = value
                    
        except Exception as e:
            logger.error(f"Erro ao ler coordenadas do site: {e}")
            
        return coords
    
    def read_fortress_name(self, site_addr: int) -> str:
        """Tenta ler o nome da fortaleza"""
        try:
            # O nome geralmente está numa estrutura de language_name
            # Vamos tentar vários offsets possíveis
            name_offsets = [0x20, 0x40, 0x60, 0x80, 0x100]
            
            for offset in name_offsets:
                name_ptr = self.dwarf_reader.memory_reader.read_pointer(site_addr + offset, 8)
                if name_ptr:
                    name = self.dwarf_reader.memory_reader.read_string(name_ptr, 64)
                    if name and len(name) > 2 and name.isprintable():
                        return name
                        
        except Exception as e:
            logger.error(f"Erro ao ler nome da fortaleza: {e}")
            
        return ""
    
    def read_site_raw_data(self, site_addr: int) -> Dict:
        """Lê dados brutos da estrutura do site"""
        raw_data = {}
        
        try:
            # Ler primeiros 256 bytes da estrutura
            chunk_size = 256
            data = self.dwarf_reader.memory_reader.read_memory(site_addr, chunk_size)
            
            if data:
                # Interpretar como diferentes tipos de dados
                for offset in range(0, min(len(data), 64), 4):
                    if offset + 4 <= len(data):
                        value_int32 = int.from_bytes(data[offset:offset+4], byteorder='little', signed=True)
                        raw_data[f'offset_0x{offset:02x}'] = value_int32
                        
        except Exception as e:
            logger.error(f"Erro ao ler dados brutos do site: {e}")
            
        return raw_data
    
    def explore_world_map_data(self, world_data_ptr: int) -> Dict:
        """Explora dados do mapa mundial"""
        logger.info("Explorando dados do mapa mundial...")
        
        map_data = {
            'dimensions': {},
            'regions': {},
            'geology': {},
            'hydrology': {},
            'climate': {}
        }
        
        try:
            # Procurar por dimensões do mundo em offsets conhecidos
            dimension_offsets = [0x00, 0x04, 0x08, 0x0C, 0x10, 0x14, 0x18, 0x1C]
            
            for i, offset in enumerate(dimension_offsets):
                value = self.dwarf_reader.memory_reader.read_int32(world_data_ptr + offset)
                
                # Valores típicos para dimensões de mundo DF (16-1024)
                if 16 <= value <= 1024:
                    map_data['dimensions'][f'dim_{i}_offset_0x{offset:02x}'] = value
                    logger.info(f"  Possível dimensão: offset 0x{offset:02x} = {value}")
                    
            # Explorar regiões do mundo
            map_data['regions'] = self.explore_world_regions(world_data_ptr)
            
            # Explorar dados geológicos
            map_data['geology'] = self.explore_geology_data(world_data_ptr)
            
        except Exception as e:
            logger.error(f"Erro ao explorar mapa mundial: {e}")
            
        return map_data
    
    def explore_world_regions(self, world_data_ptr: int) -> Dict:
        """Explora dados de regiões do mundo"""
        regions_data = {}
        
        try:
            # Procurar vetores de regiões em offsets típicos
            region_vector_offsets = [0x100, 0x200, 0x300, 0x400, 0x500]
            
            for offset in region_vector_offsets:
                start_ptr = self.dwarf_reader.memory_reader.read_pointer(world_data_ptr + offset, 8)
                end_ptr = self.dwarf_reader.memory_reader.read_pointer(world_data_ptr + offset + 8, 8)
                
                if start_ptr and end_ptr and end_ptr > start_ptr:
                    count = (end_ptr - start_ptr) // 8
                    
                    # Se o count faz sentido para regiões (1-1000)
                    if 1 <= count <= 1000:
                        regions_data[f'vector_offset_0x{offset:x}'] = {
                            'count': count,
                            'start_ptr': hex(start_ptr),
                            'end_ptr': hex(end_ptr)
                        }
                        logger.info(f"  Possível vetor de regiões: offset 0x{offset:x}, count {count}")
                        
        except Exception as e:
            logger.error(f"Erro ao explorar regiões: {e}")
            
        return regions_data
    
    def explore_geology_data(self, world_data_ptr: int) -> Dict:
        """Explora dados geológicos do mundo"""
        geology_data = {}
        
        try:
            # Dados geológicos podem estar em arrays de materiais
            geology_offsets = [0x1000, 0x2000, 0x3000, 0x4000]
            
            for offset in geology_offsets:
                # Ler alguns valores para ver se parecem IDs de materiais
                material_ids = []
                
                for i in range(10):
                    mat_id = self.dwarf_reader.memory_reader.read_int32(world_data_ptr + offset + (i * 4))
                    if 0 <= mat_id <= 1000:  # Range típico de IDs de materiais
                        material_ids.append(mat_id)
                        
                if len(material_ids) >= 5:  # Se encontrou vários IDs válidos
                    geology_data[f'materials_offset_0x{offset:x}'] = material_ids
                    logger.info(f"  Possíveis materiais: offset 0x{offset:x}, IDs {material_ids[:5]}...")
                    
        except Exception as e:
            logger.error(f"Erro ao explorar geologia: {e}")
            
        return geology_data
    
    def scan_for_coordinate_arrays(self, world_data_ptr: int) -> Dict:
        """Procura por arrays de coordenadas no world_data"""
        logger.info("Procurando arrays de coordenadas...")
        
        coord_data = {
            'coordinate_arrays': [],
            'potential_maps': []
        }
        
        try:
            # Procurar em toda a região do world_data
            scan_size = 0x10000  # 64KB de busca
            chunk_size = 0x1000   # 4KB por chunk
            
            for chunk_offset in range(0, scan_size, chunk_size):
                chunk_addr = world_data_ptr + chunk_offset
                data = self.dwarf_reader.memory_reader.read_memory(chunk_addr, chunk_size)
                
                if data:
                    # Procurar por padrões de coordenadas
                    coord_arrays = self.find_coordinate_patterns(data, chunk_addr)
                    coord_data['coordinate_arrays'].extend(coord_arrays)
                    
        except Exception as e:
            logger.error(f"Erro ao procurar coordenadas: {e}")
            
        return coord_data
    
    def find_coordinate_patterns(self, data: bytes, base_addr: int) -> List[Dict]:
        """Encontra padrões que podem ser coordenadas"""
        patterns = []
        
        try:
            # Procurar por sequências de coordenadas válidas
            for offset in range(0, len(data) - 12, 4):
                x = int.from_bytes(data[offset:offset+4], byteorder='little', signed=True)
                y = int.from_bytes(data[offset+4:offset+8], byteorder='little', signed=True)
                z = int.from_bytes(data[offset+8:offset+12], byteorder='little', signed=True)
                
                # Verificar se parecem coordenadas válidas
                if (0 <= x <= 1000 and 0 <= y <= 1000 and -100 <= z <= 200):
                    patterns.append({
                        'address': hex(base_addr + offset),
                        'coordinates': [x, y, z],
                        'type': 'potential_xyz'
                    })
                    
                # Verificar coordenadas de mapa mundial (podem ser maiores)
                elif (0 <= x <= 10000 and 0 <= y <= 10000 and -1000 <= z <= 1000):
                    patterns.append({
                        'address': hex(base_addr + offset),
                        'coordinates': [x, y, z],
                        'type': 'potential_world_coords'
                    })
                    
        except Exception as e:
            logger.error(f"Erro ao encontrar padrões: {e}")
            
        return patterns
    
    def generate_comprehensive_report(self) -> Dict:
        """Gera relatório completo da análise"""
        logger.info("Gerando relatório completo...")
        
        # Conectar ao DF
        if not self.connect_to_df():
            return {'error': 'Falha ao conectar ao DF'}
            
        # Ler ponteiro real do world_data
        world_data_ptr = self.read_world_data_pointer()
        if not world_data_ptr:
            return {'error': 'Falha ao ler ponteiro world_data'}
            
        report = {
            'analysis_timestamp': datetime.now().isoformat(),
            'world_data_address': hex(self.world_data_addr),
            'world_data_pointer': hex(world_data_ptr),
            'base_address': hex(self.base_addr),
            'active_sites': {},
            'world_map': {},
            'coordinate_arrays': {},
            'raw_structure': {}
        }
        
        try:
            # Explorar sites ativos
            report['active_sites'] = self.explore_active_sites(world_data_ptr)
            
            # Explorar mapa mundial
            report['world_map'] = self.explore_world_map_data(world_data_ptr)
            
            # Procurar arrays de coordenadas
            report['coordinate_arrays'] = self.scan_for_coordinate_arrays(world_data_ptr)
            
            # Ler estrutura bruta (primeiros 1KB)
            raw_data = self.dwarf_reader.memory_reader.read_memory(world_data_ptr, 1024)
            if raw_data:
                report['raw_structure'] = {
                    'hex_dump': raw_data[:256].hex(),
                    'interpreted_ints': [
                        int.from_bytes(raw_data[i:i+4], byteorder='little', signed=True)
                        for i in range(0, min(64, len(raw_data)), 4)
                    ]
                }
                
        except Exception as e:
            logger.error(f"Erro ao gerar relatório: {e}")
            report['error'] = str(e)
            
        return report
    
    def export_report(self, report: Dict) -> str:
        """Exporta o relatório para arquivo"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        exports_dir = Path(__file__).parent.parent / "exports"
        exports_dir.mkdir(exist_ok=True)
        
        filename = f"world_data_analysis_{timestamp}.json"
        filepath = exports_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        logger.info(f"Relatório exportado para: {filepath}")
        return str(filepath)

def main():
    """Execução principal"""
    print("="*60)
    print("WORLD DATA EXPLORER - Análise Completa do world_data")
    print("="*60)
    print()
    print("Este script analisa a estrutura world_data=0x142453de8 do Dwarf Fortress")
    print("Explorando sites ativos, mapas, coordenadas e estruturas internas.")
    print()
    
    explorer = WorldDataExplorer()
    
    try:
        # Gerar relatório completo
        print("🔍 Analisando world_data...")
        report = explorer.generate_comprehensive_report()
        
        if 'error' in report:
            print(f"❌ ERRO: {report['error']}")
            return
            
        # Exportar relatório
        filepath = explorer.export_report(report)
        
        print(f"\n{'='*60}")
        print("ANÁLISE CONCLUÍDA")
        print(f"{'='*60}")
        
        # Mostrar resumo
        print(f"\n📊 RESUMO:")
        print(f"   World data address: {report.get('world_data_address', 'N/A')}")
        print(f"   World data pointer: {report.get('world_data_pointer', 'N/A')}")
        
        if 'active_sites' in report:
            site_count = report['active_sites'].get('site_count', 0)
            print(f"   Sites ativos encontrados: {site_count}")
            
            # Mostrar fortaleza do jogador se encontrada
            for site in report['active_sites'].get('sites', []):
                if site.get('type') == 0:
                    print(f"   🏰 Fortaleza encontrada: {site.get('name', 'Unknown')}")
                    
        if 'world_map' in report:
            dimensions = report['world_map'].get('dimensions', {})
            if dimensions:
                print(f"   Dimensões do mundo: {len(dimensions)} valores encontrados")
                
        if 'coordinate_arrays' in report:
            coord_count = len(report['coordinate_arrays'].get('coordinate_arrays', []))
            print(f"   Arrays de coordenadas: {coord_count} padrões encontrados")
            
        print(f"\n📁 ARQUIVO: {filepath}")
        print("\nVerifique o arquivo de log 'world_data_explorer.log' para detalhes")
        
    except Exception as e:
        logger.error(f"Erro na análise: {e}")
        print(f"❌ ERRO: {e}")

if __name__ == "__main__":
    main()
