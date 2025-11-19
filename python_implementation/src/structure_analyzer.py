"""
Analisador completo de estrutura de keys e subkeys do arquivo JSON de dwarves
"""

import json
import os
from collections import defaultdict, Counter
from datetime import datetime

def analyze_structure(json_path):
    """Analisa completamente a estrutura do JSON"""
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'file_analyzed': json_path,
        'file_size_mb': os.path.getsize(json_path) / 1024 / 1024,
        'structure_analysis': {},
        'relationships': {},
        'statistics': {}
    }
    
    # 1. Análise de primeiro nível
    report['structure_analysis']['top_level'] = {
        'keys': list(data.keys()),
        'key_count': len(data)
    }
    
    # 2. Análise de metadata
    if 'metadata' in data:
        report['structure_analysis']['metadata'] = {
            'keys': list(data['metadata'].keys()),
            'values': data['metadata']
        }
    
    # 3. Análise profunda de estrutura de dwarves
    if 'dwarves' in data and len(data['dwarves']) > 0:
        dwarf = data['dwarves'][0]
        
        # Categorizar todas as keys por tipo
        simple_fields = {}
        dict_fields = {}
        list_fields = {}
        
        for key, value in dwarf.items():
            if isinstance(value, dict):
                dict_fields[key] = {
                    'subkey_count': len(value),
                    'subkeys': list(value.keys())
                }
                
                # Analisar estrutura profunda dos dicts
                for subkey, subvalue in value.items():
                    if isinstance(subvalue, list) and len(subvalue) > 0:
                        dict_fields[key][f'{subkey}_sample'] = subvalue[0] if len(subvalue) > 0 else None
                    elif isinstance(subvalue, dict):
                        dict_fields[key][f'{subkey}_keys'] = list(subvalue.keys())
                        
            elif isinstance(value, list):
                list_fields[key] = {
                    'element_count': len(value),
                    'element_type': type(value[0]).__name__ if len(value) > 0 else 'empty'
                }
                
                # Se é lista de dicts, analisar estrutura
                if len(value) > 0 and isinstance(value[0], dict):
                    list_fields[key]['element_structure'] = {
                        'keys': list(value[0].keys()),
                        'key_count': len(value[0])
                    }
                    
                    # Analisar tipos de valores dentro dos dicts
                    sample_dict = value[0]
                    value_types = {}
                    for k, v in sample_dict.items():
                        value_types[k] = type(v).__name__
                    list_fields[key]['value_types'] = value_types
                    
            else:
                simple_fields[key] = {
                    'type': type(value).__name__,
                    'sample_value': str(value)[:100] if value is not None else None
                }
        
        report['structure_analysis']['dwarf_fields'] = {
            'total_fields': len(dwarf),
            'simple_fields': {
                'count': len(simple_fields),
                'fields': simple_fields
            },
            'dict_fields': {
                'count': len(dict_fields),
                'fields': dict_fields
            },
            'list_fields': {
                'count': len(list_fields),
                'fields': list_fields
            }
        }
        
        # 4. Análise de relacionamentos
        relationships = analyze_relationships(data)
        report['relationships'] = relationships
        
        # 5. Estatísticas gerais
        stats = calculate_statistics(data)
        report['statistics'] = stats
    
    return report


def analyze_relationships(data):
    """Analisa relacionamentos entre keys e valores"""
    relationships = {
        'decoded_mappings': {},
        'id_references': {},
        'hierarchical_structures': {}
    }
    
    if 'dwarves' not in data or len(data['dwarves']) == 0:
        return relationships
    
    dwarf = data['dwarves'][0]
    
    # Mapear campos decodificados vs originais
    decoded_pairs = []
    for key in dwarf.keys():
        if key.endswith('_decoded'):
            original_key = key.replace('_decoded', '')
            if original_key in dwarf:
                decoded_pairs.append({
                    'original': original_key,
                    'decoded': key
                })
    
    relationships['decoded_mappings'] = {
        'pairs_found': len(decoded_pairs),
        'pairs': decoded_pairs
    }
    
    # Identificar campos de ID
    id_fields = [k for k in dwarf.keys() if 'id' in k.lower()]
    relationships['id_references'] = {
        'id_fields': id_fields,
        'count': len(id_fields)
    }
    
    # Estruturas hierárquicas (campos com subkeys)
    hierarchical = {}
    for key, value in dwarf.items():
        if isinstance(value, dict):
            hierarchical[key] = {
                'subkeys': list(value.keys()),
                'depth': 1
            }
            # Verificar se tem subestrutura
            for subkey, subvalue in value.items():
                if isinstance(subvalue, (dict, list)):
                    hierarchical[key]['has_nested_structure'] = True
                    break
    
    relationships['hierarchical_structures'] = hierarchical
    
    return relationships


