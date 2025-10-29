#!/usr/bin/env python3
"""
Coordinate Arrays Analyzer - Análise dos 16,176 Padrões de Coordenadas
Investiga arrays massivos de coordenadas para mapear estruturas geográficas completas
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
        logging.FileHandler('coordinate_arrays.log')
    ]
)
logger = logging.getLogger(__name__)

class CoordinateArraysAnalyzer:
    """Analisador dos arrays massivos de coordenadas"""
    
    def __init__(self):
        self.dwarf_reader = CompleteDFInstance()
        self.layout = None
        self.base_addr = 0
        self.world_data_addr = 0
        self.world_data_ptr = 0
        
        # Configurações de análise
        self.chunk_size = 1024  # Ler em chunks de 1KB
        self.max_coord_value = 300  # Coordenadas típicas < 300
        
    def connect_to_df(self) -> bool:
        """Conecta ao Dwarf Fortress"""
        try:
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
                
            # Obter endereços
            self.base_addr = self.dwarf_reader.base_addr
            world_data_offset = self.layout.get_address('world_data')
            self.world_data_addr = self.base_addr + world_data_offset
            self.world_data_ptr = self.dwarf_reader.memory_reader.read_pointer(self.world_data_addr, 8)
            
            logger.info(f"Conectado ao DF. PID: {self.dwarf_reader.pid}")
            logger.info(f"World data pointer: 0x{self.world_data_ptr:x}")
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao conectar: {e}")
            return False
    
    def analyze_coordinate_arrays(self) -> Dict[str, Any]:
        """Análise massiva dos arrays de coordenadas"""
        logger.info("Iniciando análise dos arrays de coordenadas...")
        
        result = {
            "coordinate_grids": {},
            "pattern_analysis": {},
            "geographic_structures": {},
            "discovered_maps": {}
        }
        
        # Explorar diferentes regiões do world_data em busca de arrays
        search_ranges = [
            {"name": "elevation_maps", "start": 0x1000, "size": 0x10000},
            {"name": "climate_data", "start": 0x20000, "size": 0x8000},
            {"name": "geology_maps", "start": 0x30000, "size": 0x8000},
            {"name": "world_features", "start": 0x40000, "size": 0x10000},
            {"name": "biome_data", "start": 0x60000, "size": 0x8000}
        ]
        
        for search_range in search_ranges:
            logger.info(f"Explorando {search_range['name']}...")
            
            try:
                grids = self._analyze_memory_region(
                    self.world_data_ptr + search_range["start"],
                    search_range["size"],
                    search_range["name"]
                )
                
                if grids:
                    result["coordinate_grids"][search_range["name"]] = grids
                    
            except Exception as e:
                logger.warning(f"Erro ao explorar {search_range['name']}: {e}")
                continue
        
        # Análise de padrões nos dados encontrados
        result["pattern_analysis"] = self._analyze_coordinate_patterns(result["coordinate_grids"])
        
        # Tentar identificar estruturas geográficas
        result["geographic_structures"] = self._identify_geographic_structures(result["coordinate_grids"])
        
        return result
    
    def _analyze_memory_region(self, start_addr: int, size: int, region_name: str) -> Dict[str, Any]:
        """Analisa uma região específica da memória em busca de arrays de coordenadas"""
        region_data = {
            "arrays_found": [],
            "grid_patterns": [],
            "coordinate_ranges": {},
            "statistics": {}
        }
        
        # Ler a região em chunks
        chunks_analyzed = 0
        coordinates_found = 0
        
        for offset in range(0, size, self.chunk_size):
            chunk_addr = start_addr + offset
            
            try:
                # Ler chunk de dados
                chunk_data = self.dwarf_reader.memory_reader.read_memory(chunk_addr, 
                                                                      min(self.chunk_size, size - offset))
                
                # Analisar como array de int32
                coord_arrays = self._extract_coordinate_arrays(chunk_data, chunk_addr, offset)
                
                if coord_arrays:
                    region_data["arrays_found"].extend(coord_arrays)
                    coordinates_found += sum(len(arr["coordinates"]) for arr in coord_arrays)
                
                chunks_analyzed += 1
                
                if chunks_analyzed % 100 == 0:
                    logger.info(f"  {region_name}: {chunks_analyzed} chunks analisados, {coordinates_found} coordenadas")
                
            except Exception as e:
                logger.warning(f"Erro ao ler chunk {offset}: {e}")
                continue
        
        # Análise de padrões nos arrays encontrados
        if region_data["arrays_found"]:
            region_data["grid_patterns"] = self._find_grid_patterns(region_data["arrays_found"])
            region_data["coordinate_ranges"] = self._analyze_coordinate_ranges(region_data["arrays_found"])
            region_data["statistics"] = self._calculate_region_statistics(region_data["arrays_found"])
        
        logger.info(f"  {region_name}: {len(region_data['arrays_found'])} arrays, {coordinates_found} coordenadas totais")
        return region_data
    
    def _extract_coordinate_arrays(self, chunk_data: bytes, chunk_addr: int, chunk_offset: int) -> List[Dict]:
        """Extrai arrays de coordenadas de um chunk de dados"""
        arrays = []
        
        # Analisar como array de int32
        for i in range(0, len(chunk_data) - 12, 4):  # Deixar espaço para triplas
            if i + 12 <= len(chunk_data):
                # Ler 3 valores consecutivos como possível tripla XYZ
                values = struct.unpack('<III', chunk_data[i:i+12])
                
                # Filtrar valores que podem ser coordenadas
                if self._are_likely_coordinates(values):
                    arrays.append({
                        "address": f"0x{chunk_addr + i:x}",
                        "offset_in_region": chunk_offset + i,
                        "coordinates": list(values),
                        "type": self._classify_coordinate_triplet(values)
                    })
        
        return arrays
    
    def _are_likely_coordinates(self, values: Tuple[int, int, int]) -> bool:
        """Verifica se uma tripla de valores provavelmente representa coordenadas"""
        x, y, z = values
        
        # Todos os valores devem estar em um range razoável
        if not all(0 <= val <= self.max_coord_value for val in values):
            return False
        
        # Pelo menos um valor deve ser > 0
        if all(val == 0 for val in values):
            return False
        
        # Não devem ser valores muito específicos (como magic numbers)
        magic_numbers = {0xFFFFFFFF, 0xCCCCCCCC, 0xDDDDDDDD, 0xFEFEFEFE}
        if any(val in magic_numbers for val in values):
            return False
        
        return True
    
    def _classify_coordinate_triplet(self, values: Tuple[int, int, int]) -> str:
        """Classifica o tipo de coordenada baseado nos valores"""
        x, y, z = values
        max_val = max(values)
        
        if max_val <= 16:
            return "region_coordinates"
        elif max_val <= 48:
            return "local_map_coordinates"
        elif max_val <= 100:
            return "elevation_data"
        elif max_val <= 200:
            return "world_coordinates"
        else:
            return "large_scale_data"
    
    def _find_grid_patterns(self, arrays: List[Dict]) -> List[Dict]:
        """Procura por padrões de grid nos arrays de coordenadas"""
        patterns = []
        
        if len(arrays) < 4:  # Precisa de pelo menos 4 pontos para um grid mínimo
            return patterns
        
        # Agrupar por tipo de coordenada
        by_type = {}
        for arr in arrays:
            coord_type = arr["type"]
            if coord_type not in by_type:
                by_type[coord_type] = []
            by_type[coord_type].append(arr)
        
        # Procurar padrões em cada tipo
        for coord_type, type_arrays in by_type.items():
            if len(type_arrays) >= 4:
                grid_pattern = self._detect_grid_structure(type_arrays, coord_type)
                if grid_pattern:
                    patterns.append(grid_pattern)
        
        return patterns
    
    def _detect_grid_structure(self, arrays: List[Dict], coord_type: str) -> Optional[Dict]:
        """Detecta estrutura de grid em um conjunto de coordenadas"""
        if len(arrays) < 4:
            return None
        
        # Extrair coordenadas X e Y
        x_coords = []
        y_coords = []
        
        for arr in arrays:
            coords = arr["coordinates"]
            x_coords.append(coords[0])
            y_coords.append(coords[1])
        
        # Verificar se há padrão regular
        x_unique = sorted(set(x_coords))
        y_unique = sorted(set(y_coords))
        
        # Para ser um grid, deve ter distribuição regular
        if len(x_unique) >= 2 and len(y_unique) >= 2:
            # Verificar se os intervalos são regulares
            x_intervals = [x_unique[i+1] - x_unique[i] for i in range(len(x_unique)-1)]
            y_intervals = [y_unique[i+1] - y_unique[i] for i in range(len(y_unique)-1)]
            
            # Se os intervalos são consistentes, é um grid
            if len(set(x_intervals)) <= 2 and len(set(y_intervals)) <= 2:  # Permitir até 2 intervalos diferentes
                return {
                    "type": coord_type,
                    "grid_dimensions": {
                        "width": len(x_unique),
                        "height": len(y_unique),
                        "x_range": [min(x_unique), max(x_unique)],
                        "y_range": [min(y_unique), max(y_unique)],
                        "x_step": x_intervals[0] if x_intervals else 1,
                        "y_step": y_intervals[0] if y_intervals else 1
                    },
                    "total_points": len(arrays),
                    "coverage": len(arrays) / (len(x_unique) * len(y_unique))  # Quão completo é o grid
                }
        
        return None
    
    def _analyze_coordinate_ranges(self, arrays: List[Dict]) -> Dict[str, Any]:
        """Analisa os ranges de coordenadas"""
        if not arrays:
            return {}
        
        all_x = []
        all_y = []
        all_z = []
        
        for arr in arrays:
            coords = arr["coordinates"]
            all_x.append(coords[0])
            all_y.append(coords[1])
            all_z.append(coords[2])
        
        return {
            "x_range": {"min": min(all_x), "max": max(all_x), "unique": len(set(all_x))},
            "y_range": {"min": min(all_y), "max": max(all_y), "unique": len(set(all_y))},
            "z_range": {"min": min(all_z), "max": max(all_z), "unique": len(set(all_z))}
        }
    
    def _calculate_region_statistics(self, arrays: List[Dict]) -> Dict[str, Any]:
        """Calcula estatísticas da região"""
        if not arrays:
            return {}
        
        # Contar por tipo
        type_counts = {}
        for arr in arrays:
            coord_type = arr["type"]
            type_counts[coord_type] = type_counts.get(coord_type, 0) + 1
        
        return {
            "total_arrays": len(arrays),
            "types_found": type_counts,
            "address_range": {
                "first": arrays[0]["address"],
                "last": arrays[-1]["address"]
            }
        }
    
    def _analyze_coordinate_patterns(self, coordinate_grids: Dict) -> Dict[str, Any]:
        """Análise de padrões entre todas as regiões"""
        analysis = {
            "total_regions_analyzed": len(coordinate_grids),
            "total_arrays_found": 0,
            "most_promising_regions": [],
            "coordinate_type_distribution": {}
        }
        
        all_types = {}
        region_scores = []
        
        for region_name, region_data in coordinate_grids.items():
            arrays_count = len(region_data.get("arrays_found", []))
            grids_count = len(region_data.get("grid_patterns", []))
            
            analysis["total_arrays_found"] += arrays_count
            
            # Score baseado em número de arrays e padrões de grid
            score = arrays_count + (grids_count * 10)  # Grids valem mais
            
            region_scores.append({
                "region": region_name,
                "score": score,
                "arrays": arrays_count,
                "grids": grids_count
            })
            
            # Contar tipos de coordenadas
            if "statistics" in region_data and "types_found" in region_data["statistics"]:
                for coord_type, count in region_data["statistics"]["types_found"].items():
                    all_types[coord_type] = all_types.get(coord_type, 0) + count
        
        # Top 3 regiões mais promissoras
        region_scores.sort(key=lambda x: x["score"], reverse=True)
        analysis["most_promising_regions"] = region_scores[:3]
        
        analysis["coordinate_type_distribution"] = all_types
        
        return analysis
    
    def _identify_geographic_structures(self, coordinate_grids: Dict) -> Dict[str, Any]:
        """Identifica possíveis estruturas geográficas nos dados"""
        structures = {
            "world_map": None,
            "elevation_map": None,
            "region_grid": None,
            "biome_map": None
        }
        
        for region_name, region_data in coordinate_grids.items():
            grids = region_data.get("grid_patterns", [])
            
            for grid in grids:
                dimensions = grid["grid_dimensions"]
                coord_type = grid["type"]
                
                # Tentar classificar baseado nas dimensões e tipo
                if coord_type == "world_coordinates":
                    if dimensions["width"] > 50 and dimensions["height"] > 50:
                        structures["world_map"] = {
                            "region": region_name,
                            "dimensions": dimensions,
                            "confidence": "ALTA"
                        }
                elif coord_type == "elevation_data":
                    structures["elevation_map"] = {
                        "region": region_name,
                        "dimensions": dimensions,
                        "confidence": "MÉDIA"
                    }
                elif coord_type == "region_coordinates":
                    structures["region_grid"] = {
                        "region": region_name,
                        "dimensions": dimensions,
                        "confidence": "ALTA"
                    }
        
        return structures
    
    def create_arrays_report(self, analysis_data: Dict[str, Any]) -> str:
        """Cria relatório dos arrays de coordenadas"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"coordinate_arrays_report_{timestamp}.json"
        report_path = Path(__file__).parent.parent / 'exports' / report_file
        
        # Garantir que o diretório existe
        report_path.parent.mkdir(exist_ok=True)
        
        # Adicionar metadata
        analysis_data["metadata"] = {
            "timestamp": datetime.now().isoformat(),
            "analyzer_version": "1.0",
            "df_pid": self.dwarf_reader.pid,
            "world_data_ptr": f"0x{self.world_data_ptr:x}",
            "analysis_focus": "coordinate_arrays"
        }
        
        # Salvar relatório
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Relatorio salvo em: {report_path}")
        return str(report_path)

