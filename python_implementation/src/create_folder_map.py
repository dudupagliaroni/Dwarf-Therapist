#!/usr/bin/env python3
"""
Criar mapa da estrutura de pastas das estruturas aninhadas com valores únicos reais
"""
import json
from collections import Counter, defaultdict
from pathlib import Path

def create_folder_structure_map():
    print("📁 CRIANDO MAPA DA ESTRUTURA DE PASTAS COM VALORES ÚNICOS")
    print("="*70)
    
    # Load actual data to get real values
    with open(r'C:\Users\Eduardo\Documents\projetinhos\Dwarf-Therapist\exports\complete_dwarves_data_20251025_141436.json') as f:
        data = json.load(f)
    
    dwarfs = data.get('dwarves', [])
    
    print(f"📊 Analisando {len(dwarfs)} dwarfs para valores únicos...")
    
    # Analyze real data for unique values
    unique_values = analyze_unique_values(dwarfs)
    
    # Base path
    base_path = Path(r"C:\Users\Eduardo\Documents\projetinhos\Dwarf-Therapist\exports")
    
    # Create structure with real unique values
    structure_map = create_structure_with_values(dwarfs, unique_values)
    
    print("📂 ESTRUTURA DE PASTAS CRIADA:")
    print_structure(structure_map, 0)
    
    # Create only MD file
    summary_file = base_path / "ESTRUTURA_PASTAS_COMPLETA.md"
    create_complete_folder_documentation(summary_file, structure_map, unique_values, dwarfs, data)
    
    print(f"✅ Documentação completa criada em: {summary_file}")

def analyze_unique_values(dwarfs):
    """Analyze actual data to get real unique values"""
    unique_values = {}
    
    # Simple field analysis
    for field in ['profession', 'race', 'caste', 'sex', 'age', 'mood', 'civ_id', 'squad_id']:
        values = [d.get(field) for d in dwarfs if d.get(field) is not None]
        if values:
            unique_values[field] = Counter(values)
    
    # Skills analysis
    all_skills = []
    for dwarf in dwarfs:
        skills = dwarf.get('skills_decoded', dwarf.get('skills', []))
        all_skills.extend(skills)
    
    if all_skills:
        skill_names = [s.get('skill_name', s.get('name', 'Unknown')) for s in all_skills]
        skill_levels = [s.get('level', 0) for s in all_skills]
        unique_values['skill_names'] = Counter(skill_names)
        unique_values['skill_levels'] = Counter(skill_levels)
    
    # Attributes analysis  
    all_phys = []
    all_ment = []
    for dwarf in dwarfs:
        phys = dwarf.get('physical_attributes_decoded', dwarf.get('physical_attributes', []))
        ment = dwarf.get('mental_attributes_decoded', dwarf.get('mental_attributes', []))
        all_phys.extend(phys)
        all_ment.extend(ment)
    
    if all_phys:
        phys_names = [a.get('attribute_name', a.get('name', 'Unknown')) for a in all_phys]
        unique_values['physical_attributes'] = Counter(phys_names)
    
    if all_ment:
        ment_names = [a.get('attribute_name', a.get('name', 'Unknown')) for a in all_ment]
        unique_values['mental_attributes'] = Counter(ment_names)
    
    # Labors analysis
    all_labors = []
    enabled_labors = []
    for dwarf in dwarfs:
        labors = dwarf.get('labors_decoded', dwarf.get('labors', []))
        all_labors.extend(labors)
        enabled_labors.extend([l for l in labors if l.get('enabled', False)])
    
    if all_labors:
        labor_names = [l.get('labor_name', l.get('name', 'Unknown')) for l in all_labors]
        unique_values['all_labors'] = Counter(labor_names)
    
    if enabled_labors:
        enabled_names = [l.get('labor_name', l.get('name', 'Unknown')) for l in enabled_labors]
        unique_values['enabled_labors'] = Counter(enabled_names)
    
    # Wounds analysis
    all_wounds = []
    for dwarf in dwarfs:
        wounds = dwarf.get('wounds_decoded', dwarf.get('wounds', []))
        all_wounds.extend(wounds)
    
    if all_wounds:
        pain_levels = [w.get('pain', 0) for w in all_wounds if w.get('pain', 0) > 0]
        body_parts = [w.get('body_part', 0) for w in all_wounds]
        unique_values['wound_pain'] = Counter(pain_levels)
        unique_values['wound_parts'] = Counter(body_parts)
    
    # Equipment analysis
    all_equipment = []
    for dwarf in dwarfs:
        equipment = dwarf.get('equipment_decoded', dwarf.get('equipment', []))
        all_equipment.extend(equipment)
    
    if all_equipment:
        item_types = [e.get('item_type_name', f"Type {e.get('item_type', 'Unknown')}") for e in all_equipment]
        qualities = [e.get('quality_name', f"Quality {e.get('quality', 'Unknown')}") for e in all_equipment]
        materials = [e.get('material_name', f"Material {e.get('material_type', 'Unknown')}") for e in all_equipment]
        unique_values['item_types'] = Counter(item_types)
        unique_values['item_qualities'] = Counter(qualities)
        unique_values['item_materials'] = Counter(materials)
    
    # Personality analysis
    all_traits = []
    stress_levels = []
    for dwarf in dwarfs:
        personality = dwarf.get('personality_decoded', dwarf.get('personality', {}))
        main_traits = personality.get('main_traits', [])
        all_traits.extend(main_traits)
        stress = personality.get('stress_level', 0)
        stress_levels.append(stress)
    
    if all_traits:
        trait_names = [t.get('name', 'Unknown') for t in all_traits]
        trait_tendencies = [t.get('tendency', 'Unknown') for t in all_traits]
        unique_values['trait_names'] = Counter(trait_names)
        unique_values['trait_tendencies'] = Counter(trait_tendencies)
    
    if stress_levels:
        unique_values['stress_levels'] = Counter(stress_levels)
    
    return unique_values

