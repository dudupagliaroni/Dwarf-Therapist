#!/usr/bin/env python3
"""
Fortress Coordinate Analyzer - Análise Detalhada das Coordenadas da Fortaleza
Foca especificamente na validação das coordenadas encontradas (valor 15)
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
        logging.FileHandler('fortress_coordinates.log')
    ]
)
logger = logging.getLogger(__name__)

class FortressCoordinateAnalyzer:
    """Analisador específico das coordenadas da fortaleza"""
    
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
    
    def analyze_fortress_coordinates(self) -> Dict[str, Any]:
        """Análise detalhada das coordenadas da fortaleza"""
        logger.info("🏰 Analisando coordenadas da fortaleza...")
        
        result = {
            "fortress_analysis": {},
            "coordinate_validation": {},
            "structure_mapping": {},
            "patterns_found": []
        }
        
        try:
            # 1. Encontrar fortaleza
            sites_vector_addr = self.world_data_ptr + 0x000483b0
            start_ptr = self.dwarf_reader.memory_reader.read_pointer(sites_vector_addr, 8)
            end_ptr = self.dwarf_reader.memory_reader.read_pointer(sites_vector_addr + 8, 8)
            
            site_count = (end_ptr - start_ptr) // 8
            logger.info(f"Sites encontrados: {site_count}")
            
            for i in range(site_count):
                site_ptr_addr = start_ptr + (i * 8)
                site_addr = self.dwarf_reader.memory_reader.read_pointer(site_ptr_addr, 8)
                site_type = self.dwarf_reader.memory_reader.read_int16(site_addr + 0x80)
                
                if site_type == 0:  # Player fortress
                    logger.info(f"🏰 Fortaleza encontrada no endereço: 0x{site_addr:x}")
                    fortress_data = self._analyze_fortress_structure(site_addr)
                    result["fortress_analysis"] = fortress_data
                    break
            
            return result
            
        except Exception as e:
            logger.error(f"Erro na análise: {e}")
            return result
    
    def _analyze_fortress_structure(self, fortress_addr: int) -> Dict[str, Any]:
        """Análise detalhada da estrutura da fortaleza"""
        logger.info(f"📊 Analisando estrutura da fortaleza em 0x{fortress_addr:x}")
        
        fortress_data = {
            "address": f"0x{fortress_addr:x}",
            "coordinates": {},
            "raw_bytes": {},
            "potential_coords": {},
            "structure_analysis": {}
        }
        
        # Ler os primeiros 256 bytes da estrutura da fortaleza
        raw_data = self.dwarf_reader.memory_reader.read_memory(fortress_addr, 256)
        
        # Analisar cada 4 bytes como int32
        for offset in range(0, 256, 4):
            if offset + 4 <= len(raw_data):
                value = struct.unpack('<I', raw_data[offset:offset+4])[0]
                fortress_data["raw_bytes"][f"offset_0x{offset:02x}"] = value
                
                # Procurar por valores que podem ser coordenadas (0-200 range típico)
                if 0 < value < 200:
                    fortress_data["potential_coords"][f"offset_0x{offset:02x}"] = {
                        "value": value,
                        "as_signed": struct.unpack('<i', raw_data[offset:offset+4])[0],
                        "likelihood": self._assess_coordinate_likelihood(value, offset)
                    }
        
        # Análise específica dos offsets onde encontramos valor 15
        key_offsets = [0x18, 0x38]
        for offset in key_offsets:
            if offset < len(raw_data) - 4:
                value = struct.unpack('<I', raw_data[offset:offset+4])[0]
                signed_value = struct.unpack('<i', raw_data[offset:offset+4])[0]
                
                fortress_data["coordinates"][f"key_offset_0x{offset:02x}"] = {
                    "unsigned": value,
                    "signed": signed_value,
                    "hex": f"0x{value:x}",
                    "analysis": self._analyze_coordinate_value(value, offset)
                }
                
                logger.info(f"📍 Offset 0x{offset:02x}: {value} (signed: {signed_value})")
        
        # Procurar por padrões de coordenadas (X, Y, Z consecutivos)
        fortress_data["structure_analysis"] = self._find_coordinate_patterns(raw_data)
        
        return fortress_data
    
    def _assess_coordinate_likelihood(self, value: int, offset: int) -> str:
        """Avalia a probabilidade de um valor ser uma coordenada"""
        likelihood_score = 0
        
        # Valores típicos de coordenadas mundiais (0-200)
        if 0 < value < 200:
            likelihood_score += 3
        
        # Offsets onde tipicamente encontramos coordenadas
        coordinate_offsets = [0x04, 0x08, 0x0c, 0x18, 0x1c, 0x20, 0x38, 0x3c, 0x40]
        if offset in coordinate_offsets:
            likelihood_score += 2
        
        # Valores que são potências de 2 ou muito regulares são menos prováveis
        if value in [0, 1, 2, 4, 8, 16, 32, 64, 128]:
            likelihood_score -= 1
        
        if likelihood_score >= 4:
            return "MUITO_ALTA"
        elif likelihood_score >= 3:
            return "ALTA"
        elif likelihood_score >= 2:
            return "MÉDIA"
        else:
            return "BAIXA"
    
    def _analyze_coordinate_value(self, value: int, offset: int) -> Dict[str, Any]:
        """Análise detalhada de um valor de coordenada"""
        analysis = {
            "world_coord_range": 0 < value < 200,
            "region_coord_range": 0 < value < 17,  # Regiões são 16x16 tipicamente
            "local_coord_range": 0 < value < 48,   # Mapas locais são 48x48
            "is_fortress_size": value == 15,       # Valor específico encontrado
            "binary_representation": bin(value),
            "possible_meanings": []
        }
        
        # Análise baseada no valor específico
        if value == 15:
            analysis["possible_meanings"].extend([
                "Tamanho padrão de embark (15x15 não é comum, mas próximo)",
                "Coordenada de região (0-15 para região 16x16)",
                "Offset dentro de uma estrutura de mapa",
                "ID de bioma ou tipo de terreno"
            ])
        elif 0 < value < 17:
            analysis["possible_meanings"].extend([
                "Coordenada de região mundial",
                "Posição dentro de um tile de região"
            ])
        elif 0 < value < 48:
            analysis["possible_meanings"].extend([
                "Coordenada local no mapa",
                "Posição dentro do site da fortaleza"
            ])
        elif 0 < value < 200:
            analysis["possible_meanings"].extend([
                "Coordenada mundial X ou Y",
                "ID de região ou área"
            ])
        
        return analysis
    
    def _find_coordinate_patterns(self, raw_data: bytes) -> Dict[str, Any]:
        """Procura por padrões de coordenadas na estrutura"""
        patterns = {
            "xyz_triplets": [],
            "coordinate_pairs": [],
            "repeated_values": {},
            "sequential_values": []
        }
        
        # Procurar por triplas X,Y,Z
        for offset in range(0, len(raw_data) - 12, 4):
            x = struct.unpack('<I', raw_data[offset:offset+4])[0]
            y = struct.unpack('<I', raw_data[offset+4:offset+8])[0]
            z = struct.unpack('<I', raw_data[offset+8:offset+12])[0]
            
            # Se todos os valores estão em um range razoável de coordenadas
            if all(0 <= val < 200 for val in [x, y, z]) and any(val > 0 for val in [x, y, z]):
                patterns["xyz_triplets"].append({
                    "offset": f"0x{offset:02x}",
                    "x": x, "y": y, "z": z,
                    "likelihood": self._assess_triplet_likelihood(x, y, z)
                })
        
        # Procurar por pares X,Y
        for offset in range(0, len(raw_data) - 8, 4):
            x = struct.unpack('<I', raw_data[offset:offset+4])[0]
            y = struct.unpack('<I', raw_data[offset+4:offset+8])[0]
            
            if all(0 <= val < 200 for val in [x, y]) and any(val > 0 for val in [x, y]):
                patterns["coordinate_pairs"].append({
                    "offset": f"0x{offset:02x}",
                    "x": x, "y": y
                })
        
        # Contar valores repetidos
        for offset in range(0, len(raw_data) - 4, 4):
            value = struct.unpack('<I', raw_data[offset:offset+4])[0]
            if value not in patterns["repeated_values"]:
                patterns["repeated_values"][value] = []
            patterns["repeated_values"][value].append(f"0x{offset:02x}")
        
        # Manter apenas valores que aparecem mais de uma vez
        patterns["repeated_values"] = {
            val: offsets for val, offsets in patterns["repeated_values"].items() 
            if len(offsets) > 1 and 0 < val < 200
        }
        
        return patterns
    
    def _assess_triplet_likelihood(self, x: int, y: int, z: int) -> str:
        """Avalia a probabilidade de uma tripla ser coordenadas XYZ"""
        score = 0
        
        # Valores dentro de ranges típicos
        if all(0 < val < 200 for val in [x, y]):
            score += 2
        if 0 <= z < 50:  # Z típico para elevação
            score += 1
        
        # Não são valores muito baixos ou altos demais
        if not any(val in [0, 1] for val in [x, y, z]):
            score += 1
        
        # Valores não são idênticos (improvável para coordenadas reais)
        if len(set([x, y, z])) == 3:
            score += 1
        
        if score >= 4:
            return "ALTA"
        elif score >= 2:
            return "MÉDIA"
        else:
            return "BAIXA"
    
    def create_coordinate_report(self, analysis_data: Dict[str, Any]) -> str:
        """Cria relatório detalhado das coordenadas"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"fortress_coordinates_report_{timestamp}.json"
        report_path = Path(__file__).parent.parent / 'exports' / report_file
        
        # Garantir que o diretório existe
        report_path.parent.mkdir(exist_ok=True)
        
        # Adicionar metadata
        analysis_data["metadata"] = {
            "timestamp": datetime.now().isoformat(),
            "analyzer_version": "1.0",
            "df_pid": self.dwarf_reader.pid,
            "world_data_ptr": f"0x{self.world_data_ptr:x}",
            "analysis_focus": "fortress_coordinates"
        }
        
        # Salvar relatório
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"📄 Relatório salvo em: {report_path}")
        return str(report_path)