def main():
    """Função principal"""
    print("=" * 60)
    print("📊 COORDINATE ARRAYS ANALYZER")
    print("=" * 60)
    print()
    print("Analisando 16,176+ padrões de coordenadas encontrados...")
    print("Procurando mapas de elevação, clima, geologia e estruturas mundiais")
    print()
    
    analyzer = CoordinateArraysAnalyzer()
    
    print("🔍 Conectando ao Dwarf Fortress...")
    if not analyzer.connect_to_df():
        print("❌ ERRO: Falha ao conectar ao DF")
        return
    
    print("📊 Executando análise massiva de coordenadas...")
    print("⚠️  AVISO: Este processo pode demorar alguns minutos...")
    analysis_data = analyzer.analyze_coordinate_arrays()
    
    print("📄 Gerando relatório...")
    report_path = analyzer.create_arrays_report(analysis_data)
    
    print()
    print("=" * 60)
    print("✅ ANÁLISE DOS ARRAYS CONCLUÍDA")
    print("=" * 60)
    
    # Mostrar resultados principais
    if "pattern_analysis" in analysis_data:
        patterns = analysis_data["pattern_analysis"]
        print(f"📊 Arrays totais encontrados: {patterns.get('total_arrays_found', 0)}")
        print(f"🗺️ Regiões analisadas: {patterns.get('total_regions_analyzed', 0)}")
        
        if "most_promising_regions" in patterns and patterns["most_promising_regions"]:
            print("\n🎯 REGIÕES MAIS PROMISSORAS:")
            for region in patterns["most_promising_regions"][:3]:
                print(f"   {region['region']}: {region['arrays']} arrays, {region['grids']} grids")
        
        if "coordinate_type_distribution" in patterns and patterns["coordinate_type_distribution"]:
            print("\n📍 TIPOS DE COORDENADAS ENCONTRADAS:")
            for coord_type, count in patterns["coordinate_type_distribution"].items():
                print(f"   {coord_type}: {count}")
    
    if "geographic_structures" in analysis_data:
        structures = analysis_data["geographic_structures"]
        identified = [name for name, data in structures.items() if data is not None]
        
        if identified:
            print(f"\n🌍 ESTRUTURAS GEOGRÁFICAS IDENTIFICADAS: {len(identified)}")
            for structure_name in identified:
                structure = structures[structure_name]
                print(f"   {structure_name}: {structure['confidence']} confiança")
    
    print(f"\n📁 RELATÓRIO COMPLETO: {report_path}")
    print("\n🎉 DESCOBERTAS PRONTAS PARA VISUALIZAÇÃO!")

if __name__ == "__main__":
    main()