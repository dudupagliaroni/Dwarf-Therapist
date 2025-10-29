#!/usr/bin/env python3
"""
Extrator de informações de coordenadas do arquivo comprehensive offsets
"""

import json
import re

def main():
    # Carregar dados
    with open(r'c:\Users\Eduardo\Documents\projetinhos\Dwarf-Therapist\python_implementation\exports\comprehensive_offsets_20251029_001658.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    sections = data['sections']
    
    print("=== ANÁLISE DE COORDENADAS E POSICIONAMENTO ===\n")
    
    # Buscar todos os offsets relacionados a coordenadas
    coord_keywords = ['pos', 'coord', 'x', 'y', 'z', 'map', 'location', 'elevation', 'position', 'cursor', 'view']
    
    found_coords = {}
    
    for section_name, section_data in sections.items():
        print(f"\n--- {section_name.upper()} ---")
        
        if not isinstance(section_data, dict):
            continue
            
        section_coords = []
        
        for offset_name, offset_data in section_data.items():
            if isinstance(offset_data, dict) and any(keyword in offset_name.lower() for keyword in coord_keywords):
                section_coords.append({
                    'name': offset_name,
                    'hex_value': offset_data.get('hex_value', 'N/A'),
                    'meaning': offset_data.get('meaning', 'Sem descrição'),
                    'data_type': offset_data.get('data_type', 'unknown'),
                    'size': offset_data.get('size', 'unknown'),
                    'possible_values': offset_data.get('possible_values', [])
                })
        
        if section_coords:
            found_coords[section_name] = section_coords
            for coord in section_coords:
                print(f"  {coord['name']}: {coord['hex_value']}")
                print(f"    Significado: {coord['meaning']}")
                print(f"    Tipo: {coord['data_type']}, Tamanho: {coord['size']}")
                if coord['possible_values']:
                    print(f"    Valores possíveis: {coord['possible_values'][:5]}...")
                print()
        else:
            print("  Nenhum offset de coordenada encontrado")
    
    # Buscar também offsets que podem conter coordenadas mesmo sem keywords óbvias
    print("\n=== OFFSETS POTENCIALMENTE RELACIONADOS A POSIÇÃO ===")
    
    potential_coords = []
    
    for section_name, section_data in sections.items():
        if not isinstance(section_data, dict):
            continue
            
        for offset_name, offset_data in section_data.items():
            if isinstance(offset_data, dict):
                meaning = offset_data.get('meaning', '').lower()
                if any(keyword in meaning for keyword in ['coord', 'pos', 'location', 'map', 'elevat', 'cursor', 'view']):
                    potential_coords.append({
                        'section': section_name,
                        'name': offset_name,
                        'hex_value': offset_data.get('hex_value', 'N/A'),
                        'meaning': offset_data.get('meaning', 'Sem descrição'),
                        'data_type': offset_data.get('data_type', 'unknown')
                    })
    
    for coord in potential_coords:
        print(f"{coord['section']}.{coord['name']}: {coord['hex_value']}")
        print(f"  {coord['meaning']}")
        print(f"  Tipo: {coord['data_type']}")
        print()
    
    # Estatísticas
    print(f"\n=== ESTATÍSTICAS ===")
    print(f"Total de seções: {len(sections)}")
    print(f"Seções com offsets de coordenadas: {len(found_coords)}")
    print(f"Total de offsets relacionados a posição: {sum(len(coords) for coords in found_coords.values()) + len(potential_coords)}")
    
    # Salvar relatório
    timestamp = data['metadata']['generated_at'][:19].replace(':', '').replace('-', '')
    report_file = f'coordinate_analysis_{timestamp}.json'
    
    report = {
        'metadata': {
            'generated_at': data['metadata']['generated_at'],
            'description': 'Análise de offsets relacionados a coordenadas e posicionamento'
        },
        'coordinate_offsets': found_coords,
        'potential_coordinates': potential_coords,
        'statistics': {
            'sections_with_coordinates': len(found_coords),
            'total_coordinate_offsets': sum(len(coords) for coords in found_coords.values()),
            'potential_coordinate_offsets': len(potential_coords)
        }
    }
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"Relatório salvo em: {report_file}")

if __name__ == "__main__":
    main()