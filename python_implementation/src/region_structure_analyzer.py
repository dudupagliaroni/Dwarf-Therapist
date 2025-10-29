#!/usr/bin/env python3
"""
Region Structure Analyzer - Análise das 530 Regiões do Mundo
Mapeia a estrutura completa das regiões encontradas no offset 0x300
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
        logging.FileHandler('region_analyzer.log')
    ]
)
logger = logging.getLogger(__name__)

class RegionStructureAnalyzer:
    """Analisador específico das 530 regiões do mundo"""
    
    def __init__(self):
        self.dwarf_reader = CompleteDFInstance()
        self.layout = None
        self.base_addr = 0
        self.world_data_addr = 0
        self.world_data_ptr = 0
        
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
    
    def analyze_regions_vector(self) -> Dict[str, Any]:
        """Análise do vetor de regiões no offset 0x300"""
        logger.info("Analisando vetor de regioes...")
        
        result = {
            "regions_vector": {},
            "region_samples": [],
            "structure_analysis": {},
            "patterns_discovered": {}
        }
        
        try:
            # Vetor de regiões está no offset 0x300 do world_data
            regions_vector_addr = self.world_data_ptr + 0x300
            
            # Ler ponteiros do vetor
            start_ptr = self.dwarf_reader.memory_reader.read_pointer(regions_vector_addr, 8)
            end_ptr = self.dwarf_reader.memory_reader.read_pointer(regions_vector_addr + 8, 8)
            
            # Calcular tamanho de cada região
            element_size = 8  # Assumindo ponteiros de 64-bit
            region_count = (end_ptr - start_ptr) // element_size
            
            logger.info(f"Regioes encontradas: {region_count}")
            logger.info(f"Start ptr: 0x{start_ptr:x}")
            logger.info(f"End ptr: 0x{end_ptr:x}")
            
            result["regions_vector"] = {
                "vector_address": f"0x{regions_vector_addr:x}",
                "start_ptr": f"0x{start_ptr:x}",
                "end_ptr": f"0x{end_ptr:x}",
                "region_count": region_count,
                "element_size": element_size
            }
            
            # Analisar uma amostra de regiões (primeiras 10)
            sample_count = min(10, region_count)
            logger.info(f"Analisando amostra de {sample_count} regioes...")
            
            for i in range(sample_count):
                region_ptr_addr = start_ptr + (i * element_size)
                
                try:
                    # Ler ponteiro para a região
                    region_addr = self.dwarf_reader.memory_reader.read_pointer(region_ptr_addr, 8)
                    
                    if region_addr != 0:  # Verificar se é um ponteiro válido
                        region_data = self._analyze_region_structure(region_addr, i)
                        result["region_samples"].append(region_data)
                        logger.info(f"Regiao {i}: 0x{region_addr:x}")
                        
                except Exception as e:
                    logger.warning(f"Erro ao ler regiao {i}: {e}")
                    continue
            
            # Análise de padrões
            if result["region_samples"]:
                result["structure_analysis"] = self._analyze_region_patterns(result["region_samples"])
            
            return result
            
        except Exception as e:
            logger.error(f"Erro na análise do vetor de regiões: {e}")
            return result
    
    def _analyze_region_structure(self, region_addr: int, region_index: int) -> Dict[str, Any]:
        """Análise detalhada da estrutura de uma região"""
        region_data = {
            "index": region_index,
            "address": f"0x{region_addr:x}",
            "raw_data": {},
            "coordinates": {},
            "potential_fields": {},
            "patterns": {}
        }
        
        try:
            # Ler os primeiros 128 bytes da estrutura da região
            raw_bytes = self.dwarf_reader.memory_reader.read_memory(region_addr, 128)
            
            # Analisar cada 4 bytes como diferentes tipos
            for offset in range(0, min(128, len(raw_bytes)), 4):
                if offset + 4 <= len(raw_bytes):
                    # Ler como int32 unsigned e signed
                    uint_val = struct.unpack('<I', raw_bytes[offset:offset+4])[0]
                    int_val = struct.unpack('<i', raw_bytes[offset:offset+4])[0]
                    
                    region_data["raw_data"][f"offset_0x{offset:02x}"] = {
                        "unsigned": uint_val,
                        "signed": int_val,
                        "hex": f"0x{uint_val:x}"
                    }
                    
                    # Identificar possíveis coordenadas (range 0-200)
                    if 0 < uint_val < 200:
                        region_data["coordinates"][f"offset_0x{offset:02x}"] = {
                            "value": uint_val,
                            "type": self._classify_coordinate_value(uint_val),
                            "likelihood": self._assess_coordinate_likelihood(uint_val, offset)
                        }
                    
                    # Identificar possíveis IDs ou tipos (range 0-1000)
                    elif 0 <= uint_val < 1000:
                        region_data["potential_fields"][f"offset_0x{offset:02x}"] = {
                            "value": uint_val,
                            "possible_types": self._classify_field_value(uint_val)
                        }
            
            # Procurar por padrões XYZ
            region_data["patterns"] = self._find_xyz_patterns(raw_bytes)
            
        except Exception as e:
            logger.warning(f"Erro ao analisar região {region_index}: {e}")
        
        return region_data
    
    def _classify_coordinate_value(self, value: int) -> List[str]:
        """Classifica um valor baseado em ranges típicos de coordenadas"""
        types = []
        
        if 0 <= value < 17:
            types.append("region_coordinate")  # 16x16 regions
        if 0 <= value < 48:
            types.append("local_map_coordinate")  # 48x48 local maps
        if 0 <= value < 200:
            types.append("world_coordinate")  # World map coordinates
        if value in [15, 16, 48]:
            types.append("map_dimension")  # Common map sizes
        
        return types
    
    def _assess_coordinate_likelihood(self, value: int, offset: int) -> str:
        """Avalia probabilidade de ser coordenada baseado no valor e posição"""
        score = 0
        
        # Valores em ranges típicos
        if 0 < value < 200:
            score += 2
        if 0 < value < 17:
            score += 1  # Range de região
        
        # Offsets típicos para coordenadas
        coord_offsets = [0x00, 0x04, 0x08, 0x0c, 0x10, 0x14, 0x18, 0x1c, 0x20]
        if offset in coord_offsets:
            score += 2
        
        # Valores especiais (como encontramos na fortaleza)
        if value in [15, 24]:
            score += 1
        
        if score >= 4:
            return "MUITO_ALTA"
        elif score >= 3:
            return "ALTA"
        elif score >= 2:
            return "MEDIA"
        else:
            return "BAIXA"
    
    def _classify_field_value(self, value: int) -> List[str]:
        """Classifica possíveis significados de campos baseado no valor"""
        possibilities = []
        
        if value == 0:
            possibilities.append("null_or_default")
        elif 1 <= value <= 10:
            possibilities.append("biome_type_id")
        elif 10 <= value <= 100:
            possibilities.append("material_id")
        elif 100 <= value <= 500:
            possibilities.append("large_id_or_count")
        elif 500 <= value <= 1000:
            possibilities.append("temperature_or_climate")
        
        return possibilities
    
    def _find_xyz_patterns(self, raw_bytes: bytes) -> Dict[str, List]:
        """Procura por padrões XYZ consecutivos"""
        patterns = {
            "xyz_triplets": [],
            "xy_pairs": [],
            "sequential_coords": []
        }
        
        # Procurar triplas XYZ
        for offset in range(0, len(raw_bytes) - 12, 4):
            if offset + 12 <= len(raw_bytes):
                x = struct.unpack('<I', raw_bytes[offset:offset+4])[0]
                y = struct.unpack('<I', raw_bytes[offset+4:offset+8])[0]
                z = struct.unpack('<I', raw_bytes[offset+8:offset+12])[0]
                
                if all(0 <= val < 200 for val in [x, y, z]) and any(val > 0 for val in [x, y, z]):
                    patterns["xyz_triplets"].append({
                        "offset": f"0x{offset:02x}",
                        "x": x, "y": y, "z": z
                    })
        
        # Procurar pares XY
        for offset in range(0, len(raw_bytes) - 8, 4):
            if offset + 8 <= len(raw_bytes):
                x = struct.unpack('<I', raw_bytes[offset:offset+4])[0]
                y = struct.unpack('<I', raw_bytes[offset+4:offset+8])[0]
                
                if all(0 <= val < 200 for val in [x, y]) and any(val > 0 for val in [x, y]):
                    patterns["xy_pairs"].append({
                        "offset": f"0x{offset:02x}",
                        "x": x, "y": y
                    })
        
        return patterns
    
    def _analyze_region_patterns(self, region_samples: List[Dict]) -> Dict[str, Any]:
        """Análise de padrões entre as regiões"""
        analysis = {
            "common_offsets": {},
            "coordinate_patterns": {},
            "value_distributions": {},
            "structure_size": 0
        }
        
        if not region_samples:
            return analysis
        
        # Identificar offsets que aparecem em todas as regiões
        all_offsets = set()
        for region in region_samples:
            all_offsets.update(region["raw_data"].keys())
        
        # Analisar valores comuns por offset
        for offset in all_offsets:
            values = []
            for region in region_samples:
                if offset in region["raw_data"]:
                    values.append(region["raw_data"][offset]["unsigned"])
            
            if values:
                analysis["common_offsets"][offset] = {
                    "values": values,
                    "min": min(values),
                    "max": max(values),
                    "unique_count": len(set(values)),
                    "all_zero": all(v == 0 for v in values),
                    "all_same": len(set(values)) == 1
                }
        
        # Identificar padrões de coordenadas
        coord_offsets = []
        for region in region_samples:
            coord_offsets.extend(list(region["coordinates"].keys()))
        
        # Contar frequência de offsets com coordenadas
        coord_frequency = {}
        for offset in coord_offsets:
            coord_frequency[offset] = coord_frequency.get(offset, 0) + 1
        
        analysis["coordinate_patterns"] = {
            "frequent_coord_offsets": {
                offset: count for offset, count in coord_frequency.items() 
                if count >= len(region_samples) // 2  # Aparece em pelo menos metade
            },
            "total_coord_offsets": len(set(coord_offsets))
        }
        
        return analysis
    
    def create_regions_report(self, analysis_data: Dict[str, Any]) -> str:
        """Cria relatório detalhado das regiões"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"regions_analysis_report_{timestamp}.json"
        report_path = Path(__file__).parent.parent / 'exports' / report_file
        
        # Garantir que o diretório existe
        report_path.parent.mkdir(exist_ok=True)
        
        # Adicionar metadata
        analysis_data["metadata"] = {
            "timestamp": datetime.now().isoformat(),
            "analyzer_version": "1.0",
            "df_pid": self.dwarf_reader.pid,
            "world_data_ptr": f"0x{self.world_data_ptr:x}",
            "analysis_focus": "region_structures"
        }
        
        # Salvar relatório
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Relatorio salvo em: {report_path}")
        return str(report_path)

