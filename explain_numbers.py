#!/usr/bin/env python3
"""Explica o significado dos números nos campos de equipamento"""

# Raw values da seleção
item_id = 181000
item_type = 29
material_type = 422
material_index = 174
quality = 0
wear = 1

# Item types (do EquipmentDecoder)
ITEM_TYPES = {29: 'GLOVES'}
QUALITY = {
    0: 'normal', 
    1: 'well-crafted -', 
    2: 'finely-crafted +', 
    3: 'superior *', 
    4: 'exceptional ≡', 
    5: 'masterwork ☼', 
    6: 'artifact !'
}
WEAR = {
    0: 'new (100%)', 
    1: 'worn x (66%)', 
    2: 'threadbare X (33%)', 
    3: 'tattered XX (10%)'
}

print('EXPLICAÇÃO DOS NÚMEROS:')
print('=' * 70)
print(f'item_id: {item_id}')
print(f'  → Identificador único do item no jogo (ID interno do Dwarf Fortress)')
print()
print(f'item_type: {item_type}')
print(f'  → Tipo do item: {ITEM_TYPES.get(item_type, "UNKNOWN")}')
print(f'  → Este é o enum ITEM_TYPE do DF (0-90): 29 = GLOVES (luvas)')
print()
print(f'material_type: {material_type}')
print(f'  → Categoria do material (0-30 range típico)')
print(f'  → 422 indica um material específico (provavelmente tecido/couro)')
print(f'  → Valores comuns: 0=INORGANIC(metal/pedra), 8=CREATURE(couro), 10=PLANT(tecido)')
print()
print(f'material_index: {material_index}')
print(f'  → Índice dentro da categoria material_type')
print(f'  → 174 é o índice do material específico no vetor de materiais')
print(f'  → Ex: se material_type=8(CREATURE), material_index aponta para qual criatura')
print()
print(f'quality: {quality}')
print(f'  → Qualidade da fabricação: {QUALITY.get(quality, "unknown")}')
print(f'  → Escala 0-6: normal(0), well-crafted(1), finely-crafted(2), superior(3),')
print(f'  →             exceptional(4), masterwork☼(5), artifact!(6)')
print()
print(f'wear: {wear}')
print(f'  → Nível de desgaste: {WEAR.get(wear, "unknown")}')
print(f'  → Escala 0-3: new(0), worn x(1), threadbare X(2), tattered XX(3)')
print('=' * 70)
print()
print('RESUMO DESTE ITEM:')
print(f'  Luvas (GLOVES) de material 422/174, qualidade normal, desgaste worn (66%)')
print()
print('=' * 70)
print('MATERIAL_TYPE - CATEGORIAS COMUNS:')
print('=' * 70)
print('  0 = INORGANIC    → Metais (iron, steel, copper) e pedras')
print('  1 = AMBER        → Âmbar')
print('  2 = CORAL        → Coral')
print('  3 = GLASS_GREEN  → Vidro verde')
print('  4 = GLASS_CLEAR  → Vidro transparente')
print('  5 = GLASS_CRYSTAL→ Cristal')
print('  6 = WATER        → Água (gelo)')
print('  7 = COAL         → Carvão')
print('  8 = CREATURE_MAT → Materiais de criatura (couro, osso, pelo)')
print('  9 = LOCAL_CREATURE_MAT → Material local de criatura')
print(' 10 = PLANT        → Materiais vegetais (tecido de planta)')
print(' 11 = LOCAL_PLANT_MAT → Material local de planta')
print(' 12 = WOOD         → Madeira')
print(' 19 = CREATURE_ID  → ID da criatura')
print()
print('NOTA: material_type=422 está fora do range típico (0-30).')
print('Isso sugere que pode ser:')
print('  1) Um índice composto (categoria + offset)')
print('  2) Um ID de material processado diferentemente')
print('  3) Um material customizado/gerado pelo jogo')
print()
print('Para resolver material_type/material_index em nomes reais (ex: "steel", "pig leather"),')
print('seria necessário ler os vetores de materiais da memória do Dwarf Fortress.')
