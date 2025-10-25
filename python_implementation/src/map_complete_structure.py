#!/usr/bin/env python3
"""
Mapeamento completo da estrutura de dados dos dwarfs
"""
import json
from collections import defaultdict, Counter
import statistics

def analyze_complete_structure():
    with open(r'C:\Users\Eduardo\Documents\projetinhos\Dwarf-Therapist\exports\complete_dwarves_data_20251025_135840.json') as f:
        data = json.load(f)
    
    print("🗺️  MAPEAMENTO COMPLETO DA ESTRUTURA DE DADOS")
    print("="*80)
    
    # 1. METADATA ANALYSIS
    print("\n📋 1. METADATA:")
    print("-" * 40)
    metadata = data.get('metadata', {})
    for key, value in metadata.items():
        if isinstance(value, dict):
            print(f"  {key}:")
            for k, v in value.items():
                print(f"    {k}: {v}")
        else:
            print(f"  {key}: {value}")
    
    # 2. DWARF STRUCTURE ANALYSIS
    dwarfs = data.get('dwarves', [])
    print(f"\n👥 2. DWARFS STRUCTURE ({len(dwarfs)} dwarfs):")
    print("-" * 40)
    
    if not dwarfs:
        print("❌ No dwarfs found!")
        return
    
    # Analyze first dwarf to understand structure
    sample_dwarf = dwarfs[0]
    
    def analyze_field(obj, path="", level=0):
        """Recursively analyze object structure"""
        indent = "  " * level
        
        if isinstance(obj, dict):
            for key, value in obj.items():
                current_path = f"{path}.{key}" if path else key
                
                if isinstance(value, (dict, list)) and value:
                    print(f"{indent}{key}: {type(value).__name__}")
                    analyze_field(value, current_path, level + 1)
                else:
                    value_type = type(value).__name__
                    if isinstance(value, (int, float)):
                        print(f"{indent}{key}: {value_type} = {value}")
                    elif isinstance(value, str):
                        truncated = value[:30] + "..." if len(value) > 30 else value
                        print(f"{indent}{key}: {value_type} = '{truncated}'")
                    else:
                        print(f"{indent}{key}: {value_type} = {value}")
        
        elif isinstance(obj, list):
            if obj:
                print(f"{indent}[0]: {type(obj[0]).__name__}")
                if isinstance(obj[0], dict):
                    analyze_field(obj[0], f"{path}[0]", level + 1)
                else:
                    print(f"{indent}  Sample: {obj[0]}")
                
                if len(obj) > 1:
                    print(f"{indent}... (+{len(obj)-1} more items)")
    
    print("ESTRUTURA COMPLETA (sample do primeiro dwarf):")
    analyze_field(sample_dwarf)
    
    # 3. UNIQUE VALUES ANALYSIS
    print(f"\n🔍 3. ANÁLISE DE VALORES ÚNICOS:")
    print("-" * 40)
    
    # Collect all simple field values
    simple_fields = {}
    
    for dwarf in dwarfs:
        for key, value in dwarf.items():
            if not isinstance(value, (dict, list)):
                if key not in simple_fields:
                    simple_fields[key] = []
                simple_fields[key].append(value)
    
    # Analyze unique values
    for field, values in simple_fields.items():
        unique_values = list(set(values))
        unique_count = len(unique_values)
        total_count = len(values)
        
        if unique_count <= 20:  # Show fields with few unique values
            value_counts = Counter(values)
            print(f"\n{field}: {unique_count} valores únicos de {total_count}")
            for value, count in value_counts.most_common(10):
                percentage = (count / total_count) * 100
                print(f"  {value}: {count} ({percentage:.1f}%)")
        else:
            if isinstance(unique_values[0], (int, float)):
                try:
                    min_val = min(values)
                    max_val = max(values)
                    avg_val = statistics.mean(values)
                    print(f"\n{field}: {unique_count} valores únicos - Range: {min_val} to {max_val} (avg: {avg_val:.1f})")
                except:
                    print(f"\n{field}: {unique_count} valores únicos")
            else:
                print(f"\n{field}: {unique_count} valores únicos")
    
    # 4. COMPLEX STRUCTURES ANALYSIS
    print(f"\n🏗️  4. ESTRUTURAS COMPLEXAS:")
    print("-" * 40)
    
    # Skills analysis
    all_skills = []
    for dwarf in dwarfs:
        skills = dwarf.get('skills', [])
        all_skills.extend(skills)
    
    if all_skills:
        print(f"\nSKILLS ({len(all_skills)} total skills):")
        skill_ids = [s.get('id') for s in all_skills if s.get('id') is not None]
        skill_id_counts = Counter(skill_ids)
        print(f"  Skill IDs únicos: {len(skill_id_counts)}")
        print("  Top 10 skills mais comuns:")
        for skill_id, count in skill_id_counts.most_common(10):
            print(f"    ID {skill_id}: {count} dwarfs")
        
        # Skill levels
        skill_levels = [s.get('level') for s in all_skills if s.get('level') is not None]
        if skill_levels:
            print(f"  Níveis: {min(skill_levels)} a {max(skill_levels)} (média: {statistics.mean(skill_levels):.1f})")
    
    # Attributes analysis
    all_phys_attrs = []
    all_ment_attrs = []
    
    for dwarf in dwarfs:
        phys_attrs = dwarf.get('physical_attributes', [])
        ment_attrs = dwarf.get('mental_attributes', [])
        all_phys_attrs.extend(phys_attrs)
        all_ment_attrs.extend(ment_attrs)
    
    if all_phys_attrs:
        print(f"\nPHYSICAL ATTRIBUTES ({len(all_phys_attrs)} total):")
        phys_values = [a.get('value') for a in all_phys_attrs if a.get('value') is not None]
        if phys_values:
            print(f"  Valores: {min(phys_values)} a {max(phys_values)} (média: {statistics.mean(phys_values):.1f})")
    
    if all_ment_attrs:
        print(f"\nMENTAL ATTRIBUTES ({len(all_ment_attrs)} total):")
        ment_values = [a.get('value') for a in all_ment_attrs if a.get('value') is not None]
        if ment_values:
            print(f"  Valores: {min(ment_values)} a {max(ment_values)} (média: {statistics.mean(ment_values):.1f})")
    
    # Labors analysis
    all_labors = []
    for dwarf in dwarfs:
        labors = dwarf.get('labors', [])
        all_labors.extend(labors)
    
    if all_labors:
        print(f"\nLABORS ({len(all_labors)} total):")
        labor_ids = [l.get('id') for l in all_labors if l.get('id') is not None]
        labor_counts = Counter(labor_ids)
        print(f"  Labor IDs únicos: {len(labor_counts)}")
        print("  Top 10 labors mais comuns:")
        for labor_id, count in labor_counts.most_common(10):
            print(f"    ID {labor_id}: {count} dwarfs")
    
    # Wounds analysis
    all_wounds = []
    for dwarf in dwarfs:
        wounds = dwarf.get('wounds', [])
        all_wounds.extend(wounds)
    
    if all_wounds:
        print(f"\nWOUNDS ({len(all_wounds)} total):")
        if all_wounds:
            sample_wound = all_wounds[0]
            print("  Estrutura de ferimento:")
            analyze_field(sample_wound, level=1)
    
    # Equipment analysis
    all_equipment = []
    for dwarf in dwarfs:
        equipment = dwarf.get('equipment', [])
        all_equipment.extend(equipment)
    
    if all_equipment:
        print(f"\nEQUIPMENT ({len(all_equipment)} total):")
        if all_equipment:
            sample_equipment = all_equipment[0]
            print("  Estrutura de equipamento:")
            analyze_field(sample_equipment, level=1)
    
    # 5. GROUPING SUGGESTIONS
    print(f"\n📊 5. SUGESTÕES DE AGRUPAMENTO:")
    print("-" * 40)
    
    # Group by profession
    professions = [d.get('profession') for d in dwarfs]
    prof_counts = Counter(professions)
    print(f"\nPor PROFESSION ({len(prof_counts)} diferentes):")
    for prof, count in prof_counts.most_common(10):
        print(f"  Profession {prof}: {count} dwarfs")
    
    # Group by age ranges
    ages = [d.get('age') for d in dwarfs if d.get('age') is not None]
    if ages:
        age_ranges = {
            'Jovem (0-20)': len([a for a in ages if 0 <= a <= 20]),
            'Adulto (21-50)': len([a for a in ages if 21 <= a <= 50]),
            'Maduro (51-100)': len([a for a in ages if 51 <= a <= 100]),
            'Idoso (100+)': len([a for a in ages if a > 100])
        }
        print(f"\nPor IDADE:")
        for range_name, count in age_ranges.items():
            print(f"  {range_name}: {count} dwarfs")
    
    # Group by skill count
    skill_counts = [len(d.get('skills', [])) for d in dwarfs]
    skill_ranges = {
        'Sem skills (0)': len([s for s in skill_counts if s == 0]),
        'Poucos skills (1-5)': len([s for s in skill_counts if 1 <= s <= 5]),
        'Skills médios (6-15)': len([s for s in skill_counts if 6 <= s <= 15]),
        'Muitos skills (16+)': len([s for s in skill_counts if s >= 16])
    }
    print(f"\nPor QUANTIDADE DE SKILLS:")
    for range_name, count in skill_ranges.items():
        print(f"  {range_name}: {count} dwarfs")
    
    print(f"\n🎯 RESUMO ESTRUTURAL:")
    print("-" * 40)
    print(f"✅ Estrutura completa mapeada com {len(dwarfs)} dwarfs")
    print(f"✅ Campos simples: {len(simple_fields)} diferentes")
    print(f"✅ Estruturas complexas: skills, attributes, labors, wounds, equipment")
    print(f"✅ Múltiplas opções de agrupamento identificadas")

if __name__ == "__main__":
    analyze_complete_structure()