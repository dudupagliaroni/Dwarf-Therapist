#!/usr/bin/env python3
"""
Análise detalhada das estruturas aninhadas e valores únicos
"""
import json
from collections import defaultdict, Counter

def deep_structure_analysis():
    with open(r'C:\Users\Eduardo\Documents\projetinhos\Dwarf-Therapist\exports\complete_dwarves_data_20251025_135840.json') as f:
        data = json.load(f)
    
    dwarfs = data.get('dwarves', [])
    
    print("🔬 ANÁLISE DETALHADA DAS ESTRUTURAS ANINHADAS")
    print("="*80)
    
    # 1. SKILLS DEEP ANALYSIS
    print("\n⚔️  1. SKILLS - ANÁLISE PROFUNDA:")
    print("-" * 50)
    
    all_skills = []
    skill_by_dwarf = defaultdict(list)
    
    for dwarf in dwarfs:
        dwarf_id = dwarf.get('id')
        skills = dwarf.get('skills_decoded', dwarf.get('skills', []))
        skill_by_dwarf[dwarf_id] = skills
        all_skills.extend(skills)
    
    if all_skills:
        # Skill names frequency
        skill_names = Counter([s.get('skill_name', s.get('name', 'Unknown')) for s in all_skills])
        print(f"Top 15 skills mais comuns:")
        for skill_name, count in skill_names.most_common(15):
            print(f"  {skill_name}: {count} dwarfs")
        
        # Skill levels distribution
        skill_levels = Counter([s.get('level', 0) for s in all_skills])
        print(f"\nDistribuição de níveis de skill:")
        for level in sorted(skill_levels.keys())[:10]:
            count = skill_levels[level]
            print(f"  Nível {level}: {count} skills")
        
        # Experience ranges
        experiences = [s.get('experience', 0) for s in all_skills if s.get('experience', 0) > 0]
        if experiences:
            exp_ranges = {
                'Baixa (0-500)': len([e for e in experiences if 0 <= e <= 500]),
                'Média (501-2000)': len([e for e in experiences if 501 <= e <= 2000]),
                'Alta (2001-10000)': len([e for e in experiences if 2001 <= e <= 10000]),
                'Muito Alta (10000+)': len([e for e in experiences if e > 10000])
            }
            print(f"\nDistribuição de experiência:")
            for range_name, count in exp_ranges.items():
                print(f"  {range_name}: {count} skills")
    
    # 2. ATTRIBUTES DEEP ANALYSIS
    print("\n💪 2. ATTRIBUTES - ANÁLISE PROFUNDA:")
    print("-" * 50)
    
    all_phys_attrs = []
    all_ment_attrs = []
    
    for dwarf in dwarfs:
        phys = dwarf.get('physical_attributes_decoded', dwarf.get('physical_attributes', []))
        ment = dwarf.get('mental_attributes_decoded', dwarf.get('mental_attributes', []))
        all_phys_attrs.extend(phys)
        all_ment_attrs.extend(ment)
    
    if all_phys_attrs:
        print("ATRIBUTOS FÍSICOS:")
        phys_names = Counter([a.get('attribute_name', a.get('name', 'Unknown')) for a in all_phys_attrs])
        for attr_name, count in phys_names.most_common():
            print(f"  {attr_name}: {count} dwarfs")
        
        # Physical attribute ranges
        phys_values = [a.get('value', 0) for a in all_phys_attrs]
        phys_percentages = [a.get('percentage', 0) for a in all_phys_attrs if 'percentage' in a]
        
        if phys_percentages:
            phys_ranges = {
                'Muito Baixo (0-20%)': len([p for p in phys_percentages if 0 <= p <= 20]),
                'Baixo (21-40%)': len([p for p in phys_percentages if 21 <= p <= 40]),
                'Médio (41-60%)': len([p for p in phys_percentages if 41 <= p <= 60]),
                'Alto (61-80%)': len([p for p in phys_percentages if 61 <= p <= 80]),
                'Muito Alto (81-100%)': len([p for p in phys_percentages if 81 <= p <= 100])
            }
            print(f"  Distribuição de força (%):")
            for range_name, count in phys_ranges.items():
                print(f"    {range_name}: {count} atributos")
    
    if all_ment_attrs:
        print("\nATRIBUTOS MENTAIS:")
        ment_names = Counter([a.get('attribute_name', a.get('name', 'Unknown')) for a in all_ment_attrs])
        for attr_name, count in ment_names.most_common():
            print(f"  {attr_name}: {count} dwarfs")
    
    # 3. LABORS DEEP ANALYSIS
    print("\n🔨 3. LABORS - ANÁLISE PROFUNDA:")
    print("-" * 50)
    
    all_labors = []
    enabled_labors = []
    
    for dwarf in dwarfs:
        labors = dwarf.get('labors_decoded', dwarf.get('labors', []))
        all_labors.extend(labors)
        enabled_labors.extend([l for l in labors if l.get('enabled', False)])
    
    if all_labors:
        labor_names = Counter([l.get('labor_name', l.get('name', 'Unknown')) for l in all_labors])
        print(f"Todos os labors disponíveis:")
        for labor_name, count in labor_names.most_common():
            print(f"  {labor_name}: presente em {count} dwarfs")
        
        if enabled_labors:
            enabled_labor_names = Counter([l.get('labor_name', l.get('name', 'Unknown')) for l in enabled_labors])
            print(f"\nLabors HABILITADOS (top 10):")
            for labor_name, count in enabled_labor_names.most_common(10):
                print(f"  {labor_name}: {count} dwarfs")
    
    # 4. WOUNDS DEEP ANALYSIS
    print("\n🩸 4. WOUNDS - ANÁLISE PROFUNDA:")
    print("-" * 50)
    
    all_wounds = []
    dwarfs_with_wounds = 0
    
    for dwarf in dwarfs:
        wounds = dwarf.get('wounds_decoded', dwarf.get('wounds', []))
        if wounds:
            dwarfs_with_wounds += 1
            all_wounds.extend(wounds)
    
    print(f"Dwarfs com ferimentos: {dwarfs_with_wounds}/{len(dwarfs)}")
    
    if all_wounds:
        # Wound body parts
        body_parts = [w.get('body_part', 0) for w in all_wounds]
        body_part_counts = Counter(body_parts)
        print(f"Partes do corpo feridas (IDs):")
        for part_id, count in body_part_counts.most_common(10):
            print(f"  Parte {part_id}: {count} ferimentos")
        
        # Pain levels
        pain_levels = [w.get('pain', 0) for w in all_wounds if w.get('pain', 0) > 0]
        if pain_levels:
            pain_ranges = {
                'Leve (1-25)': len([p for p in pain_levels if 1 <= p <= 25]),
                'Moderada (26-50)': len([p for p in pain_levels if 26 <= p <= 50]),
                'Severa (51-100)': len([p for p in pain_levels if 51 <= p <= 100]),
                'Extrema (100+)': len([p for p in pain_levels if p > 100])
            }
            print(f"Níveis de dor:")
            for range_name, count in pain_ranges.items():
                print(f"  {range_name}: {count} ferimentos")
    
    # 5. EQUIPMENT DEEP ANALYSIS
    print("\n⚔️  5. EQUIPMENT - ANÁLISE PROFUNDA:")
    print("-" * 50)
    
    all_equipment = []
    dwarfs_with_equipment = 0
    
    for dwarf in dwarfs:
        equipment = dwarf.get('equipment_decoded', dwarf.get('equipment', []))
        if equipment:
            dwarfs_with_equipment += 1
            all_equipment.extend(equipment)
    
    print(f"Dwarfs com equipamentos: {dwarfs_with_equipment}/{len(dwarfs)}")
    
    if all_equipment:
        # Item types
        item_types = Counter([e.get('item_type_name', f"Type {e.get('item_type', 'Unknown')}") for e in all_equipment])
        print(f"Tipos de item (top 10):")
        for item_type, count in item_types.most_common(10):
            print(f"  {item_type}: {count} itens")
        
        # Materials
        materials = Counter([e.get('material_name', f"Material {e.get('material_type', 'Unknown')}") for e in all_equipment])
        print(f"\nMateriais (top 10):")
        for material, count in materials.most_common(10):
            print(f"  {material}: {count} itens")
        
        # Quality
        qualities = Counter([e.get('quality_name', f"Quality {e.get('quality', 'Unknown')}") for e in all_equipment])
        print(f"\nQualidades:")
        for quality, count in qualities.most_common():
            print(f"  {quality}: {count} itens")
    
    # 6. PERSONALITY DEEP ANALYSIS
    print("\n🧠 6. PERSONALITY - ANÁLISE PROFUNDA:")
    print("-" * 50)
    
    all_traits = []
    stress_levels = []
    focus_levels = []
    
    for dwarf in dwarfs:
        personality = dwarf.get('personality_decoded', dwarf.get('personality', {}))
        
        # Main traits
        main_traits = personality.get('main_traits', [])
        all_traits.extend(main_traits)
        
        # Stress and focus
        stress = personality.get('stress_level', 0)
        focus = personality.get('focus_level', 0)
        stress_levels.append(stress)
        focus_levels.append(focus)
    
    if all_traits:
        trait_names = Counter([t.get('name', 'Unknown') for t in all_traits])
        print(f"Traços de personalidade principais (top 15):")
        for trait_name, count in trait_names.most_common(15):
            print(f"  {trait_name}: {count} dwarfs")
        
        trait_tendencies = Counter([t.get('tendency', 'Unknown') for t in all_traits])
        print(f"\nTendências dos traços:")
        for tendency, count in trait_tendencies.most_common():
            print(f"  {tendency}: {count} traços")
    
    if stress_levels:
        stress_ranges = {
            'Sem Stress (0-100)': len([s for s in stress_levels if 0 <= s <= 100]),
            'Stress Baixo (101-1000)': len([s for s in stress_levels if 101 <= s <= 1000]),
            'Stress Médio (1001-5000)': len([s for s in stress_levels if 1001 <= s <= 5000]),
            'Stress Alto (5000+)': len([s for s in stress_levels if s > 5000])
        }
        print(f"\nNíveis de stress:")
        for range_name, count in stress_ranges.items():
            print(f"  {range_name}: {count} dwarfs")
    
    # 7. GROUPING RECOMMENDATIONS
    print("\n📋 7. RECOMENDAÇÕES DE AGRUPAMENTO:")
    print("-" * 50)
    
    print("🎯 AGRUPAMENTOS SUGERIDOS POR ESTRUTURA:")
    
    print("\nPor SKILLS:")
    print("  • Specialists: dwarfs com 1-3 skills de alto nível")
    print("  • Generalists: dwarfs com muitos skills de nível baixo/médio")
    print("  • Masters: dwarfs com skills nível 15+")
    print("  • Novatos: dwarfs com poucos skills baixos")
    
    print("\nPor LABORS:")
    print("  • Workers: muitos labors habilitados")
    print("  • Specialists: poucos labors específicos")
    print("  • Idle: poucos ou nenhum labor habilitado")
    
    print("\nPor ATRIBUTOS:")
    print("  • Strong: atributos físicos altos")
    print("  • Smart: atributos mentais altos")
    print("  • Balanced: atributos equilibrados")
    print("  • Weak: atributos baixos")
    
    print("\nPor ESTADO:")
    print("  • Healthy: sem ferimentos")
    print("  • Wounded: com ferimentos")
    print("  • Well-equipped: muito equipamento")
    print("  • Stressed: níveis altos de stress")
    
    print("\nPor EXPERIÊNCIA:")
    print("  • Veterans: idade alta + skills altos")
    print("  • Rookies: idade baixa + skills baixos")
    print("  • Migrants: flag migrant + skills médios")
    
    print(f"\n✅ ESTRUTURA COMPLETAMENTE MAPEADA!")
    print("🔍 Todas as estruturas aninhadas analisadas")
    print("📊 Valores únicos identificados para agrupamento")
    print("🎯 Múltiplas estratégias de categorização disponíveis")

if __name__ == "__main__":
    deep_structure_analysis()