def main():
    """Função principal"""
    print("=" * 60)
    print("🏰 FORTRESS COORDINATE ANALYZER")
    print("=" * 60)
    print()
    print("Analisando coordenadas específicas da fortaleza...")
    print("Foco: Validar o valor '15' encontrado nos offsets 0x18 e 0x38")
    print()
    
    analyzer = FortressCoordinateAnalyzer()
    
    print("🔍 Conectando ao Dwarf Fortress...")
    if not analyzer.connect_to_df():
        print("❌ ERRO: Falha ao conectar ao DF")
        return
    
    print("📊 Executando análise detalhada...")
    analysis_data = analyzer.analyze_fortress_coordinates()
    
    print("📄 Gerando relatório...")
    report_path = analyzer.create_coordinate_report(analysis_data)
    
    print()
    print("=" * 60)
    print("✅ ANÁLISE CONCLUÍDA")
    print("=" * 60)
    
    # Mostrar resultados principais
    if "fortress_analysis" in analysis_data and analysis_data["fortress_analysis"]:
        fortress = analysis_data["fortress_analysis"]
        
        print(f"🏰 Fortaleza: {fortress['address']}")
        
        if "coordinates" in fortress:
            print("\n📍 COORDENADAS CHAVE:")
            for key, coord_data in fortress["coordinates"].items():
                print(f"   {key}: {coord_data['unsigned']} (signed: {coord_data['signed']})")
        
        if "potential_coords" in fortress and fortress["potential_coords"]:
            print(f"\n🎯 COORDENADAS POTENCIAIS: {len(fortress['potential_coords'])} encontradas")
            high_likelihood = [
                f"{offset}={data['value']}" 
                for offset, data in fortress["potential_coords"].items() 
                if data["likelihood"] in ["ALTA", "MUITO_ALTA"]
            ]
            if high_likelihood:
                print(f"   Alta probabilidade: {', '.join(high_likelihood)}")
        
        if "structure_analysis" in fortress:
            structure = fortress["structure_analysis"]
            if "xyz_triplets" in structure and structure["xyz_triplets"]:
                triplets = [t for t in structure["xyz_triplets"] if t["likelihood"] == "ALTA"]
                print(f"\n🗺️ TRIPLAS XYZ (alta probabilidade): {len(triplets)}")
                for triplet in triplets[:3]:  # Mostrar apenas as 3 primeiras
                    print(f"   {triplet['offset']}: ({triplet['x']}, {triplet['y']}, {triplet['z']})")
    
    print(f"\n📁 RELATÓRIO COMPLETO: {report_path}")
    print("\n💡 PRÓXIMO PASSO: Verificar as coordenadas no jogo para validação!")

if __name__ == "__main__":
    main()