#!/usr/bin/env python3
"""
Extrator avançado de informações geográficas e de localização do Dwarf Therapist
Focando em world_data, sites, e estruturas de coordenadas
"""

import json
import re
import os
from pathlib import Path

def main():
    print("=== ANÁLISE AVANÇADA DE COORDENADAS E GEOGRAFIA ===\n")
    
    # 1. Examinar world_data dos exports JSON existentes
    exports_dir = Path(r'C:\Users\Eduardo\Documents\projetinhos\Dwarf-Therapist\python_implementation\exports')
    
    world_data_files = list(exports_dir.glob('world_data_analysis_*.json'))
    
    if world_data_files:
        print(f"Encontrados {len(world_data_files)} arquivos de world_data:")
        for file in world_data_files:
            print(f"  - {file.name}")
        
        # Analisar o mais recente
        latest_file = max(world_data_files, key=os.path.getmtime)
        print(f"\nAnalisando arquivo mais recente: {latest_file.name}")
        
        with open(latest_file, 'r', encoding='utf-8') as f:
            world_data = json.load(f)
        
        print(f"Estrutura do world_data:")
        if isinstance(world_data, dict):
            for key in world_data.keys():
                print(f"  - {key}")
                
                # Verificar se contém informações geográficas
                if isinstance(world_data[key], dict):
                    for subkey in list(world_data[key].keys())[:5]:  # Primeiras 5 chaves
                        print(f"    - {subkey}")
                elif isinstance(world_data[key], list) and len(world_data[key]) > 0:
                    print(f"    Lista com {len(world_data[key])} elementos")
                    if isinstance(world_data[key][0], dict):
                        print(f"    Primeiro elemento tem chaves: {list(world_data[key][0].keys())[:5]}")
    
    # 2. Analisar arquivos de memory layout especificamente para world/site offsets
    print("\n=== ANÁLISE DOS MEMORY LAYOUTS ===")
    
    layouts_dir = Path(r'C:\Users\Eduardo\Documents\projetinhos\Dwarf-Therapist\share\memory_layouts')
    
    # Buscar offsets relacionados a world e sites
    world_offsets = {}
    
    for platform_dir in layouts_dir.iterdir():
        if platform_dir.is_dir():
            print(f"\nAnalisando plataforma: {platform_dir.name}")
            
            for layout_file in platform_dir.glob('*.ini'):
                try:
                    with open(layout_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Buscar offsets relacionados a world, site, coordinate
                    world_related = []
                    
                    for line in content.split('\n'):
                        if '=' in line and any(keyword in line.lower() for keyword in ['world', 'site', 'coord', 'pos', 'location', 'map', 'elevation']):
                            world_related.append(line.strip())
                    
                    if world_related:
                        world_offsets[layout_file.name] = world_related
                        print(f"  {layout_file.name}: {len(world_related)} offsets relacionados")
                        for offset in world_related[:3]:  # Mostrar apenas os primeiros 3
                            print(f"    {offset}")
                        if len(world_related) > 3:
                            print(f"    ... e mais {len(world_related) - 3} offsets")
                
                except Exception as e:
                    print(f"  Erro ao ler {layout_file}: {e}")
    
    # 3. Examinar código fonte para estruturas de coordenadas
    print("\n=== ANÁLISE DO CÓDIGO FONTE ===")
    
    src_dir = Path(r'C:\Users\Eduardo\Documents\projetinhos\Dwarf-Therapist\src')
    
    coordinate_structures = []
    
    for cpp_file in src_dir.glob('*.cpp'):
        try:
            with open(cpp_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Buscar por estruturas que podem conter coordenadas
            patterns = [
                r'(read_\w+.*?coord)',
                r'(read_\w+.*?pos)',
                r'(read_\w+.*?[xy])',
                r'(\w+_x\s*=.*?read)',
                r'(\w+_y\s*=.*?read)',
                r'(\w+_z\s*=.*?read)',
                r'(world.*?read)',
                r'(site.*?read)'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for match in matches:
                    coordinate_structures.append({
                        'file': cpp_file.name,
                        'pattern': match
                    })
        
        except Exception as e:
            continue
    
    if coordinate_structures:
        print(f"Encontradas {len(coordinate_structures)} estruturas potenciais de coordenadas:")
        
        # Agrupar por arquivo
        by_file = {}
        for struct in coordinate_structures:
            if struct['file'] not in by_file:
                by_file[struct['file']] = []
            by_file[struct['file']].append(struct['pattern'])
        
        for file, patterns in list(by_file.items())[:5]:  # Primeiros 5 arquivos
            print(f"\n  {file}:")
            for pattern in patterns[:3]:  # Primeiros 3 patterns
                print(f"    {pattern}")
            if len(patterns) > 3:
                print(f"    ... e mais {len(patterns) - 3} patterns")
    
    # 4. Verificar comprehensive offsets para offsets específicos de localização
    print("\n=== OFFSETS ESPECÍFICOS DE LOCALIZAÇÃO ===")
    
    try:
        comprehensive_file = r'C:\Users\Eduardo\Documents\projetinhos\Dwarf-Therapist\python_implementation\exports\comprehensive_offsets_20251029_001658.json'
        
        with open(comprehensive_file, 'r', encoding='utf-8') as f:
            comprehensive_data = json.load(f)
        
        # Buscar por offsets que podem conter coordenadas reais
        location_offsets = []
        
        for section_name, section_data in comprehensive_data['sections'].items():
            if isinstance(section_data, dict):
                for offset_name, offset_data in section_data.items():
                    if isinstance(offset_data, dict):
                        meaning = offset_data.get('meaning', '').lower()
                        # Buscar por padrões mais específicos de coordenadas
                        if any(pattern in meaning for pattern in ['x', 'y', 'z', 'coordenad', 'elevação', 'mapa', 'localizaç']):
                            location_offsets.append({
                                'section': section_name,
                                'name': offset_name,
                                'hex': offset_data.get('hex_value', 'N/A'),
                                'meaning': offset_data.get('meaning', ''),
                                'type': offset_data.get('data_type', 'unknown')
                            })
        
        print(f"Encontrados {len(location_offsets)} offsets específicos de localização:")
        for offset in location_offsets[:10]:  # Primeiros 10
            print(f"  {offset['section']}.{offset['name']}: {offset['hex']}")
            print(f"    {offset['meaning']}")
    
    except Exception as e:
        print(f"Erro ao analisar comprehensive offsets: {e}")
    
    # 5. Criar relatório final
    print("\n=== CRIANDO RELATÓRIO DETALHADO ===")
    
    report = {
        'metadata': {
            'analysis_type': 'Coordenadas e Geografia do Dwarf Fortress',
            'generated_at': '2025-10-29T00:30:00'
        },
        'world_data_analysis': {
            'files_found': len(world_data_files) if 'world_data_files' in locals() else 0,
            'structure_keys': list(world_data.keys()) if 'world_data' in locals() and isinstance(world_data, dict) else []
        },
        'memory_layout_offsets': world_offsets,
        'coordinate_structures_in_code': {
            'total_found': len(coordinate_structures),
            'by_file': by_file if 'by_file' in locals() else {}
        },
        'specific_location_offsets': location_offsets if 'location_offsets' in locals() else [],
        'recommendations': [
            "world_data contém informações sobre sites ativos",
            "Cada site pode ter coordenadas no mundo",
            "Dwarf individuals podem ter posições locais",
            "Cursor/camera podem ter coordenadas de viewport",
            "Map blocks têm coordenadas de chunk/região"
        ]
    }
    
    # Salvar relatório
    report_file = 'geografia_e_coordenadas_detalhado.json'
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"Relatório detalhado salvo em: {report_file}")
    
    # 6. Sugestões de próximos passos
    print("\n=== PRÓXIMOS PASSOS SUGERIDOS ===")
    print("1. Examinar estrutura completa do world_data export")
    print("2. Procurar por offsets de cursor/camera no código")
    print("3. Analisar como o DT acessa coordenadas de dwarf")
    print("4. Verificar se existem offsets de map blocks")
    print("5. Implementar extração de coordenadas em tempo real")

if __name__ == "__main__":
    main()