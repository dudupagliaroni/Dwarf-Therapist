import json
data = json.load(open('exports/complete_dwarves_data_20251118_225240.json', encoding='utf-8'))
d = data['dwarves'][0]
print('Keys:', list(d.keys()))
print('Has _decoded:', '_decoded' in d)
if '_decoded' in d:
    print('_decoded keys:', list(d['_decoded'].keys()))
    if 'equipment' in d['_decoded']:
        print('Sample decoded equipment:', d['_decoded']['equipment'][0] if d['_decoded']['equipment'] else 'None')
