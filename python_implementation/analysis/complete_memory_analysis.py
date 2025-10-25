#!/usr/bin/env python3
"""
ANÁLISE COMPLETA E EXAUSTIVA DOS DADOS DE MEMÓRIA DO DWARF FORTRESS
Extrai TODAS as chaves e subchaves de TODOS os layouts de memória disponíveis
"""

import configparser
import json
from pathlib import Path
from collections import defaultdict
import re

def parse_all_layouts():
    """Analisa todos os layouts de memória e extrai todas as chaves possíveis"""
    
    print("🔍 ANÁLISE EXAUSTIVA DOS LAYOUTS DE MEMÓRIA DO DWARF FORTRESS")
    print("=" * 80)
    
    layouts_dir = Path("share/memory_layouts/windows")
    layout_files = list(layouts_dir.glob("*.ini"))
    
    print(f"📁 Encontrados {len(layout_files)} arquivos de layout")
    print(f"📍 Diretório: {layouts_dir}")
    
    # Estrutura para armazenar todos os dados
    all_sections = defaultdict(lambda: defaultdict(set))
    version_data = {}
    
    # Analisar cada arquivo de layout
    for layout_file in layout_files:
        print(f"\n🔄 Processando: {layout_file.name}")
        
        try:
            config = configparser.ConfigParser()
            config.read(layout_file)
            
            version_data[layout_file.stem] = {
                'sections': list(config.sections()),
                'total_keys': 0
            }
            
            # Processar cada seção
            for section_name in config.sections():
                section = config[section_name]
                
                for key, value in section.items():
                    all_sections[section_name][key].add(value)
                    version_data[layout_file.stem]['total_keys'] += 1
                    
        except Exception as e:
            print(f"❌ Erro ao processar {layout_file.name}: {e}")
    
    return all_sections, version_data

def analyze_data_types(all_sections):
    """Analisa os tipos de dados e padrões encontrados"""
    
    print(f"\n📊 ANÁLISE DE TIPOS DE DADOS")
    print("=" * 50)
    
    data_patterns = {
        'hex_addresses': 0,
        'hex_offsets': 0,
        'decimal_values': 0,
        'text_values': 0,
        'boolean_values': 0
    }
    
    for section_name, keys in all_sections.items():
        for key, values in keys.items():
            for value in values:
                if re.match(r'^0x[0-9a-fA-F]+$', value):
                    if len(value) > 8:  # Endereços são mais longos
                        data_patterns['hex_addresses'] += 1
                    else:  # Offsets são mais curtos
                        data_patterns['hex_offsets'] += 1
                elif value.isdigit():
                    data_patterns['decimal_values'] += 1
                elif value.lower() in ['true', 'false']:
                    data_patterns['boolean_values'] += 1
                else:
                    data_patterns['text_values'] += 1
    
    for pattern, count in data_patterns.items():
        print(f"  📈 {pattern:<20}: {count}")

def categorize_sections(all_sections):
    """Categoriza as seções por tipo de dados que contêm"""
    
    categories = {
        'Global Addresses': ['addresses'],
        'Unit/Dwarf Data': ['dwarf_offsets', 'unit_offsets', 'soul_details'],
        'Health & Medical': ['unit_wound_offsets', 'syndrome_offsets'],
        'Items & Equipment': ['item_offsets', 'itemdef_offsets', 'general_ref_offsets'],
        'World & Environment': ['race_offsets', 'caste_offsets', 'material_offsets'],
        'Social & Historical': ['hist_figure_offsets', 'hist_entity_offsets', 'hist_event_offsets'],
        'Language & Names': ['word_offsets', 'language_offsets'],
        'Military & Combat': ['squad_offsets', 'weapon_offsets'],
        'Magic & Supernatural': ['artifact_offsets', 'creature_offsets'],
        'Technical/System': ['info', 'offsets', 'valid_flags_*']
    }
    
    print(f"\n🗂️  CATEGORIZAÇÃO DAS SEÇÕES")
    print("=" * 50)
    
    categorized = defaultdict(list)
    uncategorized = []
    
    for section_name in all_sections.keys():
        found_category = False
        for category, patterns in categories.items():
            for pattern in patterns:
                if pattern.replace('*', '') in section_name:
                    categorized[category].append(section_name)
                    found_category = True
                    break
            if found_category:
                break
        
        if not found_category:
            uncategorized.append(section_name)
    
    # Mostrar categorização
    for category, sections in categorized.items():
        if sections:
            print(f"\n📁 {category}:")
            for section in sorted(sections):
                key_count = len(all_sections[section])
                print(f"   ├─ {section} ({key_count} chaves)")
    
    if uncategorized:
        print(f"\n❓ Seções não categorizadas:")
        for section in sorted(uncategorized):
            key_count = len(all_sections[section])
            print(f"   ├─ {section} ({key_count} chaves)")