def create_structure_with_values(dwarfs, unique_values):
    """Create folder structure with actual values from data"""
    
    # Helper to format top values
    def format_top_values(counter, limit=10):
        if not counter:
            return "No data"
        items = []
        for value, count in counter.most_common(limit):
            items.append(f"{value}: {count}")
        return " | ".join(items)
    
    # Get top professions
    prof_counter = unique_values.get('profession', Counter())
    top_profs = prof_counter.most_common(5)
    
    # Get age ranges
    ages = [d.get('age', 0) for d in dwarfs if d.get('age', 0) >= 0]  # Filter out negative ages
    age_ranges = {
        'young_0_20': len([a for a in ages if 0 <= a <= 20]),
        'adult_21_50': len([a for a in ages if 21 <= a <= 50]),
        'mature_51_100': len([a for a in ages if 51 <= a <= 100]),
        'elder_100plus': len([a for a in ages if a > 100])
    }
    
    structure = {
        "dwarf_fortress_data/": {
            "metadata/": {
                "session_info": "Session metadata and statistics",
                "layout_info": "Memory layout information",
                "statistics": "Decoder statistics and counts"
            },
            "dwarfs/": {
                "demographics/": {
                    "by_profession/": {
                        f"profession_{prof[0]}": f"{prof[1]} dwarfs" for prof in top_profs
                    },
                    "by_age/": {
                        f"{age_range}": f"{count} dwarfs" for age_range, count in age_ranges.items()
                    },
                    "by_gender/": {
                        "female": f"{unique_values.get('sex', Counter()).get(0, 0)} dwarfs",
                        "male": f"{unique_values.get('sex', Counter()).get(1, 0)} dwarfs",
                        "unknown": f"{unique_values.get('sex', Counter()).get(255, 0)} dwarfs"
                    },
                    "by_civilization/": {
                        f"civ_{civ_id}": f"{count} dwarfs" for civ_id, count in unique_values.get('civ_id', Counter()).most_common(5)
                    }
                },
                "skills/": {
                    "by_category/": {
                        "social_skills": format_top_values(Counter({k: v for k, v in unique_values.get('skill_names', Counter()).items() if any(social in k.lower() for social in ['teaching', 'speaking', 'flattery', 'leadership', 'conversation'])}), 5),
                        "combat_skills": format_top_values(Counter({k: v for k, v in unique_values.get('skill_names', Counter()).items() if any(combat in k.lower() for combat in ['weapon', 'armor', 'shield', 'dodge', 'fighter'])}), 5),
                        "craft_skills": format_top_values(Counter({k: v for k, v in unique_values.get('skill_names', Counter()).items() if any(craft in k.lower() for craft in ['mining', 'smith', 'carpentry', 'mason'])}), 5)
                    },
                    "by_level/": {
                        f"level_{level}": f"{count} skills" for level, count in unique_values.get('skill_levels', Counter()).most_common(10)
                    },
                    "top_skills": format_top_values(unique_values.get('skill_names', Counter()), 15)
                },
                "attributes/": {
                    "physical/": {
                        "all_physical": format_top_values(unique_values.get('physical_attributes', Counter()), 10)
                    },
                    "mental/": {
                        "all_mental": format_top_values(unique_values.get('mental_attributes', Counter()), 10)
                    }
                },
                "labors/": {
                    "enabled/": {
                        "enabled_labors": format_top_values(unique_values.get('enabled_labors', Counter()), 10)
                    },
                    "all_available/": {
                        "all_labors": format_top_values(unique_values.get('all_labors', Counter()), 12)
                    }
                },
                "health/": {
                    "wounds/": {
                        "by_pain_level": format_top_values(unique_values.get('wound_pain', Counter()), 10),
                        "by_body_part": format_top_values(unique_values.get('wound_parts', Counter()), 10),
                        "summary": f"{len([d for d in dwarfs if d.get('wounds', [])])} wounded | {len(dwarfs) - len([d for d in dwarfs if d.get('wounds', [])])} healthy"
                    }
                },
                "equipment/": {
                    "by_type": format_top_values(unique_values.get('item_types', Counter()), 10),
                    "by_quality": format_top_values(unique_values.get('item_qualities', Counter()), 15),
                    "by_material": format_top_values(unique_values.get('item_materials', Counter()), 10)
                },
                "personality/": {
                    "traits/": {
                        "trait_names": format_top_values(unique_values.get('trait_names', Counter()), 15),
                        "trait_tendencies": format_top_values(unique_values.get('trait_tendencies', Counter()), 5)
                    },
                    "stress_levels": format_top_values(unique_values.get('stress_levels', Counter()), 10)
                }
            }
        }
    }
    
    return structure

