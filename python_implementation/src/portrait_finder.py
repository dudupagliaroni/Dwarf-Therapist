#!/usr/bin/env python3
"""
Portrait Finder - Descobre a relação entre ID do dwarf e sprite nos portraits
Explora a memória do DF para encontrar dados de aparência/portrait
"""

import os
import sys
from pathlib import Path
import logging
from typing import Dict, List, Optional, Tuple
import json

# Adicionar o caminho do complete_dwarf_reader
sys.path.insert(0, str(Path(__file__).parent))
from complete_dwarf_reader import (
    CompleteDFInstance, CompletelyDwarfData, MemoryReader, 
    logger as base_logger
)

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('portrait_finder.log')
    ]
)
logger = logging.getLogger(__name__)

class PortraitFinder:
    """Busca informações de aparência/portrait na memória do DF"""
    
    def __init__(self, df_instance: CompleteDFInstance):
        self.df = df_instance
        self.memory = df_instance.memory_reader
        self.portraits_path = Path(r"C:\Program Files (x86)\Steam\steamapps\common\Dwarf Fortress\data\vanilla\vanilla_creatures_graphics\graphics\images\portraits")
        
        logger.info(f"PortraitFinder inicializado")
        logger.info(f"Caminho dos portraits: {self.portraits_path}")
        
        # Verificar se o diretório existe
        if self.portraits_path.exists():
            portrait_files = list(self.portraits_path.glob("*.png"))
            logger.info(f"Encontrados {len(portrait_files)} arquivos de portrait")
            for pf in portrait_files[:10]:  # Mostrar primeiros 10
                logger.info(f"  - {pf.name}")
        else:
            logger.warning(f"Diretório de portraits não encontrado: {self.portraits_path}")
    
    def explore_dwarf_appearance(self, dwarf: CompletelyDwarfData) -> Dict:
        """
        Explora campos relacionados à aparência de um dwarf específico
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"Explorando aparência de: {dwarf.name} (ID: {dwarf.id})")
        logger.info(f"Endereço base: 0x{dwarf.address:x}")
        
        appearance_data = {
            'dwarf_id': dwarf.id,
            'dwarf_name': dwarf.name,
            'address': hex(dwarf.address),
            'appearance_fields': {}
        }
        
        # Campos conhecidos relacionados à aparência
        layout_offsets = self.df.layout.offsets.get('dwarf', {})
        
        # Campos de interesse para aparência
        appearance_fields = {
            'appearance_vector': 'Vetor de aparência/características físicas',
            'colors': 'Cores (cabelo, pele, olhos)',
            'physical_description': 'Descrição física',
            'body_appearance': 'Aparência corporal',
            'figure_appearance': 'Aparência da figura',
            'characteristic': 'Características',
            'figure': 'Dados da figura',
            'body_plan': 'Plano corporal',
            'caste': 'Casta (afeta aparência)',
            'race': 'Raça (afeta aparência)'
        }
        
        logger.info("\nBuscando campos de aparência conhecidos:")
        for field_name, description in appearance_fields.items():
            if field_name in layout_offsets:
                offset = layout_offsets[field_name]
                addr = dwarf.address + offset
                
                # Tentar ler como diferentes tipos
                value_int32 = self.memory.read_int32(addr)
                value_int16 = self.memory.read_int16(addr)
                value_ptr = self.memory.read_pointer(addr, self.df.pointer_size)
                
                logger.info(f"  {field_name} (offset 0x{offset:x}):")
                logger.info(f"    - int32: {value_int32}")
                logger.info(f"    - int16: {value_int16}")
                logger.info(f"    - ptr: 0x{value_ptr:x}")
                
                appearance_data['appearance_fields'][field_name] = {
                    'offset': hex(offset),
                    'address': hex(addr),
                    'value_int32': value_int32,
                    'value_int16': value_int16,
                    'value_ptr': hex(value_ptr),
                    'description': description
                }
        
        # Explorar área de memória próxima ao endereço base
        logger.info("\n--- Explorando região de memória próxima ---")
        self._explore_memory_region(dwarf.address, appearance_data)
        
        # Tentar ler vetores próximos
        logger.info("\n--- Explorando vetores próximos ---")
        self._explore_nearby_vectors(dwarf.address, appearance_data)
        
        # Informações da raça/casta (podem conter dados de sprite)
        logger.info("\n--- Dados de Raça/Casta ---")
        appearance_data['race_info'] = self._explore_race_info(dwarf)
        
        return appearance_data
    
    def _explore_memory_region(self, base_addr: int, result_dict: Dict):
        """Explora região de memória próxima para encontrar padrões"""
        logger.info(f"Explorando região 0x{base_addr:x} - 0x{base_addr+0x500:x}")
        
        # Ler chunk de memória
        chunk_size = 0x500  # 1280 bytes
        memory_data = self.memory.read_memory(base_addr, chunk_size)
        
        if not memory_data:
            logger.warning("Não foi possível ler região de memória")
            return
        
        # Procurar por padrões interessantes
        interesting_offsets = []
        
        for offset in range(0, len(memory_data) - 8, 4):
            # Ler como int32
            value = int.from_bytes(memory_data[offset:offset+4], byteorder='little', signed=False)
            
            # Valores que podem ser índices de sprite (0-1000)
            if 0 < value < 1000:
                interesting_offsets.append((offset, value, 'possible_sprite_index'))
            
            # Valores que podem ser ponteiros válidos
            if 0x7FF000000000 < value < 0x7FFFFFFFFFFF:
                interesting_offsets.append((offset, value, 'possible_pointer'))
        
        # Mostrar achados interessantes
        if interesting_offsets:
            logger.info(f"Encontrados {len(interesting_offsets)} valores interessantes:")
            for offset, value, hint in interesting_offsets[:20]:  # Primeiros 20
                logger.info(f"  Offset 0x{offset:x}: {value} ({hint})")
                
            result_dict['memory_exploration'] = [
                {
                    'offset': hex(off),
                    'value': val,
                    'hint': hint
                }
                for off, val, hint in interesting_offsets[:50]
            ]
    
    def _explore_nearby_vectors(self, base_addr: int, result_dict: Dict):
        """Tenta encontrar vetores de dados próximos ao dwarf"""
        vectors_found = []
        
        # Procurar vetores a cada 8 bytes em uma janela
        for offset in range(0, 0x300, 8):
            addr = base_addr + offset
            vec_start = self.memory.read_pointer(addr, self.df.pointer_size)
            vec_end = self.memory.read_pointer(addr + self.df.pointer_size, self.df.pointer_size)
            
            # Validar se parece um vetor válido
            if vec_start > 0 and vec_end > vec_start:
                size = (vec_end - vec_start) // self.df.pointer_size
                
                # Vetores com tamanho razoável
                if 0 < size < 1000:
                    logger.info(f"  Vetor encontrado em offset 0x{offset:x}:")
                    logger.info(f"    Start: 0x{vec_start:x}")
                    logger.info(f"    End: 0x{vec_end:x}")
                    logger.info(f"    Size: {size} elementos")
                    
                    # Ler primeiros elementos
                    elements = []
                    for i in range(min(size, 10)):
                        elem_addr = vec_start + (i * self.df.pointer_size)
                        elem = self.memory.read_pointer(elem_addr, self.df.pointer_size)
                        elements.append(elem)
                    
                    vectors_found.append({
                        'offset': hex(offset),
                        'start': hex(vec_start),
                        'end': hex(vec_end),
                        'size': size,
                        'first_elements': [hex(e) for e in elements]
                    })
        
        if vectors_found:
            result_dict['nearby_vectors'] = vectors_found
            logger.info(f"Total de vetores encontrados: {len(vectors_found)}")
    
    def _explore_race_info(self, dwarf: CompletelyDwarfData) -> Dict:
        """Explora informações da raça que podem conter dados de sprite"""
        race_info = {
            'race_id': dwarf.race,
            'caste_id': dwarf.caste,
            'sex': dwarf.sex
        }
        
        logger.info(f"Raça: {dwarf.race}, Casta: {dwarf.caste}, Sexo: {dwarf.sex}")
        
        # Tentar acessar dados da raça
        race_vector_addr = self.df.layout.get_address('race_vector')
        if race_vector_addr:
            race_vector_addr += self.df.base_addr
            race_pointers = self.memory.read_vector(race_vector_addr, self.df.pointer_size)
            
            if dwarf.race < len(race_pointers):
                race_addr = race_pointers[dwarf.race]
                logger.info(f"Endereço da raça: 0x{race_addr:x}")
                
                race_offsets = self.df.layout.offsets.get('race', {})
                logger.info(f"Offsets de raça disponíveis: {list(race_offsets.keys())}")
                
                # Campos interessantes da raça
                interesting_race_fields = [
                    'caste_vector', 'creature_id', 'name', 'graphics'
                ]
                
                for field in interesting_race_fields:
                    if field in race_offsets:
                        offset = race_offsets[field]
                        addr = race_addr + offset
                        value = self.memory.read_pointer(addr, self.df.pointer_size)
                        logger.info(f"  {field}: 0x{value:x}")
                        race_info[field] = hex(value)
        
        return race_info
    
    def analyze_all_dwarves(self, dwarves: List[CompletelyDwarfData], max_count: int = 5):
        """Analisa múltiplos dwarves para encontrar padrões"""
        logger.info(f"\n{'='*60}")
        logger.info(f"ANALISANDO {min(max_count, len(dwarves))} DWARVES")
        logger.info(f"{'='*60}")
        
        all_data = []
        
        for i, dwarf in enumerate(dwarves[:max_count]):
            logger.info(f"\n--- Dwarf {i+1}/{max_count} ---")
            appearance_data = self.explore_dwarf_appearance(dwarf)
            all_data.append(appearance_data)
        
        # Procurar por padrões comuns
        self._find_patterns(all_data)
        
        return all_data
    
    def _find_patterns(self, all_data: List[Dict]):
        """Procura por padrões nos dados coletados"""
        logger.info(f"\n{'='*60}")
        logger.info("PROCURANDO PADRÕES")
        logger.info(f"{'='*60}")
        
        # Comparar campos comuns
        common_fields = {}
        for data in all_data:
            for field, info in data.get('appearance_fields', {}).items():
                if field not in common_fields:
                    common_fields[field] = []
                common_fields[field].append(info.get('value_int32', 0))
        
        logger.info("\nVariação de valores por campo:")
        for field, values in common_fields.items():
            unique_values = set(values)
            logger.info(f"  {field}: {len(unique_values)} valores únicos")
            if len(unique_values) <= 10:
                logger.info(f"    Valores: {unique_values}")
    
    def export_results(self, data: List[Dict], filename: str = None):
        """Exporta resultados da análise"""
        if filename is None:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            exports_dir = Path(__file__).parent.parent.parent / "exports"
            exports_dir.mkdir(exist_ok=True)
            filename = exports_dir / f"portrait_analysis_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'analysis_type': 'dwarf_portrait_appearance',
                'portraits_path': str(self.portraits_path),
                'portraits_exist': self.portraits_path.exists(),
                'data': data
            }, f, indent=2)
        
        logger.info(f"\nResultados exportados para: {filename}")
        return filename

def main():
    """Execução principal"""
    print("="*60)
    print("PORTRAIT FINDER - Descobrindo relação ID/Aparência")
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
        
        # Analisar aparência
        print("\nAnalisando aparência dos dwarves...")
        finder = PortraitFinder(df)
        
        # Analisar primeiros 5 dwarves
        analysis_data = finder.analyze_all_dwarves(dwarves, max_count=5)
        
        # Exportar resultados
        output_file = finder.export_results(analysis_data)
        
        print(f"\n{'='*60}")
        print("ANÁLISE CONCLUÍDA")
        print(f"{'='*60}")
        print(f"\nResultados salvos em: {output_file}")
        print("\nVerifique o arquivo de log 'portrait_finder.log' para detalhes")
        
    except Exception as e:
        logger.error(f"Erro na análise: {e}", exc_info=True)
        print(f"ERRO: {e}")
    finally:
        df.disconnect()

if __name__ == "__main__":
    main()