def detailed_section_analysis(all_sections):
    """Análise detalhada seção por seção"""
    
    print(f"\n📋 ANÁLISE DETALHADA DAS SEÇÕES")
    print("=" * 80)
    
    # Ordenar seções por número de chaves (mais importantes primeiro)
    sorted_sections = sorted(all_sections.items(), 
                           key=lambda x: len(x[1]), reverse=True)
    
    for section_name, keys in sorted_sections:
        print(f"\n🔍 [{section_name}] ({len(keys)} chaves)")
        print("─" * 60)
        
        # Ordenar chaves alfabeticamente
        for key in sorted(keys.keys()):
            values = keys[key]
            if len(values) == 1:
                value = list(values)[0]
                print(f"   {key:<30} = {value}")
            else:
                print(f"   {key:<30} = {len(values)} valores diferentes:")
                for i, value in enumerate(sorted(values)):
                    if i < 3:  # Mostrar apenas os primeiros 3
                        print(f"   {'':<32} • {value}")
                    elif i == 3:
                        print(f"   {'':<32} • ... e mais {len(values)-3}")
                        break

def export_complete_data(all_sections, version_data):
    """Exporta todos os dados para JSON"""
    
    print(f"\n💾 EXPORTANDO DADOS COMPLETOS")
    print("=" * 40)
    
    # Converter sets para lists para JSON
    export_data = {}
    for section_name, keys in all_sections.items():
        export_data[section_name] = {}
        for key, values in keys.items():
            export_data[section_name][key] = list(values)
    
    # Dados do export
    complete_export = {
        'metadata': {
            'total_layouts_analyzed': len(version_data),
            'total_sections': len(all_sections),
            'total_unique_keys': sum(len(keys) for keys in all_sections.values()),
            'analysis_timestamp': '2025-10-25T01:00:00Z'
        },
        'version_summary': version_data,
        'all_sections': export_data
    }
    
    # Salvar em arquivo
    with open('complete_memory_layout_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(complete_export, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Dados exportados para: complete_memory_layout_analysis.json")
    
    # Estatísticas finais
    total_keys = sum(len(keys) for keys in all_sections.values())
    total_values = sum(len(values) for keys in all_sections.values() 
                      for values in keys.values())
    
    print(f"📊 Estatísticas finais:")
    print(f"   • Layouts analisados: {len(version_data)}")
    print(f"   • Seções encontradas: {len(all_sections)}")
    print(f"   • Chaves únicas: {total_keys}")
    print(f"   • Valores totais: {total_values}")

def create_implementation_guide(all_sections):
    """Cria um guia de implementação baseado nos dados encontrados"""
    
    print(f"\n🛠️  GUIA DE IMPLEMENTAÇÃO")
    print("=" * 50)
    
    priority_sections = {
        'dwarf_offsets': 'ALTA - Dados essenciais dos dwarves',
        'soul_details': 'ALTA - Skills e personalidade',
        'addresses': 'ALTA - Endereços globais necessários',
        'unit_wound_offsets': 'MÉDIA - Sistema de saúde',
        'race_offsets': 'MÉDIA - Informações raciais',
        'caste_offsets': 'MÉDIA - Dados de casta/gênero',
        'hist_figure_offsets': 'BAIXA - Figuras históricas',
        'word_offsets': 'BAIXA - Sistema de linguagem'
    }
    
    print("\n🎯 Prioridades de implementação:")
    for section, priority in priority_sections.items():
        if section in all_sections:
            key_count = len(all_sections[section])
            print(f"   {priority} - {section} ({key_count} campos)")
        else:
            print(f"   ❌ {section} não encontrado nos layouts")
    
    # Campos mais comuns
    print(f"\n🔥 Campos mais frequentes entre versões:")
    
    key_frequency = defaultdict(int)
    for section_name, keys in all_sections.items():
        for key in keys.keys():
            key_frequency[f"{section_name}.{key}"] += 1
    
    most_common = sorted(key_frequency.items(), key=lambda x: x[1], reverse=True)[:20]
    
    for field, count in most_common:
        section, key = field.split('.', 1)
        print(f"   {field:<40} ({count} versões)")

def main():
    """Função principal"""
    
    # 1. Analisar todos os layouts
    all_sections, version_data = parse_all_layouts()
    
    # 2. Análise de tipos de dados
    analyze_data_types(all_sections)
    
    # 3. Categorização
    categorize_sections(all_sections)
    
    # 4. Análise detalhada
    detailed_section_analysis(all_sections)
    
    # 5. Export completo
    export_complete_data(all_sections, version_data)
    
    # 6. Guia de implementação
    create_implementation_guide(all_sections)
    
    print(f"\n🎉 ANÁLISE COMPLETA FINALIZADA!")
    print("=" * 50)
    print("📁 Arquivos gerados:")
    print("   • complete_memory_layout_analysis.json - Dados completos")
    print("   • Este relatório no terminal")

if __name__ == "__main__":
    main()