import json
from collections import Counter

data = json.load(open('exports/complete_dwarves_data_20251118_225240.json', encoding='utf-8'))

types = []
for d in data['dwarves']:
    if '_decoded' in d and d['_decoded'].get('equipment'):
        for eq in d['_decoded']['equipment']:
            types.append(eq['item_type']['type_name'])

counts = Counter(types)
print('=' * 50)
print('EQUIPMENT TYPES FOUND')
print('=' * 50)
for name, count in sorted(counts.items(), key=lambda x: -x[1]):
    print(f'{count:4d}x {name}')
print('=' * 50)
print(f'Total: {len(types)} items, {len(counts)} unique types')
