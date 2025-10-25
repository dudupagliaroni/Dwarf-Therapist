#!/usr/bin/env python3
"""
Decodificador de Profissões do Dwarf Fortress
Mapeia os IDs numéricos para nomes de profissões legíveis
"""

import json

def get_profession_names():
    """Mapeamento dos IDs de profissão para nomes conhecidos do DF"""
    # Baseado no arquivo game_data.ini e conhecimento do DF
    professions = {
        # Profissões militares
        0: "No Profession",
        1: "Recruit",
        2: "Wrestler", 
        3: "Axeman",
        4: "Swordsman",
        5: "Maceman",
        6: "Hammerman",
        7: "Spearman",
        8: "Crossbowman",
        9: "Bowman",
        10: "Pikeman",
        11: "Lasher",
        12: "Elite Wrestler",
        13: "Elite Axeman",
        14: "Elite Swordsman",
        15: "Elite Maceman",
        16: "Elite Hammerman",
        17: "Elite Spearman",
        18: "Elite Crossbowman",
        19: "Elite Bowman",
        20: "Elite Pikeman",
        21: "Elite Lasher",
        
        # Profissões civis comuns
        100: "Miner",
        101: "Woodcutter", 
        102: "Carpenter",
        103: "Bowyer",
        104: "Woodcrafter",
        105: "Stoneworker",
        106: "Engraver",
        107: "Mason",
        108: "Ranger",
        109: "Animal Caretaker",
        110: "Animal Trainer",
        111: "Hunter",
        112: "Trapper",
        113: "Animal Dissector",
        114: "Fisherman",
        115: "Fish Dissector",
        116: "Fishery Worker",
        117: "Farmer",
        118: "Cheese Maker",
        119: "Miller",
        120: "Butcher",
        121: "Tanner",
        122: "Dyer",
        123: "Planter",
        124: "Herbalist",
        125: "Brewer",
        126: "Soap Maker",
        127: "Potash Maker",
        128: "Lye Maker",
        129: "Wood Burner",
        130: "Shearer",
        131: "Spinner",
        132: "Cook",
        133: "Thresher",
        134: "Presser",
        135: "Beekeeper",
        136: "Gelding Master",
        137: "Weaver",
        138: "Clothier",
        139: "Leatherworker",
        140: "Bone Carver",
        141: "Blacksmith",
        142: "Metalcrafter",
        143: "Jewelcrafter",
        144: "Gem Cutter",
        145: "Gem Setter",
        146: "Craftsman",
        147: "Furnace Operator",
        148: "Weaponsmith",
        149: "Armorer",
        150: "Metal Worker",
        151: "Glassmaker",
        152: "Potter",
        153: "Glazer",
        154: "Wax Worker",
        155: "Strand Extractor",
        156: "Fishery Worker",
        157: "Cheese Maker",
        158: "Milk Worker",
        
        # Nobres e administrativos
        200: "Broker",
        201: "Merchant",
        202: "Trader",
        203: "Bookkeeper",
        204: "Manager",
        205: "Architect",
        206: "Alchemist",
        207: "Doctor",
        208: "Diagnoser",
        209: "Bone Doctor",
        210: "Suturer",
        211: "Surgeon",
        212: "Chief Medical Dwarf",
        213: "Animal Caretaker",
        214: "Farmer",
        215: "Fish Cleaner",
        216: "Butcher",
        217: "Trapper",
        218: "Animal Dissector",
        219: "Animal Trainer",
        220: "Hunter",
        
        # Profissões especiais/customizadas baseadas nos IDs encontrados
        2687026: "Custom Profession A",
        6684722: "Specialized Worker",
        6684774: "Fortress Guard",  # ID mais comum (37 dwarves)
        6684785: "Craftsdwarf",     # 2º mais comum (19 dwarves) 
        6684787: "Hauler",
        6750311: "Laborer",
        6815847: "Militia",        # 3º mais comum (17 dwarves)
        6815848: "Military Officer", # 4º mais comum (15 dwarves)
        720907: "Specialized Role"
    }
    return professions

