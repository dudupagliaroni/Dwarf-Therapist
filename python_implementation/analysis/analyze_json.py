#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análise Completa do JSON do Dwarf Therapist
Gera relatório detalhado de todos os dados coletados
"""

import json
import statistics
from collections import Counter, defaultdict
import sys
import os
from pathlib import Path

# Configurar encoding para UTF-8
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

def analyze_json():
    """Função principal de análise"""
    
    # Definir caminho do arquivo de dados
    script_dir = Path(__file__).parent
    data_file = script_dir.parent / "data" / "complete_dwarves_data.json"
    
    # Verificar se arquivo existe
    if not data_file.exists():
        print("❌ Arquivo complete_dwarves_data.json não encontrado!")
        print(f"Procurado em: {data_file}")
        return
    
    # Carregar o JSON completo
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print("ANÁLISE COMPLETA DO JSON - DWARF THERAPIST")
    print("=" * 70)

    # 1. METADADOS E ESTRUTURA GERAL
    metadata = data['metadata']
    dwarves = data['dwarves']

    print("📊 ESTRUTURA GERAL:")
    print(f"   Versão: {metadata['version']}")
    print(f"   Timestamp: {metadata['timestamp']}")
    print(f"   Endereço base: {metadata['base_address']}")
    print(f"   Pointer size: {metadata['pointer_size']} bytes")
    print(f"   Layout: {metadata['layout_info']['version_name']}")
    print(f"   Checksum: {metadata['layout_info']['checksum']}")

    # 2. ESTATÍSTICAS DOS DWARVES
    print(f"\n👥 POPULAÇÃO DWARF:")
    print(f"   Total de dwarves: {len(dwarves)}")
    print(f"   Com skills: {metadata['statistics']['dwarves_with_skills']}")
    print(f"   Com ferimentos: {metadata['statistics']['dwarves_with_wounds']}")
    print(f"   Com equipamentos: {metadata['statistics']['dwarves_with_equipment']}")

    # 3. ANÁLISE DE IDADES
    ages = [d['age'] for d in dwarves if d['age'] > 0]
    if ages:
        print(f"\n📈 ANÁLISE DE IDADES:")
        print(f"   Idade média: {statistics.mean(ages):.1f} anos")
        print(f"   Idade mediana: {statistics.median(ages):.1f} anos")
        print(f"   Mais novo: {min(ages)} anos")
        print(f"   Mais velho: {max(ages)} anos")
        print(f"   Desvio padrão: {statistics.stdev(ages):.1f} anos")
        
        # Distribuição por faixas etárias
        young = len([a for a in ages if a < 30])
        adult = len([a for a in ages if 30 <= a < 80])
        elder = len([a for a in ages if a >= 80])
        print(f"   Distribuição etária:")
        print(f"      Jovens (<30): {young} ({young/len(ages)*100:.1f}%)")
        print(f"      Adultos (30-79): {adult} ({adult/len(ages)*100:.1f}%)")
        print(f"      Idosos (80+): {elder} ({elder/len(ages)*100:.1f}%)")

    # 4. ANÁLISE DE NOMES
    names = [d['name'] for d in dwarves if d['name']]
    name_lengths = [len(name) for name in names]
    print(f"\n📝 ANÁLISE DE NOMES:")
    print(f"   Dwarves com nome: {len(names)}")
    print(f"   Tamanho médio do nome: {statistics.mean(name_lengths):.1f} caracteres")
    print(f"   Nome mais longo: '{max(names, key=len)}' ({len(max(names, key=len))} chars)")
    print(f"   Nome mais curto: '{min(names, key=len)}' ({len(min(names, key=len))} chars)")
    
    # Análise de caracteres
    all_chars = ''.join(names)
    char_counter = Counter(all_chars)
    print(f"   Caracteres mais comuns nos nomes:")
    for char, count in char_counter.most_common(5):
        print(f"      '{char}': {count} ocorrências")

    # 5. ANÁLISE DE SKILLS
    all_skills = []
    skill_levels = []
    skill_names = set()
    skill_experience = []

    for dwarf in dwarves:
        for skill in dwarf['skills']:
            all_skills.append(skill)
            skill_levels.append(skill['level'])
            skill_experience.append(skill['experience'])
            skill_names.add(skill['name'])

    print(f"\n🎯 ANÁLISE DE SKILLS:")
    print(f"   Total de skills registrados: {len(all_skills)}")
    print(f"   Skills únicos: {len(skill_names)}")
    print(f"   Level médio: {statistics.mean(skill_levels):.2f}")
    print(f"   Level máximo: {max(skill_levels)}")
    print(f"   Experiência média: {statistics.mean(skill_experience):.0f}")
    print(f"   Experiência máxima: {max(skill_experience)}")

    # Distribuição de levels
    level_dist = Counter(skill_levels)
    print(f"   Distribuição de levels:")
    for level in sorted(level_dist.keys())[:10]:  # Primeiros 10 levels
        print(f"      Level {level}: {level_dist[level]} skills")

    # Top 15 skills mais comuns
    skill_counter = Counter(skill['name'] for skill in all_skills)
    print(f"   Top 15 skills mais comuns:")
    for skill_name, count in skill_counter.most_common(15):
        avg_level = statistics.mean([s['level'] for s in all_skills if s['name'] == skill_name])
        print(f"      {skill_name}: {count} dwarves (level médio: {avg_level:.1f})")

    # 6. ANÁLISE DE ATRIBUTOS FÍSICOS
    physical_attrs = []
    for dwarf in dwarves:
        for attr in dwarf['physical_attributes']:
            physical_attrs.append(attr)

    if physical_attrs:
        attr_values = [attr['value'] for attr in physical_attrs if attr['value'] > 0]
        attr_names = [attr['name'] for attr in physical_attrs]
        
        print(f"\n💪 ATRIBUTOS FÍSICOS:")
        print(f"   Total registrados: {len(physical_attrs)}")
        if attr_values:
            print(f"   Valor médio: {statistics.mean(attr_values):.1f}")
            print(f"   Valor máximo: {max(attr_values)}")
        
        # Contagem por tipo de atributo
        attr_counter = Counter(attr_names)
        print(f"   Distribuição por tipo:")
        for attr_name, count in attr_counter.most_common():
            values = [a['value'] for a in physical_attrs if a['name'] == attr_name and a['value'] > 0]
            if values:
                avg_value = statistics.mean(values)
                print(f"      {attr_name}: {count} dwarves (média: {avg_value:.1f})")

    # 7. ANÁLISE DE ATRIBUTOS MENTAIS
    mental_attrs = []
    for dwarf in dwarves:
        for attr in dwarf['mental_attributes']:
            mental_attrs.append(attr)

    if mental_attrs:
        mental_values = [attr['value'] for attr in mental_attrs if attr['value'] > 0]
        
        print(f"\n🧠 ATRIBUTOS MENTAIS:")
        print(f"   Total registrados: {len(mental_attrs)}")
        if mental_values:
            print(f"   Valor médio: {statistics.mean(mental_values):.1f}")
            print(f"   Valor máximo: {max(mental_values)}")

    # 8. ANÁLISE DE FERIMENTOS
    all_wounds = []
    for dwarf in dwarves:
        for wound in dwarf['wounds']:
            all_wounds.append(wound)

    if all_wounds:
        print(f"\n🏥 FERIMENTOS:")
        print(f"   Total de ferimentos: {len(all_wounds)}")
        
        # Análise de dor
        pain_values = [w['pain'] for w in all_wounds if w['pain'] > 0]
        if pain_values:
            print(f"   Dor média: {statistics.mean(pain_values):.1f}")
            print(f"   Dor máxima: {max(pain_values)}")
        
        # Análise de sangramento
        bleeding_values = [w['bleeding'] for w in all_wounds if w['bleeding'] > 0]
        if bleeding_values:
            print(f"   Sangramento médio: {statistics.mean(bleeding_values):.1f}")
            print(f"   Sangramento máximo: {max(bleeding_values)}")
        
        # Partes do corpo mais afetadas
        body_parts = [w['body_part'] for w in all_wounds]
        body_counter = Counter(body_parts)
        print(f"   Partes mais feridas:")
        for part, count in body_counter.most_common(10):
            print(f"      Parte {part}: {count} ferimentos")

    # 9. ANÁLISE DE EQUIPAMENTOS
    all_equipment = []
    for dwarf in dwarves:
        for item in dwarf['equipment']:
            all_equipment.append(item)

    if all_equipment:
        print(f"\n⚔️ EQUIPAMENTOS:")
        print(f"   Total de itens: {len(all_equipment)}")
        print(f"   Média de itens por dwarf: {len(all_equipment)/len([d for d in dwarves if d['equipment']]):.1f}")
        
        # Materiais mais comuns
        materials = [item['material_type'] for item in all_equipment]
        material_counter = Counter(materials)
        print(f"   Materiais mais comuns:")
        for material, count in material_counter.most_common(10):
            print(f"      Material {material}: {count} itens")

    # 10. ANÁLISE DE PERSONALIDADE
    personalities = [d['personality'] for d in dwarves if d['personality']]
    if personalities:
        stress_levels = [p['stress_level'] for p in personalities if p['stress_level'] > 0]
        focus_levels = [p['focus_level'] for p in personalities if p['focus_level'] > 0]
        
        print(f"\n🧠 PERSONALIDADE:")
        print(f"   Dwarves com dados de personalidade: {len(personalities)}")
        if stress_levels:
            print(f"   Stress médio: {statistics.mean(stress_levels):.1f}")
            print(f"   Stress máximo: {max(stress_levels)}")
        if focus_levels:
            print(f"   Foco médio: {statistics.mean(focus_levels):.1f}")
            print(f"   Foco máximo: {max(focus_levels)}")

    # 11. ANÁLISE DE LABORS
    all_labors = []
    enabled_labors = []
    for dwarf in dwarves:
        for labor in dwarf['labors']:
            all_labors.append(labor)
            if labor['enabled']:
                enabled_labors.append(labor)

    if all_labors:
        print(f"\n🔧 LABORS:")
        print(f"   Total de labors: {len(all_labors)}")
        print(f"   Labors habilitados: {len(enabled_labors)}")
        print(f"   Taxa de habilitação: {len(enabled_labors)/len(all_labors)*100:.1f}%")
        
        # Labors mais habilitados
        enabled_counter = Counter(labor['name'] for labor in enabled_labors)
        print(f"   Labors mais habilitados:")
        for labor_name, count in enabled_counter.most_common(10):
            print(f"      {labor_name}: {count} dwarves")

    # 12. RESUMO FINAL
    print(f"\n📋 RESUMO FINAL:")
    print(f"   Tamanho do arquivo: {len(json.dumps(data))/1024:.1f} KB")
    print(f"   Estruturas de dados:")
    print(f"      Dwarves: {len(dwarves)}")
    print(f"      Skills: {len(all_skills)}")
    print(f"      Atributos físicos: {len(physical_attrs)}")
    print(f"      Atributos mentais: {len(mental_attrs)}")
    print(f"      Ferimentos: {len(all_wounds)}")
    print(f"      Equipamentos: {len(all_equipment)}")
    print(f"      Labors: {len(all_labors)}")
    
    total_data_points = (len(dwarves) + len(all_skills) + len(physical_attrs) + 
                        len(mental_attrs) + len(all_wounds) + len(all_equipment) + len(all_labors))
    print(f"   TOTAL DE PONTOS DE DADOS: {total_data_points:,}")

if __name__ == "__main__":
    try:
        analyze_json()
    except Exception as e:
        print(f"Erro na análise: {e}")