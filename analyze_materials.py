import json
from collections import Counter

data = json.load(open('exports/complete_dwarves_data_20251118_232709.json', encoding='utf-8'))

eq = [item for d in data['dwarves'] 
      if d.get('_decoded', {}).get('equipment') 
      for item in d['_decoded']['equipment']]

# Count by category
categories = Counter([item['material']['category'] for item in eq if 'material' in item])
print("Material Categories:")
for cat, count in sorted(categories.items()):
    print(f"  {cat}: {count}")

# Show unique material names
materials = Counter([item['material']['name'] for item in eq if 'material' in item])
print(f"\nUnique materials: {len(materials)}")
print("\nMost common materials:")
for mat, count in materials.most_common(10):
    print(f"  {count:4d}x {mat}")

# Check if any resolved to real names
real_names = [m for m in materials.keys() if not m.startswith(('creature_', 'plant_', 'inorganic_', 'mat_'))]
print(f"\nResolved material names: {len(real_names)}")
if real_names:
    for name in real_names[:10]:
        print(f"  - {name}")
