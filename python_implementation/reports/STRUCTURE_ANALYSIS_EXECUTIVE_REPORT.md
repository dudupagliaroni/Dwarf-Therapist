# 📊 Relatório Executivo - Análise Estrutural de Dwarves

```
================================================================================
📊 RELATÓRIO EXECUTIVO - ANÁLISE ESTRUTURAL DE DWARVES
================================================================================

📁 Arquivo: complete_dwarves_data_20251118_214050.json
📏 Tamanho: 6.06 MB
⏰ Análise realizada em: 2025-11-18T21:45:04.265469

🔍 1. ESTRUTURA DE PRIMEIRO NÍVEL:
   Total de keys principais: 2
   ├── metadata
   ├── dwarves

📋 2. METADATA:
   ├── version: 2.0-COMPLETE
   ├── timestamp: 2025-10-25T02:00:00Z
   ├── dwarf_count: 243
   ├── base_address: 0x7ff692450000
   ├── pointer_size: 8
   ├── layout_info: {'checksum': '0x68d64ce7', 'version_name': 'v0.52.05 win64 STEAM', 'complete': 'true'}
   ├── decoded: True
   ├── statistics: {'total_skills_read': 6082, 'total_wounds_read': 151, 'total_equipment_read': 1799, 'dwarves_with_skills': 201, 'dwarves_with_wounds': 46, 'dwarves_with_equipment': 189}
   ├── decoder_version: 1.0

👥 3. ESTRUTURA DOS CAMPOS DE DWARF:
   Total de campos por dwarf: 43
   ├── Campos simples: 26
   ├── Objetos (dict): 4
   └── Arrays (list): 13

   🔹 CAMPOS SIMPLES (DETALHADO):
      ├── address (int): 1888841080896
      ├── age (int): 55
      ├── birth_time (int): 402135
      ├── birth_year (int): 70
      ├── blood_level (int): 5760
      ├── body_size (int): 6923
      ├── caste (int): 0
      ├── civ_id (int): 287
      ├── custom_profession (str): None
      ├── flags1 (int): 2147500033
      ├── flags2 (int): 301989952
      ├── flags3 (int): 258
      ├── happiness (int): 0
      ├── hist_id (int): 6897
      ├── id (int): 904
      ├── mood (int): -1
      ├── name (str): sodel
      ├── pet_owner_id (int): 4294967295
      ├── profession (int): 115
      ├── race (int): 572
      ├── sex (int): 0
      ├── soul_address (int): 1888747860784
      ├── squad_id (int): 4294967295
      ├── squad_position (int): 4294967295
      ├── temp_mood (int): -1
      ├── turn_count (int): 888099

   🔸 OBJETOS/ESTRUTURAS (DETALHADO):
      ├── counters (3 subkeys):
      │   └── counter1
      │   └── counter2
      │   └── counter3
      ├── decoded_info (7 subkeys):
      │   └── profession_name
      │   └── race_name
      │   └── caste_name
      │   └── gender
      │   └── mood_name
      │   └── happiness_level
      │   └── stress_level
      ├── personality (3 subkeys):
      │   └── traits
      │   └── stress_level
      │   └── focus_level
      ├── personality_decoded (6 subkeys):
      │   └── traits
      │   └── stress_level
      │   └── focus_level
      │   └── stress_description
      │   └── focus_description
      │   └── main_traits

   🔹 ARRAYS/LISTAS (DETALHADO):
      ├── equipment (10 elementos):
      │   └── Tipo de elemento: dict
      │   └── Estrutura do elemento: 6 keys
      │       • item_id
      │       • item_type
      │       • material_type
      │       • material_index
      │       • quality
      │       • wear
      ├── equipment_decoded (10 elementos):
      │   └── Tipo de elemento: dict
      │   └── Estrutura do elemento: 10 keys
      │       • item_id
      │       • item_type
      │       • material_type
      │       • material_index
      │       • quality
      │       • wear
      │       • material_name
      │       • item_type_name
      │       • quality_name
      │       • wear_description
      ├── labors (12 elementos):
      │   └── Tipo de elemento: dict
      │   └── Estrutura do elemento: 3 keys
      │       • id
      │       • enabled
      │       • name
      ├── labors_decoded (12 elementos):
      │   └── Tipo de elemento: dict
      │   └── Estrutura do elemento: 5 keys
      │       • id
      │       • enabled
      │       • name
      │       • labor_name
      │       • status
      ├── mental_attributes (7 elementos):
      │   └── Tipo de elemento: dict
      │   └── Estrutura do elemento: 4 keys
      │       • id
      │       • value
      │       • max_value
      │       • name
      ├── mental_attributes_decoded (7 elementos):
      │   └── Tipo de elemento: dict
      │   └── Estrutura do elemento: 7 keys
      │       • id
      │       • value
      │       • max_value
      │       • name
      │       • attribute_name
      │       • percentage
      │       • description
      ├── physical_attributes (6 elementos):
      │   └── Tipo de elemento: dict
      │   └── Estrutura do elemento: 4 keys
      │       • id
      │       • value
      │       • max_value
      │       • name
      ├── physical_attributes_decoded (6 elementos):
      │   └── Tipo de elemento: dict
      │   └── Estrutura do elemento: 7 keys
      │       • id
      │       • value
      │       • max_value
      │       • name
      │       • attribute_name
      │       • percentage
      │       • description
      ├── skills (31 elementos):
      │   └── Tipo de elemento: dict
      │   └── Estrutura do elemento: 4 keys
      │       • id
      │       • level
      │       • experience
      │       • name
      ├── skills_decoded (31 elementos):
      │   └── Tipo de elemento: dict
      │   └── Estrutura do elemento: 7 keys
      │       • id
      │       • level
      │       • experience
      │       • name
      │       • skill_name
      │       • level_name
      │       • experience_percentage
      ├── syndromes (0 elementos):
      │   └── Tipo de elemento: empty
      ├── wounds (0 elementos):
      │   └── Tipo de elemento: empty
      ├── wounds_decoded (0 elementos):
      │   └── Tipo de elemento: empty

🔗 4. RELACIONAMENTOS IDENTIFICADOS:
   📊 Pares Decoded encontrados: 7
      ├── skills ↔ skills_decoded
      ├── physical_attributes ↔ physical_attributes_decoded
      ├── mental_attributes ↔ mental_attributes_decoded
      ├── labors ↔ labors_decoded
      ├── wounds ↔ wounds_decoded
      ├── equipment ↔ equipment_decoded
      ├── personality ↔ personality_decoded

   🆔 Campos de ID: 5
      ├── id
      ├── hist_id
      ├── civ_id
      ├── squad_id
      ├── pet_owner_id

   🏗️ Estruturas Hierárquicas: 4
      ├── personality (com subestruturas)
      │   └── traits
      │   └── stress_level
      │   └── focus_level
      ├── counters 
      │   └── counter1
      │   └── counter2
      │   └── counter3
      ├── decoded_info 
      │   └── profession_name
      │   └── race_name
      │   └── caste_name
      │   └── gender
      │   └── mood_name
      │   └── ... (+2 mais)
      ├── personality_decoded (com subestruturas)
      │   └── traits
      │   └── stress_level
      │   └── focus_level
      │   └── stress_description
      │   └── focus_description
      │   └── ... (+1 mais)

📈 5. ESTATÍSTICAS GERAIS:
   Total de Dwarves: 243

   📊 Estatísticas de Arrays:
      ├── skills:
      │   ├── Min: 0 elementos
      │   ├── Max: 50 elementos
      │   ├── Média: 25.0 elementos
      │   └── Total: 6082 elementos
      ├── physical_attributes:
      │   ├── Min: 6 elementos
      │   ├── Max: 6 elementos
      │   ├── Média: 6.0 elementos
      │   └── Total: 1458 elementos
      ├── mental_attributes:
      │   ├── Min: 7 elementos
      │   ├── Max: 7 elementos
      │   ├── Média: 7.0 elementos
      │   └── Total: 1701 elementos
      ├── labors:
      │   ├── Min: 12 elementos
      │   ├── Max: 12 elementos
      │   ├── Média: 12.0 elementos
      │   └── Total: 2916 elementos
      ├── wounds:
      │   ├── Min: 0 elementos
      │   ├── Max: 18 elementos
      │   ├── Média: 0.6 elementos
      │   └── Total: 151 elementos
      ├── equipment:
      │   ├── Min: 0 elementos
      │   ├── Max: 19 elementos
      │   ├── Média: 7.4 elementos
      │   └── Total: 1799 elementos
      ├── syndromes:
      │   ├── Min: 0 elementos
      │   ├── Max: 1 elementos
      │   ├── Média: 0.1 elementos
      │   └── Total: 15 elementos
      ├── skills_decoded:
      │   ├── Min: 0 elementos
      │   ├── Max: 50 elementos
      │   ├── Média: 25.0 elementos
      │   └── Total: 6082 elementos
      ├── physical_attributes_decoded:
      │   ├── Min: 6 elementos
      │   ├── Max: 6 elementos
      │   ├── Média: 6.0 elementos
      │   └── Total: 1458 elementos
      ├── mental_attributes_decoded:
      │   ├── Min: 7 elementos
      │   ├── Max: 7 elementos
      │   ├── Média: 7.0 elementos
      │   └── Total: 1701 elementos
      ├── labors_decoded:
      │   ├── Min: 12 elementos
      │   ├── Max: 12 elementos
      │   ├── Média: 12.0 elementos
      │   └── Total: 2916 elementos
      ├── wounds_decoded:
      │   ├── Min: 0 elementos
      │   ├── Max: 18 elementos
      │   ├── Média: 0.6 elementos
      │   └── Total: 151 elementos
      ├── equipment_decoded:
      │   ├── Min: 0 elementos
      │   ├── Max: 19 elementos
      │   ├── Média: 7.4 elementos
      │   └── Total: 1799 elementos

   📋 Cobertura de Campos (% não-nulos):
      ├── id: 100.0% (243/243)
      ├── name: 100.0% (243/243)
      ├── profession: 100.0% (243/243)
      ├── race: 100.0% (243/243)
      ├── caste: 100.0% (243/243)
      ├── sex: 100.0% (243/243)
      ├── age: 100.0% (243/243)
      ├── birth_year: 100.0% (243/243)
      ├── birth_time: 100.0% (243/243)
      ├── mood: 100.0% (243/243)
      ├── temp_mood: 100.0% (243/243)
      ├── happiness: 100.0% (243/243)
      ├── flags1: 100.0% (243/243)
      ├── flags2: 100.0% (243/243)
      ├── flags3: 100.0% (243/243)

================================================================================
🎉 ANÁLISE ESTRUTURAL COMPLETADA COM SUCESSO!
================================================================================
```