def calculate_statistics(data):
    """Calcula estatísticas gerais do dataset"""
    stats = {}
    
    if 'dwarves' not in data:
        return stats
    
    dwarves = data['dwarves']
    
    # Estatísticas básicas
    stats['dwarf_count'] = len(dwarves)
    
    # Análise de arrays
    array_stats = {}
    if len(dwarves) > 0:
        sample_dwarf = dwarves[0]
        for key, value in sample_dwarf.items():
            if isinstance(value, list):
                lengths = [len(d.get(key, [])) for d in dwarves if isinstance(d.get(key), list)]
                array_stats[key] = {
                    'min_length': min(lengths) if lengths else 0,
                    'max_length': max(lengths) if lengths else 0,
                    'avg_length': sum(lengths) / len(lengths) if lengths else 0,
                    'total_elements': sum(lengths)
                }
    
    stats['array_statistics'] = array_stats
    
    # Contagem de valores não-nulos
    non_null_counts = {}
    if len(dwarves) > 0:
        sample_dwarf = dwarves[0]
        for key in sample_dwarf.keys():
            if not isinstance(sample_dwarf[key], (dict, list)):
                non_null = sum(1 for d in dwarves if d.get(key) is not None and d.get(key) != '')
                non_null_counts[key] = {
                    'non_null_count': non_null,
                    'percentage': (non_null / len(dwarves) * 100) if len(dwarves) > 0 else 0
                }
    
    stats['field_coverage'] = non_null_counts
    
    return stats


