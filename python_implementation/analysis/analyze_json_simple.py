#!/usr/bin/env python3
"""
Análise Simplificada do JSON do Dwarf Therapist
Versão compatível com Windows PowerShell
"""

import json
import statistics
from collections import Counter, defaultdict
import sys
import os
from pathlib import Path

def analyze_json_simple():
    """Função principal de análise sem emojis"""
    
    # Definir caminho do arquivo de dados
    script_dir = Path(__file__).parent
    data_file = script_dir.parent / "data" / "complete_dwarves_data.json"
    
    # Verificar se arquivo existe
    if not data_file.exists():
        print("ERRO: Arquivo complete_dwarves_data.json não encontrado!")
        print(f"Procurado em: {data_file}")
        return
    
    # Carregar o JSON completo
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print("ANÁLISE COMPLETA DO JSON - DWARF THERAPIST")
    print("=" * 70)
    
    # Informações gerais
    metadata = data.get('metadata', {})
    dwarves = data.get('dwarves', [])
    
    print(f"\nINFORMAÇÕES GERAIS:")
    print(f"   Data de extração: {metadata.get('extraction_date', 'N/A')}")
    print(f"   Versão DF: {metadata.get('df_version', 'N/A')}")
    print(f"   Total de anões: {len(dwarves)}")
    print(f"   Tamanho do arquivo: {metadata.get('file_size', 'N/A')}")
    
    if not dwarves:
        print("ERRO: Nenhum dado de anão encontrado!")
        return
    
    # Análise demográfica básica
    print(f"\nANÁLISE DEMOGRÁFICA:")
    sexos = [d.get('sex', 'Unknown') for d in dwarves]
    contador_sexos = Counter(sexos)
    
    print(f"   Distribuição por sexo:")
    for sexo, count in contador_sexos.items():
        print(f"      {sexo}: {count} ({count/len(dwarves)*100:.1f}%)")
    
    # Análise de idades
    idades = [d.get('age', 0) for d in dwarves if d.get('age') is not None]
    if idades:
        print(f"\n   Estatísticas de idade:")
        print(f"      Média: {statistics.mean(idades):.1f} anos")
        print(f"      Mediana: {statistics.median(idades):.1f} anos")
        print(f"      Mais novo: {min(idades)} anos")
        print(f"      Mais velho: {max(idades)} anos")
    
    # Análise de habilidades
    print(f"\nANÁLISE DE HABILIDADES:")
    all_skills = []
    for dwarf in dwarves:
        skills = dwarf.get('skills', [])
        for skill in skills:
            if isinstance(skill, dict) and skill.get('level', 0) > 0:
                skill_name = skill.get('name', f"Skill_{skill.get('id', 'Unknown')}")
                all_skills.append(skill_name)
    
    skill_counts = Counter(all_skills)
    print(f"   Total de habilidades únicas: {len(skill_counts)}")
    print(f"   Top 10 habilidades mais comuns:")
    
    for skill, count in skill_counts.most_common(10):
        percentage = (count / len(dwarves)) * 100
        print(f"      {skill}: {count} anões ({percentage:.1f}%)")
    
    # Análise de profissões
    print(f"\nANÁLISE DE PROFISSÕES:")
    profissoes = [d.get('profession', 'Unknown') for d in dwarves]
    contador_prof = Counter(profissoes)
    
    print(f"   Total de profissões únicas: {len(contador_prof)}")
    print(f"   Top 10 profissões:")
    
    for prof, count in contador_prof.most_common(10):
        percentage = (count / len(dwarves)) * 100
        print(f"      {prof}: {count} anões ({percentage:.1f}%)")
    
    # Contagem total de dados
    total_skills = sum(len(d.get('skills', [])) for d in dwarves)
    total_attributes = sum(len(d.get('attributes', {})) for d in dwarves)
    total_equipment = sum(len(d.get('equipment', [])) for d in dwarves)
    total_wounds = sum(len(d.get('wounds', [])) for d in dwarves)
    
    total_data_points = len(dwarves) + total_skills + total_attributes + total_equipment + total_wounds
    
    print(f"\nESTATÍSTICAS GERAIS:")
    print(f"   Total de anões: {len(dwarves)}")
    print(f"   Total de habilidades registradas: {total_skills}")
    print(f"   Total de atributos registrados: {total_attributes}")
    print(f"   Total de equipamentos registrados: {total_equipment}")
    print(f"   Total de ferimentos registrados: {total_wounds}")
    print(f"   TOTAL DE PONTOS DE DADOS: {total_data_points:,}")
    
    print("\nAnálise concluída com sucesso!")

if __name__ == "__main__":
    try:
        analyze_json_simple()
    except Exception as e:
        print(f"Erro na análise: {e}")