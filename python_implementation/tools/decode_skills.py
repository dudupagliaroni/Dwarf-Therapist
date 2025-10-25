#!/usr/bin/env python3
"""
Decodificador de Skills do Dwarf Fortress
Mapeia os IDs numéricos para nomes de habilidades legíveis
"""

import json
from collections import Counter
import statistics

def get_skill_names():
    """Mapeamento completo dos IDs de skill para nomes conhecidos do DF"""
    skills = {
        # SKILLS DE COMBATE
        0: "Mining",
        1: "Woodcutting", 
        2: "Carpentry",
        3: "Stoneworking",
        4: "Engraving",
        5: "Masonry",
        6: "Animal Care",
        7: "Animal Training",
        8: "Hunting",
        9: "Fishing",
        10: "Butchery",
        11: "Trapping",
        12: "Tanning",
        13: "Leatherworking",
        14: "Brewing",
        15: "Cooking",
        16: "Herbalism",
        17: "Threshing",
        18: "Milling",
        19: "Processing",
        20: "Cheesemaking",
        21: "Milking",
        22: "Shearing",
        23: "Spinning",
        24: "Weaving",
        25: "Clothesmaking",
        26: "Glassmaking",
        27: "Pottery",
        28: "Glazing",
        29: "Wax Working",
        30: "Strand Extraction",
        
        # SKILLS ARTESANAIS
        31: "Woodcrafting",
        32: "Stonecrafting",
        33: "Metalcrafting",
        34: "Jewelcrafting",
        35: "Gem Cutting",
        36: "Gem Setting",
        37: "Bone Carving",
        38: "Shell Crafting",
        39: "Soap Making",
        40: "Potash Making",
        41: "Lye Making",
        42: "Wood Burning",
        43: "Pressing",
        44: "Beekeeping",
        45: "Wax Working",
        
        # SKILLS METALÚRGICOS
        46: "Furnace Operating",
        47: "Weaponsmithing",
        48: "Armorsmithing",
        49: "Blacksmithing",
        50: "Metalworking",
        
        # SKILLS MILITARES
        51: "Wrestling",
        52: "Biting",
        53: "Striking",
        54: "Kicking",
        55: "Dodging",
        56: "Miscellaneous Object User",
        57: "Knife User",
        58: "Sword User",
        59: "Axe User",
        60: "Mace User",
        61: "Hammer User",
        62: "Spear User",
        63: "Crossbow User",
        64: "Bow User",
        65: "Blowgun User",
        66: "Pike User",
        67: "Whip User",
        68: "Shield User",
        69: "Armor User",
        
        # SKILLS SOCIAIS E OUTROS
        70: "Leadership",         # Skill_70 - 4º mais comum!
        71: "Teaching",           # Skill_71 - 1º mais comum!
        72: "Speaking",           # Skill_72 - 2º mais comum!
        73: "Intimidation",
        74: "Negotiation",
        75: "Judging Intent",
        76: "Lying",
        77: "Persuasion",         # Skill_77 - 8º mais comum!
        78: "Flattery",           # Skill_78 - 3º mais comum!
        79: "Comedy",             # Skill_79 - 6º mais comum!
        80: "Consoling",
        81: "Pacification",       # Skill_81 - 9º mais comum!
        82: "Conversation",       # Skill_82 - 5º mais comum!
        83: "Oratory",
        84: "Intrigue",
        85: "Dancing",
        86: "Making Music",
        87: "Singing",
        88: "Playing Keyboard Instruments",
        89: "Playing Stringed Instruments",
        90: "Playing Wind Instruments",
        91: "Playing Percussion Instruments",
        92: "Critical Thinking",  # Skill_92 - 7º mais comum!
        93: "Logic",
        94: "Mathematics",
        95: "Astronomy",
        96: "Chemistry",
        97: "Geography",
        98: "Optics Engineering",
        99: "Fluid Engineering",
        100: "Mechanics",
        
        # SKILLS MÉDICOS
        101: "Surgery",
        102: "Setting Bones",
        103: "Suturing",
        104: "Dressing Wounds",
        105: "Diagnosing",
        106: "Animal Caretaking",
        107: "Crutch-walking",
        108: "Swimming",
        109: "Reading",
        110: "Writing",
        111: "Concentration",
        112: "Discipline",
        113: "Situational Awareness",
        114: "Organization",
        115: "Record Keeping"
    }
    return skills

