#!/usr/bin/env python3
"""
Material Type/Index Decoder - Based on DFInstance::find_material()

This explains the material_type ranges used by Dwarf Fortress.
Reference: src/dfinstance.cpp lines 1397-1420
"""

def explain_material_system():
    """
    Explains the material_type/material_index system from Dwarf Fortress
    """
    
    print("=" * 80)
    print("DWARF FORTRESS MATERIAL SYSTEM")
    print("=" * 80)
    print()
    print("The material_type field uses RANGES to determine material category:")
    print()
    
    ranges = [
        {
            'range': 'mat_type < 0',
            'category': 'INVALID',
            'lookup': 'get_raw_material(mat_type)',
            'description': 'Invalid material type',
            'examples': []
        },
        {
            'range': 'mat_type == 0',
            'category': 'INORGANIC',
            'lookup': 'get_inorganic_material(mat_index)',
            'description': 'Inorganic materials (metals, stones, gems)',
            'examples': ['IRON (26)', 'COPPER (25)', 'SILVER (22)', 'GOLD (21)', 
                        'STEEL (8)', 'MARBLE (12)', 'OBSIDIAN (78)']
        },
        {
            'range': '0 < mat_type < 19',
            'category': 'RAW_MATERIALS',
            'lookup': 'get_raw_material(mat_type)',
            'description': 'Built-in material types (amber, coral, glass, etc.)',
            'examples': [
                '1 = AMBER',
                '2 = CORAL', 
                '3 = GLASS_GREEN',
                '4 = GLASS_CLEAR',
                '5 = GLASS_CRYSTAL',
                '6 = WATER (ice)',
                '7 = COAL',
                '12 = WOOD (generic)'
            ]
        },
        {
            'range': '19 <= mat_type < 219',
            'category': 'CREATURE_MATERIALS',
            'lookup': 'race(mat_index).get_creature_material(mat_type - 19)',
            'description': 'Materials from creatures (leather, bone, shell, hair)',
            'examples': [
                'mat_index = race ID (dwarf, cow, pig, etc.)',
                'mat_type - 19 = material within that creature',
                'Example: Pig leather, cow bone, spider silk'
            ]
        },
        {
            'range': '219 <= mat_type < 419',
            'category': 'HISTORICAL_FIGURE_MATERIALS', 
            'lookup': 'hist_figure(mat_index).race.get_creature_material(mat_type - 219)',
            'description': 'Materials from specific historical figures',
            'examples': [
                'Items made from named historical figures',
                'Example: "Urist McDwarf\'s leather"'
            ]
        },
        {
            'range': '419 <= mat_type < 619',
            'category': 'PLANT_MATERIALS',
            'lookup': 'plant(mat_index).get_plant_material(mat_type - 419)',
            'description': 'Materials from plants (wood, cloth, seeds, drinks)',
            'examples': [
                'mat_index = plant ID (plump helmet, cave wheat, etc.)',
                'mat_type - 419 = material within that plant',
                'Example: Pig tail cloth, plump helmet spawn'
            ]
        },
        {
            'range': 'mat_type >= 619',
            'category': 'UNKNOWN',
            'lookup': 'NULL',
            'description': 'Unknown/unsupported material types',
            'examples': []
        }
    ]
    
    for r in ranges:
        print(f"{'─' * 80}")
        print(f"RANGE: {r['range']}")
        print(f"CATEGORY: {r['category']}")
        print(f"{'─' * 80}")
        print(f"Lookup: {r['lookup']}")
        print(f"Description: {r['description']}")
        if r['examples']:
            print(f"\nExamples:")
            for ex in r['examples']:
                print(f"  • {ex}")
        print()
    
    return ranges


def decode_material_type(mat_type, mat_index):
    """
    Decode a specific material_type/material_index pair
    """
    print("=" * 80)
    print(f"DECODING: material_type={mat_type}, material_index={mat_index}")
    print("=" * 80)
    print()
    
    if mat_type < 0:
        category = "INVALID"
        lookup = f"get_raw_material({mat_type})"
        note = "This is an invalid material type"
        
    elif mat_type == 0:
        category = "INORGANIC" 
        lookup = f"get_inorganic_material({mat_index})"
        note = f"Look up inorganic material at index {mat_index} (metals, stones, gems)"
        
    elif mat_type < 19:
        category = "RAW_MATERIALS"
        lookup = f"get_raw_material({mat_type})"
        raw_names = {
            1: "AMBER", 2: "CORAL", 3: "GLASS_GREEN", 4: "GLASS_CLEAR",
            5: "GLASS_CRYSTAL", 6: "WATER", 7: "COAL", 12: "WOOD"
        }
        material_name = raw_names.get(mat_type, f"RAW_MAT_{mat_type}")
        note = f"Built-in material: {material_name}"
        
    elif mat_type < 219:
        category = "CREATURE_MATERIALS"
        creature_mat_index = mat_type - 19
        lookup = f"get_race({mat_index}).get_creature_material({creature_mat_index})"
        note = f"Material from creature (race_id={mat_index}), material #{creature_mat_index} within that creature"
        note += "\n       Examples: leather, bone, shell, hair, horn, hoof, chitin"
        
    elif mat_type < 419:
        category = "HISTORICAL_FIGURE_MATERIALS"
        creature_mat_index = mat_type - 219
        lookup = f"get_historical_figure({mat_index}).race.get_creature_material({creature_mat_index})"
        note = f"Material from historical figure (hist_fig_id={mat_index}), material #{creature_mat_index}"
        
    elif mat_type < 619:
        category = "PLANT_MATERIALS"
        plant_mat_index = mat_type - 419
        lookup = f"get_plant({mat_index}).get_plant_material({plant_mat_index})"
        note = f"Material from plant (plant_id={mat_index}), material #{plant_mat_index} within that plant"
        note += "\n       Examples: wood, thread/cloth, seeds, drink, oil, powder"
        
    else:
        category = "UNKNOWN"
        lookup = "NULL"
        note = "Material type out of known ranges"
    
    print(f"Category: {category}")
    print(f"Lookup:   {lookup}")
    print(f"Note:     {note}")
    print()
    
    return category, lookup


if __name__ == "__main__":
    # Show complete system
    explain_material_system()
    
    print("\n" + "=" * 80)
    print("ANALYZING YOUR SPECIFIC VALUES")
    print("=" * 80)
    print()
    
    # Decode specific values from user's equipment
    test_cases = [
        (422, 174),  # User's gloves
        (38, 308),   # User's pants
        (24, 0),     # Common armor material
        (0, 26),     # IRON (typical)
        (0, 8),      # STEEL (typical)
    ]
    
    for mat_type, mat_index in test_cases:
        decode_material_type(mat_type, mat_index)
        print()