def generate_executive_report(analysis):
    """Gera relatório executivo formatado"""
    
    report_lines = []
    report_lines.append("="*80)
    report_lines.append("📊 RELATÓRIO EXECUTIVO - ANÁLISE ESTRUTURAL DE DWARVES")
    report_lines.append("="*80)
    report_lines.append("")
    
    # Informações básicas
    report_lines.append(f"📁 Arquivo: {os.path.basename(analysis['file_analyzed'])}")
    report_lines.append(f"📏 Tamanho: {analysis['file_size_mb']:.2f} MB")
    report_lines.append(f"⏰ Análise realizada em: {analysis['timestamp']}")
    report_lines.append("")
    
    # Estrutura de primeiro nível
    report_lines.append("🔍 1. ESTRUTURA DE PRIMEIRO NÍVEL:")
    top_level = analysis['structure_analysis']['top_level']
    report_lines.append(f"   Total de keys principais: {top_level['key_count']}")
    for key in top_level['keys']:
        report_lines.append(f"   ├── {key}")
    report_lines.append("")
    
    # Metadata
    if 'metadata' in analysis['structure_analysis']:
        report_lines.append("📋 2. METADATA:")
        meta = analysis['structure_analysis']['metadata']['values']
        for k, v in meta.items():
            if isinstance(v, dict):
                report_lines.append(f"   ├── {k}: {v}")
            else:
                report_lines.append(f"   ├── {k}: {v}")
        report_lines.append("")
    
    # Estrutura de campos dos dwarves
    report_lines.append("👥 3. ESTRUTURA DOS CAMPOS DE DWARF:")
    dwarf_fields = analysis['structure_analysis']['dwarf_fields']
    report_lines.append(f"   Total de campos por dwarf: {dwarf_fields['total_fields']}")
    report_lines.append(f"   ├── Campos simples: {dwarf_fields['simple_fields']['count']}")
    report_lines.append(f"   ├── Objetos (dict): {dwarf_fields['dict_fields']['count']}")
    report_lines.append(f"   └── Arrays (list): {dwarf_fields['list_fields']['count']}")
    report_lines.append("")
    
    # Campos simples detalhados
    report_lines.append("   🔹 CAMPOS SIMPLES (DETALHADO):")
    for field, info in sorted(dwarf_fields['simple_fields']['fields'].items()):
        sample = info['sample_value'] if info['sample_value'] else 'None'
        report_lines.append(f"      ├── {field} ({info['type']}): {sample}")
    report_lines.append("")
    
    # Objetos/Dicts detalhados
    report_lines.append("   🔸 OBJETOS/ESTRUTURAS (DETALHADO):")
    for field, info in sorted(dwarf_fields['dict_fields']['fields'].items()):
        report_lines.append(f"      ├── {field} ({info['subkey_count']} subkeys):")
        for subkey in info['subkeys']:
            report_lines.append(f"      │   └── {subkey}")
    report_lines.append("")
    
    # Arrays detalhados
    report_lines.append("   🔹 ARRAYS/LISTAS (DETALHADO):")
    for field, info in sorted(dwarf_fields['list_fields']['fields'].items()):
        report_lines.append(f"      ├── {field} ({info['element_count']} elementos):")
        report_lines.append(f"      │   └── Tipo de elemento: {info['element_type']}")
        if 'element_structure' in info:
            report_lines.append(f"      │   └── Estrutura do elemento: {info['element_structure']['key_count']} keys")
            for key in info['element_structure']['keys']:
                report_lines.append(f"      │       • {key}")
    report_lines.append("")
    
    # Relacionamentos
    report_lines.append("🔗 4. RELACIONAMENTOS IDENTIFICADOS:")
    rels = analysis['relationships']
    
    report_lines.append(f"   📊 Pares Decoded encontrados: {rels['decoded_mappings']['pairs_found']}")
    for pair in rels['decoded_mappings']['pairs']:
        report_lines.append(f"      ├── {pair['original']} ↔ {pair['decoded']}")
    report_lines.append("")
    
    report_lines.append(f"   🆔 Campos de ID: {rels['id_references']['count']}")
    for id_field in rels['id_references']['id_fields']:
        report_lines.append(f"      ├── {id_field}")
    report_lines.append("")
    
    report_lines.append(f"   🏗️ Estruturas Hierárquicas: {len(rels['hierarchical_structures'])}")
    for struct, info in rels['hierarchical_structures'].items():
        nested = '(com subestruturas)' if info.get('has_nested_structure') else ''
        report_lines.append(f"      ├── {struct} {nested}")
        for subkey in info['subkeys'][:5]:  # Primeiras 5 subkeys
            report_lines.append(f"      │   └── {subkey}")
        if len(info['subkeys']) > 5:
            report_lines.append(f"      │   └── ... (+{len(info['subkeys'])-5} mais)")
    report_lines.append("")
    
    # Estatísticas
    report_lines.append("📈 5. ESTATÍSTICAS GERAIS:")
    stats = analysis['statistics']
    report_lines.append(f"   Total de Dwarves: {stats['dwarf_count']}")
    report_lines.append("")
    
    report_lines.append("   📊 Estatísticas de Arrays:")
    for array_name, array_stats in stats['array_statistics'].items():
        report_lines.append(f"      ├── {array_name}:")
        report_lines.append(f"      │   ├── Min: {array_stats['min_length']} elementos")
        report_lines.append(f"      │   ├── Max: {array_stats['max_length']} elementos")
        report_lines.append(f"      │   ├── Média: {array_stats['avg_length']:.1f} elementos")
        report_lines.append(f"      │   └── Total: {array_stats['total_elements']} elementos")
    report_lines.append("")
    
    report_lines.append("   📋 Cobertura de Campos (% não-nulos):")
    coverage = sorted(stats['field_coverage'].items(), key=lambda x: x[1]['percentage'], reverse=True)
    for field, cov in coverage[:15]:  # Top 15
        report_lines.append(f"      ├── {field}: {cov['percentage']:.1f}% ({cov['non_null_count']}/{stats['dwarf_count']})")
    report_lines.append("")
    
    report_lines.append("="*80)
    report_lines.append("🎉 ANÁLISE ESTRUTURAL COMPLETADA COM SUCESSO!")
    report_lines.append("="*80)
    
    return "\n".join(report_lines)


if __name__ == "__main__":
    json_path = "../../exports/complete_dwarves_data_20251118_214050.json"
    
    print("🔍 Iniciando análise estrutural completa...")
    print()
    
    # Realizar análise
    analysis = analyze_structure(json_path)
    
    # Gerar relatório executivo
    executive_report = generate_executive_report(analysis)
    print(executive_report)
    
    # Salvar análise completa em JSON
    output_path = "../output/analysis/structure_analysis_complete.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    
    print()
    print(f"📁 Análise completa salva em: {output_path}")
    
    # Salvar relatório executivo em Markdown
    report_path = "../reports/STRUCTURE_ANALYSIS_EXECUTIVE_REPORT.md"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# 📊 Relatório Executivo - Análise Estrutural de Dwarves\n\n")
        f.write("```\n")
        f.write(executive_report)
        f.write("\n```\n")
    
    print(f"📄 Relatório executivo salvo em: {report_path}")
