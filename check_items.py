import json
from collections import Counter

with open('exports/complete_dwarves_data_20251118_225240.json', encoding='utf-8') as f:
    data = json.load(f)

types = []
for dwarf in data['dwarves']:
    if dwarf.get('equipment'):
        for item in dwarf['equipment']:
            if '_decoded' in item:
                types.append(item['_decoded']['type_name'])

counts = Counter(types)
print('Equipment Types Found:')
print('=' * 40)
for name, count in counts.most_common():
    print(f'{count:4d}x {name}')
print('=' * 40)
print(f'Total: {len(types)} items, {len(counts)} unique types')