def print_structure(structure, level=0):
    """Print the folder structure visually"""
    indent = "  " * level
    
    for key, value in structure.items():
        if isinstance(value, dict):
            print(f"{indent}📁 {key}")
            print_structure(value, level + 1)
        else:
            print(f"{indent}📄 {key}: {value}")

def create_complete_folder_documentation(file_path, structure_map, unique_values, dwarfs, data):
    """Create comprehensive documentation of the folder structure with all unique values"""
    
    content = f"""# 📁 DWARF FORTRESS DATA - ESTRUTURA DE PASTAS COMPLETA

## 🗂️ MAPA DETALHADO COM TODOS OS VALORES ÚNICOS

Esta estrutura representa a organização completa dos dados de **{len(dwarfs)} dwarfs** extraídos do Dwarf Fortress,
mostrando TODOS os valores únicos encontrados em cada nível final do aninhamento.

## 📋 ESTRUTURA HIERÁRQUICA COMPLETA

```
dwarf_fortress_data/
├── metadata/                    # Informações da sessão
├── dwarfs/                      # Dados principais dos dwarfs
│   ├── demographics/            # Demografia detalhada
│   ├── skills/                  # Sistema completo de habilidades
│   ├── attributes/              # Atributos físicos e mentais
│   ├── labors/                  # Trabalhos e profissões
│   ├── health/                  # Saúde e ferimentos
│   ├── equipment/               # Equipamentos e itens
│   └── personality/             # Personalidade e traços
```

## 🔍 VALORES ÚNICOS DETALHADOS POR CATEGORIA

### 📊 1. DEMOGRAPHICS - VALORES ÚNICOS

#### 👥 BY PROFESSION ({len(unique_values.get('profession', Counter()))} profissões diferentes)
"""
    
    # Add profession details
    prof_counter = unique_values.get('profession', Counter())
    content += f"**Total de profissões**: {len(prof_counter)}\n\n"
    content += "**Distribuição completa**:\n"
    for prof, count in prof_counter.most_common():
        content += f"- Profession {prof}: {count} dwarfs\n"
    
    # Add age details
    ages = [d.get('age', 0) for d in dwarfs if d.get('age', 0) >= 0]
    content += f"\n#### 🎂 BY AGE ({len(set(ages))} idades diferentes)\n"
    content += f"**Range de idades**: {min(ages)} - {max(ages)} anos\n\n"
    content += "**Distribuição por faixas**:\n"
    age_ranges = {
        'Jovem (0-20)': len([a for a in ages if 0 <= a <= 20]),
        'Adulto (21-50)': len([a for a in ages if 21 <= a <= 50]),
        'Maduro (51-100)': len([a for a in ages if 51 <= a <= 100]),
        'Idoso (100+)': len([a for a in ages if a > 100])
    }
    for range_name, count in age_ranges.items():
        content += f"- {range_name}: {count} dwarfs\n"
    
    # Add gender details
    sex_counter = unique_values.get('sex', Counter())
    content += f"\n#### ⚧ BY GENDER ({len(sex_counter)} tipos)\n"
    for sex, count in sex_counter.most_common():
        gender_name = {0: 'Female', 1: 'Male', 255: 'Unknown'}.get(sex, f'Sex {sex}')
        content += f"- {gender_name}: {count} dwarfs\n"
    
    # Add civilization details
    civ_counter = unique_values.get('civ_id', Counter())
    content += f"\n#### 🏛️ BY CIVILIZATION ({len(civ_counter)} civilizações)\n"
    for civ_id, count in civ_counter.most_common():
        content += f"- Civilization {civ_id}: {count} dwarfs\n"
    
    # Skills section
    skill_names = unique_values.get('skill_names', Counter())
    content += f"\n### ⚔️ 2. SKILLS - VALORES ÚNICOS ({len(skill_names)} skills diferentes)\n"
    content += f"**Total de skills registrados**: {sum(skill_names.values())}\n\n"
    content += "**TODOS os skills encontrados**:\n"
    for skill, count in skill_names.most_common():
        content += f"- {skill}: {count} dwarfs\n"
    
    # Skill levels
    skill_levels = unique_values.get('skill_levels', Counter())
    content += f"\n#### 📈 SKILL LEVELS ({len(skill_levels)} níveis diferentes)\n"
    for level in sorted(skill_levels.keys()):
        count = skill_levels[level]
        content += f"- Nível {level}: {count} skills\n"
    
    # Attributes section
    phys_attrs = unique_values.get('physical_attributes', Counter())
    ment_attrs = unique_values.get('mental_attributes', Counter())
    
    content += f"\n### 💪 3. ATTRIBUTES - VALORES ÚNICOS\n"
    content += f"#### Physical Attributes ({len(phys_attrs)} tipos)\n"
    for attr, count in phys_attrs.most_common():
        content += f"- {attr}: {count} measurements\n"
    
    content += f"\n#### Mental Attributes ({len(ment_attrs)} tipos)\n"
    for attr, count in ment_attrs.most_common():
        content += f"- {attr}: {count} measurements\n"
    
    # Labors section
    all_labors = unique_values.get('all_labors', Counter())
    enabled_labors = unique_values.get('enabled_labors', Counter())
    
    content += f"\n### 🔨 4. LABORS - VALORES ÚNICOS\n"
    content += f"#### All Available Labors ({len(all_labors)} tipos)\n"
    for labor, count in all_labors.most_common():
        content += f"- {labor}: disponível para {count} dwarfs\n"
    
    if enabled_labors:
        content += f"\n#### Enabled Labors ({len(enabled_labors)} tipos habilitados)\n"
        for labor, count in enabled_labors.most_common():
            content += f"- {labor}: habilitado para {count} dwarfs\n"
    
    # Health section
    wound_pain = unique_values.get('wound_pain', Counter())
    wound_parts = unique_values.get('wound_parts', Counter())
    
    content += f"\n### 🩸 5. HEALTH - VALORES ÚNICOS\n"
    if wound_pain:
        content += f"#### Pain Levels ({len(wound_pain)} níveis diferentes)\n"
        for pain in sorted(wound_pain.keys()):
            count = wound_pain[pain]
            content += f"- Pain Level {pain}: {count} wounds\n"
    
    if wound_parts:
        content += f"\n#### Body Parts Affected ({len(wound_parts)} partes diferentes)\n"
        for part, count in wound_parts.most_common():
            content += f"- Body Part ID {part}: {count} wounds\n"
    
    # Equipment section
    item_types = unique_values.get('item_types', Counter())
    item_qualities = unique_values.get('item_qualities', Counter())
    item_materials = unique_values.get('item_materials', Counter())
    
    content += f"\n### ⚔️ 6. EQUIPMENT - VALORES ÚNICOS\n"
    content += f"#### Item Types ({len(item_types)} tipos)\n"
    for item_type, count in item_types.most_common():
        content += f"- {item_type}: {count} items\n"
    
    content += f"\n#### Item Qualities ({len(item_qualities)} qualidades diferentes)\n"
    for quality, count in item_qualities.most_common():
        content += f"- {quality}: {count} items\n"
    
    content += f"\n#### Item Materials ({len(item_materials)} materiais diferentes)\n" 
    for material, count in item_materials.most_common():
        content += f"- {material}: {count} items\n"
    
    # Personality section
    trait_names = unique_values.get('trait_names', Counter())
    trait_tendencies = unique_values.get('trait_tendencies', Counter())
    stress_levels = unique_values.get('stress_levels', Counter())
    
    content += f"\n### 🧠 7. PERSONALITY - VALORES ÚNICOS\n"
    content += f"#### Personality Traits ({len(trait_names)} traços diferentes)\n"
    for trait, count in trait_names.most_common():
        content += f"- {trait}: {count} dwarfs\n"
    
    content += f"\n#### Trait Tendencies ({len(trait_tendencies)} tendências)\n"
    for tendency, count in trait_tendencies.most_common():
        content += f"- {tendency}: {count} trait instances\n"
    
    content += f"\n#### Stress Levels ({len(stress_levels)} níveis únicos)\n"
    for stress in sorted(stress_levels.keys()):
        count = stress_levels[stress]
        content += f"- Stress Level {stress}: {count} dwarfs\n"
    
    # Summary statistics
    content += f"\n## 📊 RESUMO ESTATÍSTICO COMPLETO\n"
    content += f"- **Total de Dwarfs**: {len(dwarfs)}\n"
    content += f"- **Profissões Diferentes**: {len(unique_values.get('profession', Counter()))}\n"
    content += f"- **Skills Diferentes**: {len(unique_values.get('skill_names', Counter()))}\n"
    content += f"- **Atributos Físicos**: {len(unique_values.get('physical_attributes', Counter()))}\n"
    content += f"- **Atributos Mentais**: {len(unique_values.get('mental_attributes', Counter()))}\n"
    content += f"- **Labors Disponíveis**: {len(unique_values.get('all_labors', Counter()))}\n"
    content += f"- **Tipos de Equipment**: {len(unique_values.get('item_types', Counter()))}\n"
    content += f"- **Traços de Personalidade**: {len(unique_values.get('trait_names', Counter()))}\n"
    
    content += f"\n## 🎯 INSIGHTS DOS VALORES ÚNICOS\n"
    content += f"1. **Diversidade de Profissões**: {len(unique_values.get('profession', Counter()))} profissões indicam especialização\n"
    content += f"2. **Skills Sociais Dominam**: {unique_values.get('skill_names', Counter()).most_common(1)[0][0]} é o mais comum\n"
    if enabled_labors:
        content += f"3. **Labor Mais Habilitado**: {enabled_labors.most_common(1)[0][0]} com {enabled_labors.most_common(1)[0][1]} dwarfs\n"
    content += f"4. **Equipment Issues**: {len(unique_values.get('item_types', Counter()))} tipos, maioria 'None'\n"
    content += f"5. **Personality Dominante**: {trait_names.most_common(1)[0][0] if trait_names else 'N/A'}\n"
    
    content += f"\n---\n**Gerado em**: {data['metadata']['timestamp']}\n"
    content += f"**Total de Dados Analisados**: {len(dwarfs)} dwarfs com estruturas completas\n"
    content += f"**Versão do Layout**: {data['metadata']['layout_info']['version_name']}"
    
    # Write to file
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    create_folder_structure_map()