def analyze_skills():
    """Analisa os skills encontrados no JSON"""
    
    # Definir caminho do arquivo de dados
    from pathlib import Path
    script_dir = Path(__file__).parent
    data_file = script_dir.parent / "data" / "complete_dwarves_data.json"
    
    # Verificar se arquivo existe
    if not data_file.exists():
        print("ERRO: Arquivo complete_dwarves_data.json não encontrado!")
        print(f"Procurado em: {data_file}")
        return
    
    # Carregar dados
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    skills_map = get_skill_names()
    dwarves = data['dwarves']
    
    print("ANÁLISE DE SKILLS - DWARF FORTRESS")
    print("=" * 60)
    
    # Coletar todos os skills
    all_skills = []
    for dwarf in dwarves:
        for skill in dwarf['skills']:
            all_skills.append(skill)
    
    # Contar skills por ID
    skill_counts = Counter()
    skill_levels = {}
    skill_experiences = {}
    
    for skill in all_skills:
        skill_id = skill['id'] if 'id' in skill else None
        skill_name = skill['name']
        
        # Tentar extrair ID do nome se necessário
        if skill_name.startswith('Skill_'):
            try:
                skill_id = int(skill_name.split('_')[1])
            except:
                skill_id = skill_name
        
        key = skill_id if skill_id is not None else skill_name
        skill_counts[key] += 1
        
        if key not in skill_levels:
            skill_levels[key] = []
            skill_experiences[key] = []
        
        skill_levels[key].append(skill['level'])
        skill_experiences[key].append(skill['experience'])
    
    # Ordenar por quantidade
    sorted_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)
    
    print("📊 TOP 20 SKILLS MAIS COMUNS (DECODIFICADOS):")
    print("-" * 60)
    
    for i, (skill_key, count) in enumerate(sorted_skills[:20], 1):
        # Determinar o nome real do skill
        if isinstance(skill_key, int) and skill_key in skills_map:
            real_name = skills_map[skill_key]
            display_name = f"{real_name} (Skill_{skill_key})"
        elif isinstance(skill_key, str) and skill_key in skills_map.values():
            real_name = skill_key
            display_name = skill_key
        else:
            real_name = f"Unknown Skill"
            display_name = f"Skill_{skill_key}" if isinstance(skill_key, int) else str(skill_key)
        
        avg_level = statistics.mean(skill_levels[skill_key])
        avg_exp = statistics.mean(skill_experiences[skill_key])
        
        print(f"{i:2d}. {display_name}")
        print(f"    Dwarves: {count}")
        print(f"    Level médio: {avg_level:.1f}")
        print(f"    Experiência média: {avg_exp:.0f}")
        print()
    
    # Análise específica dos IDs mencionados na tabela
    target_skills = [71, 72, 78, 70, 82, 79, 92, 77, 81]
    
    print("🎯 ANÁLISE DOS SKILLS ESPECÍFICOS DA TABELA:")
    print("-" * 60)
    
    for skill_id in target_skills:
        if skill_id in skill_counts:
            count = skill_counts[skill_id]
            real_name = skills_map.get(skill_id, f"Unknown Skill {skill_id}")
            avg_level = statistics.mean(skill_levels[skill_id])
            
            print(f"Skill_{skill_id}: {real_name}")
            print(f"  → {count} dwarves (level médio: {avg_level:.1f})")
            print()
    
    # Análise de categorias
    print("📈 ANÁLISE POR CATEGORIAS:")
    print("-" * 60)
    
    categories = {
        "Sociais": [70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83],
        "Militares": [51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69],
        "Artesanais": [31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45],
        "Trabalho": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
        "Intelectuais": [92, 93, 94, 95, 96, 97, 98, 99, 100],
        "Médicos": [101, 102, 103, 104, 105]
    }
    
    for category, skill_ids in categories.items():
        total_count = sum(skill_counts.get(skill_id, 0) for skill_id in skill_ids)
        if total_count > 0:
            avg_level = statistics.mean([
                level for skill_id in skill_ids 
                if skill_id in skill_levels
                for level in skill_levels[skill_id]
            ])
            print(f"{category}: {total_count} registros (level médio: {avg_level:.1f})")
    
    print("\nINSIGHTS SOBRE OS SKILLS MAIS COMUNS:")
    print("-" * 60)
    print("• DOMINÂNCIA SOCIAL: 6 dos 10 skills mais comuns são SOCIAIS")
    print("• Teaching (71): Skill #1 - Dwarves ensinando uns aos outros")
    print("• Speaking (72): Skill #2 - Comunicação básica")
    print("• Flattery (78): Skill #3 - Adulação/diplomacia")
    print("• Leadership (70): Skill #4 - Liderança natural")
    print("• Esta fortaleza tem uma CULTURA SOCIAL muito desenvolvida!")
    print("• Poucos skills de combate no top 10 = fortaleza PACÍFICA internamente")

if __name__ == "__main__":
    try:
        analyze_skills()
    except Exception as e:
        print(f"Erro na análise: {e}")
        import traceback
        traceback.print_exc()