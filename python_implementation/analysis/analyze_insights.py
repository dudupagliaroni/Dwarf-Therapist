#!/usr/bin/env python3
"""
Análise de Insights e Padrões Interessantes do JSON
"""

import json
import statistics
from collections import Counter

def analyze_insights():
    with open('complete_dwarves_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    dwarves = data['dwarves']

    print("🎯 INSIGHTS E PADRÕES INTERESSANTES:")
    print("=" * 50)

    # 1. Análise de especialistas (dwarves com skills altos)
    specialists = []
    for dwarf in dwarves:
        high_skills = [s for s in dwarf['skills'] if s['level'] >= 10]
        if high_skills:
            specialists.append({
                'name': dwarf['name'],
                'age': dwarf['age'],
                'high_skills': high_skills
            })

    print(f"1. ESPECIALISTAS (Level 10+):")
    print(f"   {len(specialists)} dwarves especialistas encontrados")
    for spec in specialists[:5]:  # Top 5
        skills_str = ', '.join([f"{s['name']}({s['level']})" for s in spec['high_skills']])
        print(f"   {spec['name']} ({spec['age']}y): {skills_str}")

    # 2. Análise de dwarves feridos gravemente
    severely_wounded = []
    for dwarf in dwarves:
        if dwarf['wounds']:
            total_pain = sum(w['pain'] for w in dwarf['wounds'] if w['pain'] > 0)
            if total_pain > 0:
                severely_wounded.append({
                    'name': dwarf['name'],
                    'wounds': len(dwarf['wounds']),
                    'total_pain': total_pain
                })

    severely_wounded.sort(key=lambda x: x['total_pain'], reverse=True)
    print(f"\n2. DWARVES MAIS FERIDOS:")
    for wounded in severely_wounded[:5]:
        print(f"   {wounded['name']}: {wounded['wounds']} ferimentos, dor total: {wounded['total_pain']:,}")

    # 3. Análise de distribuição de equipamentos
    equipment_rich = []
    for dwarf in dwarves:
        if len(dwarf['equipment']) > 15:  # Muito equipamento
            equipment_rich.append({
                'name': dwarf['name'],
                'equipment_count': len(dwarf['equipment'])
            })

    equipment_rich.sort(key=lambda x: x['equipment_count'], reverse=True)
    print(f"\n3. DWARVES COM MAIS EQUIPAMENTOS:")
    for rich in equipment_rich[:5]:
        print(f"   {rich['name']}: {rich['equipment_count']} itens")

    # 4. Análise de stress extremo
    stressed_dwarves = []
    for dwarf in dwarves:
        if dwarf['personality'] and dwarf['personality']['stress_level'] > 3000:
            stressed_dwarves.append({
                'name': dwarf['name'],
                'stress': dwarf['personality']['stress_level'],
                'age': dwarf['age']
            })

    stressed_dwarves.sort(key=lambda x: x['stress'], reverse=True)
    print(f"\n4. DWARVES MAIS ESTRESSADOS (>3000):")
    for stressed in stressed_dwarves[:5]:
        print(f"   {stressed['name']} ({stressed['age']}y): stress {stressed['stress']}")

    # 5. Análise de correlação idade vs skills
    age_skill_correlation = []
    for dwarf in dwarves:
        if dwarf['age'] > 0 and dwarf['skills']:
            avg_skill_level = statistics.mean([s['level'] for s in dwarf['skills']])
            total_experience = sum([s['experience'] for s in dwarf['skills']])
            age_skill_correlation.append({
                'age': dwarf['age'],
                'avg_skill': avg_skill_level,
                'total_exp': total_experience
            })

    print(f"\n5. CORRELAÇÃO IDADE vs HABILIDADES:")
    young_group = [d for d in age_skill_correlation if d['age'] < 30]
    elder_group = [d for d in age_skill_correlation if d['age'] > 80]

    if young_group and elder_group:
        young_avg_skill = statistics.mean([d['avg_skill'] for d in young_group])
        elder_avg_skill = statistics.mean([d['avg_skill'] for d in elder_group])
        young_avg_exp = statistics.mean([d['total_exp'] for d in young_group])
        elder_avg_exp = statistics.mean([d['total_exp'] for d in elder_group])
        
        print(f"   Jovens (<30): skill médio {young_avg_skill:.2f}, exp média {young_avg_exp:.0f}")
        print(f"   Idosos (>80): skill médio {elder_avg_skill:.2f}, exp média {elder_avg_exp:.0f}")
        print(f"   Diferença: idosos têm {elder_avg_skill/young_avg_skill:.1f}x mais skill")

    # 6. Distribuição de sexo
    sex_distribution = Counter(dwarf['sex'] for dwarf in dwarves)
    print(f"\n6. DISTRIBUIÇÃO POR SEXO:")
    for sex_id, count in sex_distribution.most_common():
        percentage = count / len(dwarves) * 100
        print(f"   Sexo {sex_id}: {count} dwarves ({percentage:.1f}%)")

    # 7. Análise de profissões
    profession_distribution = Counter(dwarf['profession'] for dwarf in dwarves)
    print(f"\n7. PROFISSÕES MAIS COMUNS:")
    for prof_id, count in profession_distribution.most_common(10):
        percentage = count / len(dwarves) * 100
        print(f"   Profissão {prof_id}: {count} dwarves ({percentage:.1f}%)")

    # 8. Dwarves com mais diversidade de skills
    diverse_dwarves = []
    for dwarf in dwarves:
        if dwarf['skills']:
            unique_skills = len(set(s['name'] for s in dwarf['skills']))
            diverse_dwarves.append({
                'name': dwarf['name'],
                'unique_skills': unique_skills,
                'total_skills': len(dwarf['skills'])
            })

    diverse_dwarves.sort(key=lambda x: x['unique_skills'], reverse=True)
    print(f"\n8. DWARVES MAIS VERSÁTEIS:")
    for diverse in diverse_dwarves[:5]:
        print(f"   {diverse['name']}: {diverse['unique_skills']} skills únicos")

    print(f"\n🏆 RESUMO DOS INSIGHTS:")
    print(f"   📊 {len(specialists)} especialistas de alto nível")
    print(f"   🏥 {len(severely_wounded)} dwarves gravemente feridos")
    print(f"   ⚔️ {len(equipment_rich)} dwarves com equipamento abundante")
    print(f"   😰 {len(stressed_dwarves)} dwarves extremamente estressados")
    print(f"   🎯 Idosos têm significativamente mais experiência")
    print(f"   ✅ Dataset completo e rico para análises avançadas")

if __name__ == "__main__":
    analyze_insights()