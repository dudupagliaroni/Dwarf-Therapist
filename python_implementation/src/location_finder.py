#!/usr/bin/env python3
"""
Location Finder - Descobre dados de coordenadas, localizações e elevações na memória do DF
Explora informações espaciais e de posicionamento dos dwarves e estruturas do jogo
"""

import os
import sys
from pathlib import Path
import logging
from typing import Dict, List, Optional, Tuple, Any
import json
import struct

# Adicionar o caminho do complete_dwarf_reader
sys.path.insert(0, str(Path(__file__).parent))
from complete_dwarf_reader import (
    CompleteDFInstance, CompletelyDwarfData, MemoryReader, 
    logger as base_logger
)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('location_finder.log')
    ]
)
logger = logging.getLogger(__name__)

class LocationFinder:
    """Busca informações de coordenadas e localização na memória do DF"""
    
    def __init__(self, df_instance: CompleteDFInstance):
        self.df = df_instance
        self.memory = df_instance.memory_reader
        self.layout = df_instance.layout
        
        logger.info("LocationFinder inicializado")
        
        # Campos conhecidos relacionados a localização
        self.location_fields = {
            # Coordenadas básicas
            'pos_x': 'Coordenada X',
            'pos_y': 'Coordenada Y', 
            'pos_z': 'Coordenada Z (elevação)',
            'position': 'Posição geral',
            'coordinates': 'Coordenadas',
            'location': 'Localização',
            
            # Orientação e direção
            'facing': 'Direção que está olhando',
            'direction': 'Direção de movimento',
            'rotation': 'Rotação',
            
            # Localização específica
            'site_id': 'ID do site/local',
            'region_x': 'Região X (mapa mundo)',
            'region_y': 'Região Y (mapa mundo)',
            'area_id': 'ID da área',
            'building_id': 'ID do prédio',
            'room_id': 'ID do quarto',
            
            # Elevação e terreno
            'elevation': 'Elevação',
            'ground_level': 'Nível do solo',
            'water_level': 'Nível da água',
            'magma_level': 'Nível do magma',
            
            # Movimento e pathfinding
            'destination_x': 'Destino X',
            'destination_y': 'Destino Y',
            'destination_z': 'Destino Z',
            'path': 'Caminho de movimento',
            'path_vector': 'Vetor de caminho',
            
            # Squad e formação
            'squad_pos_x': 'Posição X no squad',
            'squad_pos_y': 'Posição Y no squad',
            'formation_x': 'Posição X na formação',
            'formation_y': 'Posição Y na formação',
        }
    
    def explore_dwarf_location(self, dwarf: CompletelyDwarfData) -> Dict:
        """
        Explora todos os campos relacionados à localização de um dwarf específico
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"Explorando localização de: {dwarf.name} (ID: {dwarf.id})")
        logger.info(f"Endereço base: 0x{dwarf.address:x}")
        
        location_data = {
            'dwarf_id': dwarf.id,
            'dwarf_name': dwarf.name,
            'address': hex(dwarf.address),
            'location_fields': {},
            'coordinate_candidates': [],
            'position_vectors': []
        }
        
        # 1. CAMPOS CONHECIDOS DE LOCALIZAÇÃO
        logger.info("\nBuscando campos de localização conhecidos:")
        layout_offsets = self.df.layout.offsets.get('dwarf', {})
        
        found_fields = 0
        for field_name, description in self.location_fields.items():
            if field_name in layout_offsets:
                offset = layout_offsets[field_name]
                addr = dwarf.address + offset
                
                # Ler como diferentes tipos de dados
                value_int32 = self.memory.read_int32(addr)
                value_int16 = self.memory.read_int16(addr)
                value_int8 = self.memory.read_int8(addr)
                value_float = struct.unpack('<f', self.memory.read_memory(addr, 4))[0] if len(self.memory.read_memory(addr, 4)) == 4 else 0.0
                
                logger.info(f"  {field_name} (offset 0x{offset:x}):")
                logger.info(f"    - int32: {value_int32}")
                logger.info(f"    - int16: {value_int16}")
                logger.info(f"    - int8: {value_int8}")
                logger.info(f"    - float: {value_float:.2f}")
                
                location_data['location_fields'][field_name] = {
                    'offset': hex(offset),
                    'address': hex(addr),
                    'value_int32': value_int32,
                    'value_int16': value_int16,
                    'value_int8': value_int8,
                    'value_float': round(value_float, 2),
                    'description': description
                }
                found_fields += 1
        
        if found_fields == 0:
            logger.warning("Nenhum campo de localização conhecido encontrado no layout")
        else:
            logger.info(f"Encontrados {found_fields} campos de localização conhecidos")
        
        # 2. BUSCAR COORDENADAS CANDIDATAS
        logger.info("\n--- Buscando coordenadas candidatas ---")
        candidates = self._find_coordinate_candidates(dwarf.address, location_data)
        
        # 3. EXPLORAR VETORES DE POSIÇÃO
        logger.info("\n--- Explorando vetores de posição ---")
        self._explore_position_vectors(dwarf.address, location_data)
        
        # 4. ANALISAR ÁREA DE MEMÓRIA PARA PADRÕES XYZ
        logger.info("\n--- Analisando padrões XYZ ---")
        self._analyze_xyz_patterns(dwarf.address, location_data)
        
        return location_data
    
    def _find_coordinate_candidates(self, base_addr: int, result_dict: Dict):
        """Busca valores que podem ser coordenadas (tipicamente 0-200 para mapas DF)"""
        logger.info("Procurando valores que podem ser coordenadas...")
        
        candidates = []
        chunk_size = 0x400  # 1024 bytes
        memory_data = self.memory.read_memory(base_addr, chunk_size)
        
        if not memory_data:
            logger.warning("Não foi possível ler região de memória")
            return candidates
        
        # Procurar por valores que podem ser coordenadas
        for offset in range(0, len(memory_data) - 4, 4):
            # Ler como int32
            value = int.from_bytes(memory_data[offset:offset+4], byteorder='little', signed=True)
            
            # Coordenadas típicas do DF são 0-200 para mapas de fortaleza
            if 0 <= value <= 300:
                # Verificar se há padrão XYZ nos próximos bytes
                if offset + 12 < len(memory_data):
                    y_value = int.from_bytes(memory_data[offset+4:offset+8], byteorder='little', signed=True)
                    z_value = int.from_bytes(memory_data[offset+8:offset+12], byteorder='little', signed=True)
                    
                    # Se Y e Z também estão em range razoável, pode ser coordenada XYZ
                    if 0 <= y_value <= 300 and -50 <= z_value <= 200:
                        candidates.append({
                            'offset': hex(offset),
                            'x': value,
                            'y': y_value,
                            'z': z_value,
                            'address': hex(base_addr + offset),
                            'confidence': 'high' if (10 <= value <= 200 and 10 <= y_value <= 200) else 'medium'
                        })
                        logger.info(f"  Coordenada XYZ candidata em offset 0x{offset:x}: ({value}, {y_value}, {z_value})")
            
            # Também procurar por valores de coordenada individual
            elif -100 <= value <= 500:  # Range mais amplo para Z (pode ser negativo)
                candidates.append({
                    'offset': hex(offset),
                    'value': value,
                    'address': hex(base_addr + offset),
                    'type': 'single_coordinate',
                    'confidence': 'low'
                })
        
        # Filtrar e mostrar os melhores candidatos
        high_confidence = [c for c in candidates if c.get('confidence') == 'high']
        medium_confidence = [c for c in candidates if c.get('confidence') == 'medium']
        
        logger.info(f"Encontrados {len(high_confidence)} candidatos de alta confiança")
        logger.info(f"Encontrados {len(medium_confidence)} candidatos de média confiança")
        
        result_dict['coordinate_candidates'] = candidates[:20]  # Primeiros 20
        return candidates
    
    def _explore_position_vectors(self, base_addr: int, result_dict: Dict):
        """Explora vetores que podem conter informações de posição"""
        vectors_found = []
        
        # Procurar vetores em offsets típicos
        for offset in range(0, 0x400, 8):
            addr = base_addr + offset
            vec_start = self.memory.read_pointer(addr, self.df.pointer_size)
            vec_end = self.memory.read_pointer(addr + self.df.pointer_size, self.df.pointer_size)
            
            if vec_start > 0 and vec_end > vec_start:
                size = (vec_end - vec_start) // self.df.pointer_size
                
                # Vetores pequenos podem conter posições
                if 1 <= size <= 50:
                    elements = []
                    for i in range(min(size, 10)):
                        elem_addr = vec_start + (i * self.df.pointer_size)
                        elem = self.memory.read_pointer(elem_addr, self.df.pointer_size)
                        elements.append(elem)
                        
                        # Se elemento aponta para uma região válida, explorar
                        if elem > 0x1000:
                            # Ler primeiros bytes como coordenadas potenciais
                            x = self.memory.read_int32(elem)
                            y = self.memory.read_int32(elem + 4)
                            z = self.memory.read_int32(elem + 8)
                            
                            if 0 <= x <= 300 and 0 <= y <= 300 and -50 <= z <= 200:
                                logger.info(f"  Vetor em offset 0x{offset:x}, elemento {i}: coordenadas ({x}, {y}, {z})")
                    
                    vectors_found.append({
                        'offset': hex(offset),
                        'start': hex(vec_start),
                        'end': hex(vec_end),
                        'size': size,
                        'elements': [hex(e) for e in elements]
                    })
        
        logger.info(f"Explorados {len(vectors_found)} vetores de posição")
        result_dict['position_vectors'] = vectors_found[:10]  # Primeiros 10
    
    def _analyze_xyz_patterns(self, base_addr: int, result_dict: Dict):
        """Analisa padrões consecutivos que podem ser estruturas XYZ"""
        patterns = []
        chunk_size = 0x300
        memory_data = self.memory.read_memory(base_addr, chunk_size)
        
        if not memory_data:
            return
        
        logger.info("Analisando padrões XYZ consecutivos...")
        
        # Procurar por estruturas de 12 bytes (3 int32) que podem ser XYZ
        for offset in range(0, len(memory_data) - 12, 4):
            try:
                x = struct.unpack('<i', memory_data[offset:offset+4])[0]
                y = struct.unpack('<i', memory_data[offset+4:offset+8])[0] 
                z = struct.unpack('<i', memory_data[offset+8:offset+12])[0]
                
                # Verificar se parece coordenadas válidas
                if (0 <= x <= 200 and 0 <= y <= 200 and -20 <= z <= 150):
                    # Verificar se há mais coordenadas adjacentes (array de posições)
                    next_x = struct.unpack('<i', memory_data[offset+12:offset+16])[0] if offset+16 < len(memory_data) else -999
                    next_y = struct.unpack('<i', memory_data[offset+16:offset+20])[0] if offset+20 < len(memory_data) else -999
                    next_z = struct.unpack('<i', memory_data[offset+20:offset+24])[0] if offset+24 < len(memory_data) else -999
                    
                    is_array = (0 <= next_x <= 200 and 0 <= next_y <= 200 and -20 <= next_z <= 150)
                    
                    pattern = {
                        'offset': hex(offset),
                        'x': x,
                        'y': y, 
                        'z': z,
                        'address': hex(base_addr + offset),
                        'is_array': is_array
                    }
                    
                    if is_array:
                        pattern['next_xyz'] = [next_x, next_y, next_z]
                        logger.info(f"  Array XYZ em offset 0x{offset:x}: ({x},{y},{z}) -> ({next_x},{next_y},{next_z})")
                    else:
                        logger.info(f"  XYZ em offset 0x{offset:x}: ({x},{y},{z})")
                    
                    patterns.append(pattern)
                    
            except (struct.error, IndexError):
                continue
        
        logger.info(f"Encontrados {len(patterns)} padrões XYZ")
        result_dict['xyz_patterns'] = patterns[:15]  # Primeiros 15
    
    def explore_global_coordinates(self) -> Dict:
        """Explora coordenadas globais do mundo/fortaleza"""
        logger.info(f"\n{'='*60}")
        logger.info("EXPLORANDO COORDENADAS GLOBAIS")
        logger.info(f"{'='*60}")
        
        global_data = {
            'world_coordinates': {},
            'fortress_position': {},
            'map_dimensions': {},
            'current_view': {}
        }
        
        # Endereços globais conhecidos
        addresses = self.layout.addresses
        logger.info(f"Endereços globais disponíveis: {len(addresses)}")
        
        # Coordenadas do mundo
        world_coords = [
            'world_width', 'world_height', 
            'fortress_pos_x', 'fortress_pos_y',
            'current_weather', 'current_season'
        ]
        
        for coord_name in world_coords:
            if coord_name in addresses:
                addr = addresses[coord_name] + self.df.base_addr
                value = self.memory.read_int32(addr)
                logger.info(f"  {coord_name}: {value}")
                global_data['world_coordinates'][coord_name] = value
        
        # Explorar área de endereços globais
        logger.info("\nExplorando área de endereços globais...")
        for addr_name, addr_offset in addresses.items():
            if any(keyword in addr_name.lower() for keyword in ['pos', 'coord', 'x', 'y', 'z', 'width', 'height', 'size']):
                addr = addr_offset + self.df.base_addr
                value = self.memory.read_int32(addr)
                logger.info(f"  {addr_name}: {value}")
                global_data['fortress_position'][addr_name] = value
        
        return global_data
    
    def analyze_all_dwarves_positions(self, dwarves: List[CompletelyDwarfData], max_count: int = 10):
        """Analisa posições de múltiplos dwarves para encontrar padrões"""
        logger.info(f"\n{'='*60}")
        logger.info(f"ANALISANDO POSIÇÕES DE {min(max_count, len(dwarves))} DWARVES")
        logger.info(f"{'='*60}")
        
        all_data = []
        coordinate_summary = {}
        
        for i, dwarf in enumerate(dwarves[:max_count]):
            logger.info(f"\n--- Dwarf {i+1}/{max_count} ---")
            location_data = self.explore_dwarf_location(dwarf)
            all_data.append(location_data)
            
            # Coletar coordenadas para análise de padrões
            for candidate in location_data.get('coordinate_candidates', []):
                if 'x' in candidate:  # É uma coordenada XYZ
                    coord_key = f"({candidate['x']}, {candidate['y']}, {candidate['z']})"
                    if coord_key not in coordinate_summary:
                        coordinate_summary[coord_key] = []
                    coordinate_summary[coord_key].append(dwarf.name)
        
        # Análise de padrões
        logger.info(f"\n{'='*60}")
        logger.info("ANÁLISE DE PADRÕES DE COORDENADAS")
        logger.info(f"{'='*60}")
        
        # Coordenadas compartilhadas (dwarves na mesma posição)
        shared_positions = {coord: names for coord, names in coordinate_summary.items() if len(names) > 1}
        if shared_positions:
            logger.info("Posições compartilhadas:")
            for coord, names in shared_positions.items():
                logger.info(f"  {coord}: {', '.join(names)}")
        
        # Estatísticas de distribuição
        all_xs = []
        all_ys = []
        all_zs = []
        
        for data in all_data:
            for candidate in data.get('coordinate_candidates', []):
                if 'x' in candidate and candidate.get('confidence') in ['high', 'medium']:
                    all_xs.append(candidate['x'])
                    all_ys.append(candidate['y'])
                    all_zs.append(candidate['z'])
        
        if all_xs:
            logger.info(f"\nEstatísticas de coordenadas ({len(all_xs)} amostras):")
            logger.info(f"  X: min={min(all_xs)}, max={max(all_xs)}, média={sum(all_xs)/len(all_xs):.1f}")
            logger.info(f"  Y: min={min(all_ys)}, max={max(all_ys)}, média={sum(all_ys)/len(all_ys):.1f}")
            logger.info(f"  Z: min={min(all_zs)}, max={max(all_zs)}, média={sum(all_zs)/len(all_zs):.1f}")
        
        return {
            'individual_data': all_data,
            'coordinate_summary': coordinate_summary,
            'shared_positions': shared_positions,
            'statistics': {
                'x_range': [min(all_xs), max(all_xs)] if all_xs else None,
                'y_range': [min(all_ys), max(all_ys)] if all_ys else None,
                'z_range': [min(all_zs), max(all_zs)] if all_zs else None,
                'total_coordinates_found': len(all_xs)
            }
        }
    
    def export_results(self, data: Dict, filename: str = None):
        """Exporta resultados da análise de localização"""
        if filename is None:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            exports_dir = Path(__file__).parent.parent.parent / "exports"
            exports_dir.mkdir(exist_ok=True)
            filename = exports_dir / f"location_analysis_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'analysis_type': 'dwarf_location_coordinates',
                'description': 'Análise de coordenadas, localizações e elevações na memória do DF',
                'data': data
            }, f, indent=2)
        
        logger.info(f"\nResultados exportados para: {filename}")
        return filename

def main():
    """Execução principal"""
    print("="*60)
    print("LOCATION FINDER - Descobrindo Coordenadas e Localizações")
    print("="*60)
    
    # Conectar ao DF
    df = CompleteDFInstance()
    
    try:
        # Conectar
        if not df.connect():
            print("ERRO: Falha ao conectar ao DF")
            return
        print("✓ Conectado ao DF")
        
        # Carregar layout
        if not df.load_memory_layout():
            print("ERRO: Falha ao carregar layout")
            return
        print("✓ Layout carregado")
        
        # Ler dwarves
        print("\nLendo dwarves...")
        dwarves = df.read_complete_dwarves()
        
        if not dwarves:
            print("ERRO: Nenhum dwarf encontrado")
            return
        
        print(f"✓ {len(dwarves)} dwarves encontrados")
        
        # Analisar localizações
        print("\nAnalisando localizações e coordenadas...")
        finder = LocationFinder(df)
        
        # Explorar coordenadas globais
        global_coords = finder.explore_global_coordinates()
        
        # Analisar primeiros 10 dwarves
        analysis_data = finder.analyze_all_dwarves_positions(dwarves, max_count=10)
        
        # Combinar dados
        final_data = {
            'global_coordinates': global_coords,
            'dwarves_analysis': analysis_data
        }
        
        # Exportar resultados
        output_file = finder.export_results(final_data)
        
        print(f"\n{'='*60}")
        print("ANÁLISE DE LOCALIZAÇÃO CONCLUÍDA")
        print(f"{'='*60}")
        print(f"\nResultados salvos em: {output_file}")
        print("\nVerifique o arquivo de log 'location_finder.log' para detalhes")
        
        # Resumo rápido
        stats = analysis_data.get('statistics', {})
        if stats.get('total_coordinates_found', 0) > 0:
            print(f"\n📍 RESUMO:")
            print(f"   Coordenadas encontradas: {stats['total_coordinates_found']}")
            print(f"   Range X: {stats.get('x_range', 'N/A')}")
            print(f"   Range Y: {stats.get('y_range', 'N/A')}")
            print(f"   Range Z: {stats.get('z_range', 'N/A')}")
            
            shared = len(analysis_data.get('shared_positions', {}))
            if shared > 0:
                print(f"   Posições compartilhadas: {shared}")
        
    except Exception as e:
        logger.error(f"Erro na análise: {e}", exc_info=True)
        print(f"ERRO: {e}")
    finally:
        df.disconnect()

if __name__ == "__main__":
    main()