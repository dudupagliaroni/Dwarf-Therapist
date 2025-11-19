import json

# Carrega os dados
with open('exports/complete_dwarves_data_20251118_220207.json', encoding='utf-8') as f:
    data = json.load(f)

# Verifica primeiro dwarf
dwarf = data['dwarves'][0]
print(f"Nome: {dwarf['name']}")
print(f"squad_id: {dwarf['squad_id']}")
print(f"squad_position: {dwarf['squad_position']}")
print(f"pet_owner_id: {dwarf['pet_owner_id']}")

# Verifica equipamentos
print(f"\nEquipamento (primeiros 3):")
for eq in dwarf.get('equipment', [])[:3]:
    item_type = eq.get('item_type_decoded', eq.get('item_type', 'desconhecido'))
    print(f"  {item_type}: quality={eq['quality']}, wear={eq['wear']}")

# Verifica ferimentos
print(f"\nFerimentos (primeiros 3):")
for w in dwarf.get('wounds', [])[:3]:
    print(f"  {w['body_part']}: pain={w['pain']}")

# Estatísticas gerais
print(f"\n=== ESTATÍSTICAS ===")
squad_count = sum(1 for d in data['dwarves'] if d['squad_id'] != -1)
pet_owner_count = sum(1 for d in data['dwarves'] if d['pet_owner_id'] != -1)
print(f"Total de dwarves: {len(data['dwarves'])}")
print(f"Dwarves em esquadrões: {squad_count}")
print(f"Dwarves donos de pets: {pet_owner_count}")
print(f"Dwarves civis (squad_id=-1): {len(data['dwarves']) - squad_count}")
