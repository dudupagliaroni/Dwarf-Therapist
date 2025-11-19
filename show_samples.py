import json

data = json.load(open('exports/complete_dwarves_data_20251118_225240.json', encoding='utf-8'))

print('=' * 60)
print('SAMPLE EQUIPMENT WITH FULL DETAILS')
print('=' * 60)

# Find dwarf with varied equipment
for d in data['dwarves']:
    if '_decoded' in d and len(d.get('equipment', [])) >= 5:
        print(f"\nDwarf: {d['name']}")
        print('-' * 60)
        for eq in d['_decoded']['equipment'][:8]:  # Show first 8 items
            item = eq['item_type']['display_text']
            quality = eq['quality']['display_text']
            wear = eq['wear']['display_text']
            mat_type = eq['raw_values']['material_type']
            print(f"  {item:15s} | Quality: {quality:10s} | Wear: {wear:15s} | Mat: {mat_type}")
        break