def main():
    """Função principal"""
    print("=" * 60)
    print("🗺️ REGION STRUCTURE ANALYZER")
    print("=" * 60)
    print()
    print("Analisando as 530 regiões encontradas no offset 0x300...")
    print("Mapeando estruturas, coordenadas e padrões geográficos")
    print()
    
    analyzer = RegionStructureAnalyzer()
    
    print("🔍 Conectando ao Dwarf Fortress...")
    if not analyzer.connect_to_df():
        print("❌ ERRO: Falha ao conectar ao DF")
        return
    
    print("📊 Executando análise das regiões...")
    analysis_data = analyzer.analyze_regions_vector()
    
    print("📄 Gerando relatório...")
    report_path = analyzer.create_regions_report(analysis_data)
    
    print()
    print("=" * 60)
    print("✅ ANÁLISE DAS REGIÕES CONCLUÍDA")
    print("=" * 60)
    
    # Mostrar resultados principais
    if "regions_vector" in analysis_data:
        vector_info = analysis_data["regions_vector"]
        print(f"🗺️ Regiões encontradas: {vector_info['region_count']}")
        print(f"📍 Vetor em: {vector_info['vector_address']}")
    
    if "region_samples" in analysis_data and analysis_data["region_samples"]:
        samples = analysis_data["region_samples"]
        print(f"🔬 Amostras analisadas: {len(samples)}")
        
        # Mostrar coordenadas encontradas
        total_coords = 0
        for sample in samples:
            total_coords += len(sample.get("coordinates", {}))
        
        if total_coords > 0:
            print(f"📊 Coordenadas potenciais encontradas: {total_coords}")
        
        # Mostrar padrões XYZ
        total_xyz = 0
        for sample in samples:
            patterns = sample.get("patterns", {})
            total_xyz += len(patterns.get("xyz_triplets", []))
        
        if total_xyz > 0:
            print(f"🎯 Padrões XYZ encontrados: {total_xyz}")
    
    print(f"\n📁 RELATÓRIO COMPLETO: {report_path}")
    print("\n💡 PRÓXIMO: Analisar padrões encontrados para mapear estrutura do mundo!")

if __name__ == "__main__":
    main()