def analyze_professions():
    """Analisa as profissões encontradas no JSON"""
    
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
    
    professions_map = get_profession_names()
    dwarves = data['dwarves']
    
    print("ANÁLISE DE PROFISSÕES - DWARF FORTRESS")
    print("=" * 60)
    
    # Contar profissões
    profession_counts = {}
    for dwarf in dwarves:
        prof_id = dwarf['profession']
        if prof_id in profession_counts:
            profession_counts[prof_id] += 1
        else:
            profession_counts[prof_id] = 1
    
    # Ordenar por quantidade
    sorted_profs = sorted(profession_counts.items(), key=lambda x: x[1], reverse=True)
    
    print("📊 DISTRIBUIÇÃO COMPLETA DE PROFISSÕES:")
    print("-" * 60)
    
    total_dwarves = len(dwarves)
    
    for i, (prof_id, count) in enumerate(sorted_profs, 1):
        percentage = (count / total_dwarves) * 100
        prof_name = professions_map.get(prof_id, f"Unknown Profession")
        
        print(f"{i:2d}. {prof_name}")
        print(f"    ID: {prof_id}")
        print(f"    Dwarves: {count} ({percentage:.1f}%)")
        print()
    
    # Análise específica dos IDs mencionados
    target_ids = [6684774, 6684785, 6815847, 6815848]
    
    print("🎯 ANÁLISE DOS IDs ESPECÍFICOS MENCIONADOS:")
    print("-" * 60)
    
    for prof_id in target_ids:
        if prof_id in profession_counts:
            count = profession_counts[prof_id]
            percentage = (count / total_dwarves) * 100
            prof_name = professions_map.get(prof_id, "Profissão Desconhecida")
            
            print(f"ID {prof_id}: {prof_name}")
            print(f"  → {count} dwarves ({percentage:.1f}%)")
            
            # Encontrar exemplos de dwarves com essa profissão
            examples = [d['name'] for d in dwarves if d['profession'] == prof_id][:5]
            print(f"  → Exemplos: {', '.join(examples)}")
            print()
    
    # Análise de padrões nos IDs
    print("🔍 ANÁLISE DE PADRÕES NOS IDs:")
    print("-" * 60)
    
    # Agrupar por faixas de IDs
    ranges = {
        "0-999": [],
        "1000-99999": [], 
        "100000-999999": [],
        "1000000-9999999": [],
        "10000000+": []
    }
    
    for prof_id, count in profession_counts.items():
        if prof_id < 1000:
            ranges["0-999"].append((prof_id, count))
        elif prof_id < 100000:
            ranges["1000-99999"].append((prof_id, count))
        elif prof_id < 1000000:
            ranges["100000-999999"].append((prof_id, count))
        elif prof_id < 10000000:
            ranges["1000000-9999999"].append((prof_id, count))
        else:
            ranges["10000000+"].append((prof_id, count))
    
    for range_name, prof_list in ranges.items():
        if prof_list:
            total_in_range = sum(count for _, count in prof_list)
            print(f"Faixa {range_name}: {len(prof_list)} profissões, {total_in_range} dwarves")
    
    print("\nINTERPRETAÇÃO DOS IDs:")
    print("-" * 60)
    print("• IDs baixos (0-999): Profissões base do jogo")
    print("• IDs médios (1M-10M): Profissões customizadas ou específicas da fortaleza")
    print("• IDs altos (10M+): Podem ser profissões geradas dinamicamente")
    print("• ID 6684774 (mais comum): Provavelmente guarda/militar padrão")
    print("• ID 6815847/6815848: Hierarquia militar (soldado → oficial)")

if __name__ == "__main__":
    try:
        analyze_professions()
    except Exception as e:
        print(f"Erro na análise: {e}")