import json

data = json.load(open('exports/complete_dwarves_data_20251118_232709.json', encoding='utf-8'))

eq = [item for d in data['dwarves'] 
      if d.get('_decoded', {}).get('equipment') 
      for item in d['_decoded']['equipment']]

print('Sample equipment with materials:')
print(json.dumps(eq[0], indent=2))

with_materials = [e for e in eq if 'material' in e]
print(f'\n{len(with_materials)} items have material info out of {len(eq)} total')

if with_materials:
    print('\nSample materials found:')
    for item in with_materials[:5]:
        if 'material' in item:
            mat = item['material']
            item_name = item['item_type']['type_name']
            print(f"  {item_name}: {mat['name']} ({mat['category']})")
