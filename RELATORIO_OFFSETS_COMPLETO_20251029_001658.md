# Relatório Comprehensivo de Offsets - Dwarf Therapist

**Gerado em:** 2025-10-29 00:16:58

## 📊 Estatísticas Expandidas

- **Total de seções:** 29
- **Total de offsets:** 353
- **Offsets com valores possíveis:** 5
- **Cobertura de análise:** 1.42%
- **Enums encontrados:** 10
- **Seções de game data:** 21

## 🎯 Principais Descobertas

### Offsets com Valores Mapeados

- **dwarf_offsets:** 4/52 offsets mapeados
- **emotion_offsets:** 1/7 offsets mapeados

**Total:** 2 seções com offsets mapeados

## 🔧 activity_offsets

**Total de offsets:** 13

| Offset | Hex | Dec | Tipo | Tamanho | Significado | Valores Possíveis | Exemplos |
|--------|-----|-----|------|---------|-------------|-------------------|----------|
| `activity_type` | `0x0004` | 4 | unknown | variable | Campo de dados para activity type |  |  |
| `events` | `0x0008` | 8 | unknown | variable | Campo de dados para events |  |  |
| `knowledge_category` | `0x00c0` | 192 | unknown | variable | Campo de dados para knowledge category |  |  |
| `knowledge_flag` | `0x00c4` | 196 | bool | 1 | Flag booleana indicando knowledge |  |  |
| `participants` | `0x0048` | 72 | unknown | variable | Campo de dados para participants |  |  |
| `perf_histfig` | `0x000c` | 12 | unknown | variable | Campo de dados para perf histfig |  |  |
| `perf_participants` | `0x00e0` | 224 | unknown | variable | Campo de dados para perf participants |  |  |
| `perf_type` | `0x00b0` | 176 | unknown | variable | Campo de dados para perf type |  |  |
| `pray_deity` | `0x00b0` | 176 | unknown | variable | Campo de dados para pray deity |  |  |
| `pray_sphere` | `0x00b4` | 180 | unknown | variable | Campo de dados para pray sphere |  |  |
| `sq_lead` | `0x00b4` | 180 | unknown | variable | Campo de dados para sq lead |  |  |
| `sq_skill` | `0x00bc` | 188 | unknown | variable | Campo de dados para sq skill |  |  |
| `sq_train_rounds` | `0x00c8` | 200 | unknown | variable | Campo de dados para sq train rounds |  |  |

### Detalhes dos Offsets


## 🔧 addresses

**Descrição:** Endereços globais fundamentais - ponteiros para estruturas principais do jogo

**Total de offsets:** 62

| Offset | Hex | Dec | Tipo | Tamanho | Significado | Valores Possíveis | Exemplos |
|--------|-----|-----|------|---------|-------------|-------------------|----------|
| `active_creature_vector` | `0x021960b8` | 35217592 | std::vector<> | 24 | Subconjunto de criaturas atualmente ativas/carregadas |  |  |
| `active_sites_vector` | `0x000483d0` | 295888 | std::vector<> | 24 | Vetor de sites ativos no mundo (fortalezas, cidades) |  |  |
| `activities_vector` | `0x02294798` | 36259736 | std::vector<> | 24 | Vetor de atividades em andamento |  |  |
| `all_syndromes_vector` | `0x022aa3f0` | 36348912 | std::vector<> | 24 | Todas as síndromes definidas (doenças, etc.) |  |  |
| `ammo_vector` | `0x021965d0` | 35218896 | std::vector<> | 24 | Vetor de munições (flechas, virotes) |  |  |
| `armor_vector` | `0x02197008` | 35221512 | std::vector<> | 24 | Vetor de todas as armaduras existentes |  |  |
| `artifacts_vector` | `0x021970f8` | 35221752 | std::vector<> | 24 | Vetor de todos os artefatos existentes no mundo |  |  |
| `backpacks_vector` | `0x021965b8` | 35218872 | std::vector<> | 24 | Vetor de mochilas e containers |  |  |
| `base_materials` | `0x022a8f10` | 36343568 | unknown | variable | Materiais base do sistema |  |  |
| `colors_vector` | `0x022a7ed8` | 36339416 | std::vector<> | 24 | Definições de cores disponíveis |  |  |
| `creature_vector` | `0x021960a0` | 35217568 | std::vector<> | 24 | Vetor mestre contendo todas as criaturas existentes |  |  |
| `crutches_vector` | `0x021965a0` | 35218848 | std::vector<> | 24 | Vetor contendo coleção de crutches |  |  |
| `cur_year_tick` | `0x0240423c` | 37765692 | unknown | variable | Tick atual dentro do ano (granularidade temporal) |  |  |
| `current_year` | `0x02404244` | 37765700 | unknown | variable | Ano atual no calendário interno do jogo |  |  |
| `dance_forms_vector` | `0x02298e38` | 36277816 | std::vector<> | 24 | Vetor contendo coleção de dance forms |  |  |
| `dwarf_civ_index` | `0x023fd280` | 37737088 | unknown | variable | Índice da civilização dos anões |  |  |
| `dwarf_race_index` | `0x023fd28c` | 37737100 | unknown | variable | Índice da raça dos anões na tabela de raças |  |  |
| `events_vector` | `0x022aaa90` | 36350608 | std::vector<> | 24 | Vetor contendo coleção de events |  |  |
| `external_flag` | `0x021824c4` | 35136708 | bool | 1 | Flag para comunicação com ferramentas externas |  |  |
| `fake_identities_vector` | `0x02298c10` | 36277264 | std::vector<> | 24 | Vetor contendo coleção de fake identities |  |  |
| `flasks_vector` | `0x02196888` | 35219592 | std::vector<> | 24 | Vetor de frascos e recipientes de líquidos |  |  |
| `fortress_entity` | `0x02403bd0` | 37764048 | unknown | variable | Ponteiro para a entidade que representa sua fortaleza |  |  |
| `global_equipment_update` | `0x024033f8` | 37762040 | unknown | variable | Campo de dados para global equipment update |  |  |
| `gloves_vector` | `0x02197050` | 35221584 | std::vector<> | 24 | Vetor contendo coleção de gloves |  |  |
| `gview` | `0x029fbac0` | 44022464 | unknown | variable | Visualização gráfica principal do jogo |  |  |
| `helms_vector` | `0x02197038` | 35221560 | std::vector<> | 24 | Vetor contendo coleção de helms |  |  |
| `historical_entities_vector` | `0x021827e8` | 35137512 | std::vector<> | 24 | Vetor de entidades históricas (civilizações) |  |  |
| `historical_figures_vector` | `0x022aaaf0` | 36350704 | std::vector<> | 24 | Vetor de figuras históricas importantes |  |  |
| `inorganics_vector` | `0x0229d7a8` | 36296616 | std::vector<> | 24 | Materiais inorgânicos (minerais, pedras) |  |  |
| `itemdef_ammo_vector` | `0x0229dcc8` | 36297928 | std::vector<> | 24 | Vetor contendo coleção de itemdef ammo |  |  |
| `itemdef_armor_vector` | `0x0229dcb0` | 36297904 | std::vector<> | 24 | Vetor contendo coleção de itemdef armor |  |  |
| `itemdef_food_vector` | `0x0229dd70` | 36298096 | std::vector<> | 24 | Vetor contendo coleção de itemdef food |  |  |
| `itemdef_glove_vector` | `0x0229dcf8` | 36297976 | std::vector<> | 24 | Vetor contendo coleção de itemdef glove |  |  |
| `itemdef_helm_vector` | `0x0229dd40` | 36298048 | std::vector<> | 24 | Vetor contendo coleção de itemdef helm |  |  |
| `itemdef_instrument_vector` | `0x0229dc98` | 36297880 | std::vector<> | 24 | Vetor contendo coleção de itemdef instrument |  |  |
| `itemdef_pant_vector` | `0x0229dd58` | 36298072 | std::vector<> | 24 | Vetor contendo coleção de itemdef pant |  |  |
| `itemdef_shield_vector` | `0x0229dd28` | 36298024 | std::vector<> | 24 | Vetor contendo coleção de itemdef shield |  |  |
| `itemdef_shoe_vector` | `0x0229dd10` | 36298000 | std::vector<> | 24 | Vetor contendo coleção de itemdef shoe |  |  |
| `itemdef_siegeammo_vector` | `0x0229dce0` | 36297952 | std::vector<> | 24 | Vetor contendo coleção de itemdef siegeammo |  |  |
| `itemdef_tool_vector` | `0x0229da10` | 36297232 | std::vector<> | 24 | Vetor contendo coleção de itemdef tool |  |  |
| `itemdef_toy_vector` | `0x0229d9f8` | 36297208 | std::vector<> | 24 | Vetor contendo coleção de itemdef toy |  |  |
| `itemdef_trap_vector` | `0x0229d9e0` | 36297184 | std::vector<> | 24 | Vetor contendo coleção de itemdef trap |  |  |
| `itemdef_weapons_vector` | `0x0229d9c8` | 36297160 | std::vector<> | 24 | Vetor contendo coleção de itemdef weapons |  |  |
| `language_vector` | `0x0229e590` | 36300176 | std::vector<> | 24 | Definições de idiomas |  |  |
| `material_templates_vector` | `0x0229d790` | 36296592 | std::vector<> | 24 | Templates de materiais (metais, pedras, etc.) |  |  |
| `musical_forms_vector` | `0x02298e08` | 36277768 | std::vector<> | 24 | Vetor contendo coleção de musical forms |  |  |
| `occupations_vector` | `0x02298ec8` | 36277960 | std::vector<> | 24 | Vetor contendo coleção de occupations |  |  |
| `pants_vector` | `0x02196fa8` | 35221416 | std::vector<> | 24 | Vetor contendo coleção de pants |  |  |
| `plants_vector` | `0x0229d7d8` | 36296664 | std::vector<> | 24 | Definições de plantas e árvores |  |  |
| `poetic_forms_vector` | `0x02298dd8` | 36277720 | std::vector<> | 24 | Vetor contendo coleção de poetic forms |  |  |
| `quivers_vector` | `0x02196558` | 35218776 | std::vector<> | 24 | Vetor contendo coleção de quivers |  |  |
| `races_vector` | `0x0229d948` | 36297032 | std::vector<> | 24 | Definições de todas as raças de criaturas |  |  |
| `reactions_vector` | `0x022a8070` | 36339824 | std::vector<> | 24 | Reações químicas e de workshop |  |  |
| `shapes_vector` | `0x022a7ef0` | 36339440 | std::vector<> | 24 | Definições de formas geométricas |  |  |
| `shields_vector` | `0x02196510` | 35218704 | std::vector<> | 24 | Vetor de escudos |  |  |
| `shoes_vector` | `0x02197020` | 35221536 | std::vector<> | 24 | Vetor contendo coleção de shoes |  |  |
| `squad_vector` | `0x02294738` | 36259640 | std::vector<> | 24 | Vetor de todos os esquadrões militares |  |  |
| `translation_vector` | `0x0229e5c0` | 36300224 | std::vector<> | 24 | Tabelas de tradução entre idiomas |  |  |
| `viewscreen_setupdwarfgame_vtable` | `0x01f21580` | 32642432 | unknown | variable | VTable da tela de setup inicial |  |  |
| `weapons_vector` | `0x02196480` | 35218560 | std::vector<> | 24 | Vetor de todas as armas existentes |  |  |
| `world_data` | `0x0229ca68` | 36293224 | unknown | variable | Ponteiro principal para todos os dados do mundo gerado |  |  |
| `world_site_type` | `0x0080` | 128 | unknown | variable | Campo de dados para world site type |  |  |

### Detalhes dos Offsets


## 🔧 armor_subtype_offsets

**Total de offsets:** 8

| Offset | Hex | Dec | Tipo | Tamanho | Significado | Valores Possíveis | Exemplos |
|--------|-----|-----|------|---------|-------------|-------------------|----------|
| `armor_adjective` | `0x00e8` | 232 | unknown | variable | Campo de dados para armor adjective |  |  |
| `armor_level` | `0x010c` | 268 | unknown | variable | Campo de dados para armor level |  |  |
| `chest_armor_properties` | `0x0118` | 280 | unknown | variable | Campo de dados para chest armor properties |  |  |
| `layer` | `0x0010` | 16 | uint16 | 2 | Camada corporal afetada (pele, músculo, osso) |  |  |
| `mat_name` | `0x00c8` | 200 | unknown | variable | Campo de dados para mat name |  |  |
| `other_armor_level` | `0x00cc` | 204 | unknown | variable | Campo de dados para other armor level |  |  |
| `other_armor_properties` | `0x00e8` | 232 | unknown | variable | Campo de dados para other armor properties |  |  |
| `pants_armor_properties` | `0x0128` | 296 | unknown | variable | Campo de dados para pants armor properties |  |  |

### Detalhes dos Offsets


## 🔧 art_offsets

**Total de offsets:** 1

| Offset | Hex | Dec | Tipo | Tamanho | Significado | Valores Possíveis | Exemplos |
|--------|-----|-----|------|---------|-------------|-------------------|----------|
| `name` | `0x0008` | 8 | unknown | variable | Estrutura complexa contendo primeiro nome, apelido e sobrenome |  |  |

### Detalhes dos Offsets


## 🔧 caste_offsets

**Total de offsets:** 14

| Offset | Hex | Dec | Tipo | Tamanho | Significado | Valores Possíveis | Exemplos |
|--------|-----|-----|------|---------|-------------|-------------------|----------|
| `adult_size` | `0x04d8` | 1240 | uint32 | 4 | Tamanho em bytes de adult |  |  |
| `baby_age` | `0x04c0` | 1216 | unknown | variable | Campo de dados para baby age |  |  |
| `body_info` | `0x06c0` | 1728 | unknown | variable | Campo de dados para body info |  |  |
| `caste_att_caps` | `0x1554` | 5460 | unknown | variable | Campo de dados para caste att caps |  |  |
| `caste_att_rates` | `0x1424` | 5156 | unknown | variable | Campo de dados para caste att rates |  |  |
| `caste_descr` | `0x0220` | 544 | unknown | variable | Campo de dados para caste descr |  |  |
| `caste_name` | `0x0020` | 32 | unknown | variable | Campo de dados para caste name |  |  |
| `caste_phys_att_ranges` | `0x1210` | 4624 | unknown | variable | Campo de dados para caste phys att ranges |  |  |
| `caste_trait_ranges` | `0x057c` | 1404 | unknown | variable | Campo de dados para caste trait ranges |  |  |
| `child_age` | `0x04c4` | 1220 | unknown | variable | Campo de dados para child age |  |  |
| `extracts` | `0x39e0` | 14816 | unknown | variable | Campo de dados para extracts |  |  |
| `flags` | `0x06a8` | 1704 | bool | 1 | Flag booleana indicando flags |  |  |
| `shearable_tissues_vector` | `0x16e0` | 5856 | std::vector<> | 24 | Vetor contendo coleção de shearable tissues |  |  |
| `skill_rates` | `0x08c0` | 2240 | unknown | variable | Campo de dados para skill rates |  |  |

### Detalhes dos Offsets


## 🔧 descriptor_offsets

**Total de offsets:** 2

| Offset | Hex | Dec | Tipo | Tamanho | Significado | Valores Possíveis | Exemplos |
|--------|-----|-----|------|---------|-------------|-------------------|----------|
| `color_name` | `0x0050` | 80 | unknown | variable | Campo de dados para color name |  |  |
| `shape_name_plural` | `0x0070` | 112 | unknown | variable | Campo de dados para shape name plural |  |  |

### Detalhes dos Offsets


## 🔧 dwarf_offsets

**Descrição:** Offsets para dados de unidades/criaturas - anões, animais, invasores, visitantes

**Total de offsets:** 52

| Offset | Hex | Dec | Tipo | Tamanho | Significado | Valores Possíveis | Exemplos |
|--------|-----|-----|------|---------|-------------|-------------------|----------|
| `active_syndrome_vector` | `0x0c80` | 3200 | std::vector<> | 24 | Vetor de síndromes ativas (doenças, maldições) |  |  |
| `affection_level` | `0x000c` | 12 | unknown | variable | Nível de afeição em relacionamentos |  |  |
| `animal_type` | `0x0138` | 312 | unknown | variable | Campo de dados para animal type |  |  |
| `artifact_name` | `0x09e8` | 2536 | unknown | variable | Nome de artefato associado (se criador ou portador) |  |  |
| `birth_time` | `0x0378` | 888 | uint32 | 4 | Tick específico no ano de nascimento (granularidade temporal) |  |  |
| `birth_year` | `0x0374` | 884 | uint32 | 4 | Ano de nascimento no calendário do jogo |  |  |
| `blood` | `0x06a4` | 1700 | uint32 | 4 | Nível atual de sangue no corpo (afeta sobrevivência) |  |  |
| `body_component_info` | `0x04d0` | 1232 | unknown | variable | Informações sobre componentes corporais |  |  |
| `body_size` | `0x06c8` | 1736 | uint32 | 4 | Tamanho físico atual do corpo (afeta capacidade de carga) |  |  |
| `caste` | `0x012c` | 300 | uint32 | 4 | ID da casta/subtipo da raça (referência para caste_offsets) |  |  |
| `civ` | `0x0140` | 320 | unknown | variable | ID da civilização de origem desta unidade |  |  |
| `counters1` | `0x07e0` | 2016 | uint32 | 4 | Grupo 1 de contadores diversos (ações, eventos) |  |  |
| `counters2` | `0x07fc` | 2044 | uint32 | 4 | Grupo 2 de contadores diversos |  |  |
| `counters3` | `0x0958` | 2392 | uint32 | 4 | Grupo 3 de contadores diversos |  |  |
| `current_job` | `0x04b8` | 1208 | unknown | variable | Ponteiro para estrutura do trabalho atual sendo executado |  |  |
| `curse` | `0x0820` | 2080 | unknown | variable | Informações sobre maldições ativas (vampirismo, licantropia) |  |  |
| `curse_add_flags1` | `0x080c` | 2060 | bool | 1 | Flags adicionais relacionadas a maldições |  |  |
| `custom_profession` | `0x0080` | 128 | unknown | variable | String customizada para profissão definida pelo jogador |  |  |
| `flags1` | `0x0110` | 272 | uint32 | 4 | Flags primárias de estado (ativo, vivo, cidadão, etc.) |  |  |
| `flags2` | `0x0114` | 276 | uint32 | 4 | Flags secundárias de estado (ferido, inconsciente, etc.) |  |  |
| `flags3` | `0x0118` | 280 | uint32 | 4 | Flags terciárias de estado (estados especiais adicionais) |  |  |
| `hist_id` | `0x0c10` | 3088 | uint32 | 4 | ID da figura histórica (para personagens importantes) |  |  |
| `id` | `0x0130` | 304 | uint32 | 4 | ID único da unidade (32-bit integer, usado como chave primária) |  |  |
| `inventory` | `0x03f0` | 1008 | unknown | variable | Vetor de itens carregados pela unidade |  |  |
| `inventory_item_bodypart` | `0x000a` | 10 | unknown | variable | Parte do corpo onde item está equipado |  |  |
| `inventory_item_mode` | `0x0008` | 8 | unknown | variable | Modo de carregamento de item no inventário |  |  |
| `labors` | `0x0a98` | 2712 | bitfield (labor flags) | variable | Bitfield de trabalhos habilitados para esta unidade | Bit 1: Mining; Bit 2: Carpentry; Bit 3: Crossbow Making; +80 mais | Bit 0: Mining; Bit 1: Woodcutting |
| `layer_status_vector` | `0x0048` | 72 | std::vector<> | 24 | Estado das camadas corporais (pele, músculos, etc.) |  |  |
| `limb_counters` | `0x0c18` | 3096 | uint32 | 4 | Contadores específicos de membros corporais |  |  |
| `meeting` | `0x0120` | 288 | unknown | variable | Informações sobre reuniões ou encontros agendados |  |  |
| `mood` | `0x0348` | 840 | int32 | 4 | Estado de humor/temperamento atual (normal, fey, possessed, etc.) |  |  |
| `mood_skill` | `0x04c0` | 1216 | uint32 (skill_id) | variable | Habilidade relacionada ao humor atual (para moods especiais) | 1: Mining; 2: Wood Cutting; 3: Carpentry; +134 mais | 0: Mining; 1: Woodcutting |
| `name` | `0x0008` | 8 | unknown | variable | Estrutura complexa contendo primeiro nome, apelido e sobrenome |  |  |
| `pet_owner_id` | `0x03a4` | 932 | uint32 | 4 | ID do dono se esta for uma criatura domesticada |  |  |
| `physical_attrs` | `0x05e4` | 1508 | vector<attribute_struct> | variable | Vetor de atributos físicos (força, agilidade, resistência, etc.) | 1: Strength; 2: Agility; 3: Toughness; +16 mais | Strength, Agility, Toughness, Endurance; Analytical Ability, Focus, Willpower |
| `profession` | `0x00a0` | 160 | uint32 (profession_id) | variable | ID da profissão atual (referência para professions em game_data) | 1: Miner; 2: Woodworker; 3: Carpenter; +132 mais | 0: Miner; 1: Woodworker |
| `race` | `0x00a4` | 164 | uint32 | 4 | ID da raça da criatura (referência para race_offsets) |  |  |
| `recheck_equipment` | `0x0268` | 616 | unknown | variable | Flag para revalidar equipamentos militares |  |  |
| `sex` | `0x012e` | 302 | int16 | 2 | Gênero da criatura (0=fêmea, 1=macho, -1=desconhecido) |  |  |
| `size_base` | `0x0690` | 1680 | uint32 | 4 | Tamanho base natural da criatura |  |  |
| `size_info` | `0x068c` | 1676 | uint32 | 4 | Informações detalhadas sobre tamanho e crescimento |  |  |
| `souls` | `0x0a60` | 2656 | unknown | variable | Vetor de almas (normalmente 1, múltiplas em casos especiais) |  |  |
| `specific_refs` | `0x01a8` | 424 | unknown | variable | Vetor de referências específicas a outros objetos |  |  |
| `squad_id` | `0x01d8` | 472 | uint32 | 4 | ID do esquadrão militar ao qual pertence |  |  |
| `squad_position` | `0x01dc` | 476 | uint32 | 4 | Posição/rank dentro do esquadrão |  |  |
| `states` | `0x0988` | 2440 | unknown | variable | Vetor de estados especiais (migrante, adaptado à caverna, etc.) |  |  |
| `syn_sick_flag` | `0x004c` | 76 | bool | 1 | Flag indicando se está doente por síndrome |  |  |
| `temp_mood` | `0x07f8` | 2040 | unknown | variable | Humor temporário sobrepondo o humor base |  |  |
| `turn_count` | `0x0920` | 2336 | uint32 | 4 | Contador de turnos de existência da unidade |  |  |
| `unit_health_info` | `0x0d28` | 3368 | unknown | variable | Estrutura com informações detalhadas de saúde |  |  |
| `used_items_vector` | `0x0d30` | 3376 | std::vector<> | 24 | Vetor de itens sendo ativamente utilizados |  |  |
| `wounds_vector` | `0x0590` | 1424 | std::vector<> | 24 | Vetor de ferimentos ativos na criatura |  |  |

### Detalhes dos Offsets

#### `profession` (Offset 0x00a0)

**Significado:** ID da profissão atual (referência para professions em game_data)

**Tipo de dados:** uint32 (profession_id) (variable bytes)

**Valores possíveis:**
- 1: Miner
- 2: Woodworker
- 3: Carpenter
- 4: Bowyer
- 5: Woodcutter
- 6: Stoneworker
- 7: Stonecutter
- 8: Stone Carver
- 9: Engraver
- 10: Mason
- 11: Ranger
- 12: Animal Caretaker
- 13: Animal Trainer
- 14: Hunter
- 15: Trapper
- 16: Animal Dissector
- 17: Metalsmith
- 18: Furnace Operator
- 19: Weaponsmith
- 20: Armorer
- ... e mais 115 valores

**Exemplos de uso:**
- 0: Miner
- 1: Woodworker
- 2: Carpenter
- 10: Ranger
- 22: Gem Cutter

---

#### `physical_attrs` (Offset 0x05e4)

**Significado:** Vetor de atributos físicos (força, agilidade, resistência, etc.)

**Tipo de dados:** vector<attribute_struct> (variable bytes)

**Valores possíveis:**
- 1: Strength
- 2: Agility
- 3: Toughness
- 4: Endurance
- 5: Disease Resistance
- 6: Recuperation
- 7: Analytical Ability
- 8: Creativity
- 9: Empathy
- 10: Focus
- 11: Intuition
- 12: Kinesthetic Sense
- 13: Linguistic Ability
- 14: Memory
- 15: Musicality
- 16: Patience
- 17: Social Awareness
- 18: Spatial Sense
- 19: Willpower

**Exemplos de uso:**
- Strength, Agility, Toughness, Endurance
- Analytical Ability, Focus, Willpower

---

#### `labors` (Offset 0x0a98)

**Significado:** Bitfield de trabalhos habilitados para esta unidade

**Tipo de dados:** bitfield (labor flags) (variable bytes)

**Valores possíveis:**
- Bit 1: Mining
- Bit 2: Carpentry
- Bit 3: Crossbow Making
- Bit 4: Wood Cutting
- Bit 5: Masonry
- Bit 6: Stonecutting
- Bit 7: Stone Carving
- Bit 8: Engraving
- Bit 9: Animal Training
- Bit 10: Animal Care
- Bit 11: Hunting
- Bit 12: Trapping
- Bit 13: Small Animal Dissection
- Bit 14: Diagnosis
- Bit 15: Surgery
- Bit 16: Setting Bones
- Bit 17: Suturing
- Bit 18: Dressing Wounds
- Bit 19: Feed Patients/Prisoners
- Bit 20: Recovering Wounded
- ... e mais 63 valores

**Exemplos de uso:**
- Bit 0: Mining
- Bit 1: Woodcutting
- Bit 2: Carpentry
- Bit 6: Masonry

---

#### `mood_skill` (Offset 0x04c0)

**Significado:** Habilidade relacionada ao humor atual (para moods especiais)

**Tipo de dados:** uint32 (skill_id) (variable bytes)

**Valores possíveis:**
- 1: Mining
- 2: Wood Cutting
- 3: Carpentry
- 4: Engraving
- 5: Masonry
- 6: Animal Training
- 7: Animal Caretaking
- 8: Fish Dissection
- 9: Animal Dissection
- 10: Fish Cleaning
- 11: Butchery
- 12: Trapping
- 13: Tanning
- 14: Weaving
- 15: Brewing
- 16: Clothesmaking
- 17: Milling
- 18: Threshing
- 19: Cheesemaking
- 20: Milking
- ... e mais 117 valores

**Exemplos de uso:**
- 0: Mining
- 1: Woodcutting
- 38: Weaponsmith
- 39: Armorer

---


## 🔧 emotion_offsets

**Descrição:** Offsets para sistema emocional - pensamentos, sentimentos, humores

**Total de offsets:** 7

| Offset | Hex | Dec | Tipo | Tamanho | Significado | Valores Possíveis | Exemplos |
|--------|-----|-----|------|---------|-------------|-------------------|----------|
| `emotion_type` | `0x0000` | 0 | uint32 | 4 | Tipo específico da emoção (felicidade, raiva, etc.) |  |  |
| `level` | `0x0014` | 20 | uint32 | 4 | Nível de intensidade em emoções graduais |  |  |
| `strength` | `0x0008` | 8 | uint32 | 4 | Intensidade da emoção (escala numérica) |  |  |
| `sub_id` | `0x0010` | 16 | uint32 | 4 | ID de subcategoria para emoções complexas |  |  |
| `thought_id` | `0x000c` | 12 | uint32 (thought_id) | 4 | ID do pensamento específico (referência para unit_thoughts) | 1: Conflict; 2: Trauma; 3: Death (Witnessed); +47 mais | 1: Conflict; 10: Crafted Masterwork |
| `year` | `0x0020` | 32 | uint32 | 4 | Ano em que a emoção foi gerada |  |  |
| `year_tick` | `0x0024` | 36 | uint32 | 4 | Tick específico quando a emoção foi gerada |  |  |

### Detalhes dos Offsets

#### `thought_id` (Offset 0x000c)

**Significado:** ID do pensamento específico (referência para unit_thoughts)

**Tipo de dados:** uint32 (thought_id) (4 bytes)

**Valores possíveis:**
- 1: Conflict
- 2: Trauma
- 3: Death (Witnessed)
- 4: Death (Unexpected)
- 5: Death
- 6: Killed
- 7: Love Separated
- 8: Love Reunited
- 9: Conflict Joined
- 10: Crafted Masterwork
- 11: Crafted Artifact
- 12: Mastered Skill
- 13: New Romance
- 14: Birth
- 15: Conflict Proximity
- 16: Cancelled Agreement
- 17: Traveling
- 18: Site Controlled
- 19: Cancelled Tribute
- 20: Incident
- ... e mais 30 valores

**Exemplos de uso:**
- 1: Conflict
- 10: Crafted Masterwork
- 32: Death (Pet)
- 98: Meal

---


## 🔧 general_ref_offsets

**Total de offsets:** 3

| Offset | Hex | Dec | Tipo | Tamanho | Significado | Valores Possíveis | Exemplos |
|--------|-----|-----|------|---------|-------------|-------------------|----------|
| `artifact_id` | `0x0008` | 8 | uint32 | 4 | Identificador único para artifact |  |  |
| `item_id` | `0x0008` | 8 | uint32 | 4 | Identificador único para item |  |  |
| `ref_type` | `0x0010` | 16 | unknown | variable | Campo de dados para ref type |  |  |

### Detalhes dos Offsets


## 🔧 health_offsets

**Descrição:** Offsets para sistema de saúde - ferimentos, doenças, estado físico

**Total de offsets:** 10

| Offset | Hex | Dec | Tipo | Tamanho | Significado | Valores Possíveis | Exemplos |
|--------|-----|-----|------|---------|-------------|-------------------|----------|
| `body_part_flags` | `0x0048` | 72 | bool | 1 | Flags de estado das partes corporais |  |  |
| `layer_global_id` | `0x0068` | 104 | uint32 | 4 | ID global da camada no sistema |  |  |
| `layer_tissue` | `0x0020` | 32 | unknown | variable | Tipo de tecido da camada |  |  |
| `layers_vector` | `0x0058` | 88 | std::vector<> | 24 | Camadas corporais (pele, gordura, músculo, osso) |  |  |
| `names_plural_vector` | `0x00a8` | 168 | std::vector<> | 24 | Vetor contendo coleção de names plural |  |  |
| `names_vector` | `0x0090` | 144 | std::vector<> | 24 | Nomes das partes corporais |  |  |
| `number` | `0x0084` | 132 | unknown | variable | Campo de dados para number |  |  |
| `parent_id` | `0x0040` | 64 | uint32 | 4 | ID da parte corporal pai (hierarquia) |  |  |
| `tissue_flags` | `0x0020` | 32 | bool | 1 | Flags de estado dos tecidos corporais |  |  |
| `tissue_name` | `0x0030` | 48 | unknown | variable | Nome específico do tecido |  |  |

### Detalhes dos Offsets


## 🔧 hist_entity_offsets

**Total de offsets:** 11

| Offset | Hex | Dec | Tipo | Tamanho | Significado | Valores Possíveis | Exemplos |
|--------|-----|-----|------|---------|-------------|-------------------|----------|
| `assign_hist_id` | `0x0004` | 4 | uint32 | 4 | Identificador único para assign hist |  |  |
| `assign_position_id` | `0x000c` | 12 | uint32 | 4 | Identificador único para assign position |  |  |
| `assignments` | `0x1110` | 4368 | unknown | variable | Campo de dados para assignments |  |  |
| `beliefs` | `0x0d18` | 3352 | unknown | variable | Campo de dados para beliefs |  |  |
| `histfigs` | `0x00e8` | 232 | unknown | variable | Campo de dados para histfigs |  |  |
| `position_female_name` | `0x00d8` | 216 | unknown | variable | Campo de dados para position female name |  |  |
| `position_id` | `0x0020` | 32 | uint32 | 4 | Identificador único para position |  |  |
| `position_male_name` | `0x0118` | 280 | unknown | variable | Campo de dados para position male name |  |  |
| `position_name` | `0x0098` | 152 | unknown | variable | Campo de dados para position name |  |  |
| `positions` | `0x10c0` | 4288 | unknown | variable | Posições disponíveis no esquadrão |  |  |
| `squads` | `0x11c8` | 4552 | unknown | variable | Campo de dados para squads |  |  |

### Detalhes dos Offsets


## 🔧 hist_event_offsets

**Total de offsets:** 3

| Offset | Hex | Dec | Tipo | Tamanho | Significado | Valores Possíveis | Exemplos |
|--------|-----|-----|------|---------|-------------|-------------------|----------|
| `event_year` | `0x0008` | 8 | unknown | variable | Campo de dados para event year |  |  |
| `id` | `0x0020` | 32 | uint32 | 4 | ID único da unidade (32-bit integer, usado como chave primária) |  |  |
| `killed_hist_id` | `0x0024` | 36 | uint32 | 4 | Identificador único para killed hist |  |  |

### Detalhes dos Offsets


## 🔧 hist_figure_offsets

**Total de offsets:** 13

| Offset | Hex | Dec | Tipo | Tamanho | Significado | Valores Possíveis | Exemplos |
|--------|-----|-----|------|---------|-------------|-------------------|----------|
| `current_ident` | `0x0030` | 48 | unknown | variable | Identificador único para currentent |  |  |
| `fake_birth_time` | `0x0098` | 152 | unknown | variable | Campo de dados para fake birth time |  |  |
| `fake_birth_year` | `0x0094` | 148 | unknown | variable | Campo de dados para fake birth year |  |  |
| `fake_name` | `0x0008` | 8 | unknown | variable | Campo de dados para fake name |  |  |
| `hist_fig_info` | `0x0130` | 304 | unknown | variable | Campo de dados para hist fig info |  |  |
| `hist_name` | `0x0038` | 56 | unknown | variable | Campo de dados para hist name |  |  |
| `hist_race` | `0x0002` | 2 | unknown | variable | Campo de dados para hist race |  |  |
| `id` | `0x00e0` | 224 | uint32 | 4 | ID único da unidade (32-bit integer, usado como chave primária) |  |  |
| `killed_counts_vector` | `0x00a8` | 168 | std::vector<> | 24 | Vetor contendo coleção de killed counts |  |  |
| `killed_race_vector` | `0x0018` | 24 | std::vector<> | 24 | Vetor contendo coleção de killed race |  |  |
| `killed_undead_vector` | `0x0090` | 144 | std::vector<> | 24 | Vetor contendo coleção de killed undead |  |  |
| `kills` | `0x0030` | 48 | unknown | variable | Campo de dados para kills |  |  |
| `reputation` | `0x0058` | 88 | unknown | variable | Campo de dados para reputation |  |  |

### Detalhes dos Offsets


## 🔧 item_filter_offsets

**Total de offsets:** 4

| Offset | Hex | Dec | Tipo | Tamanho | Significado | Valores Possíveis | Exemplos |
|--------|-----|-----|------|---------|-------------|-------------------|----------|
| `item_subtype` | `0x0002` | 2 | unknown | variable | Campo de dados para item subtype |  |  |
| `mat_class` | `0x0004` | 4 | unknown | variable | Campo de dados para mat class |  |  |
| `mat_index` | `0x0008` | 8 | unknown | variable | Campo de dados para mat index |  |  |
| `mat_type` | `0x0006` | 6 | unknown | variable | Campo de dados para mat type |  |  |

### Detalhes dos Offsets


## 🔧 item_offsets

**Descrição:** Offsets para itens genéricos - armas, ferramentas, materiais

**Total de offsets:** 11

| Offset | Hex | Dec | Tipo | Tamanho | Significado | Valores Possíveis | Exemplos |
|--------|-----|-----|------|---------|-------------|-------------------|----------|
| `artifact_id` | `0x0000` | 0 | uint32 | 4 | Identificador único para artifact |  |  |
| `artifact_name` | `0x0008` | 8 | unknown | variable | Nome de artefato associado (se criador ou portador) |  |  |
| `general_refs` | `0x0038` | 56 | unknown | variable | Campo de dados para general refs |  |  |
| `id` | `0x001c` | 28 | uint32 | 4 | ID único da unidade (32-bit integer, usado como chave primária) |  |  |
| `item_def` | `0x00e0` | 224 | unknown | variable | Campo de dados para item def |  |  |
| `maker_race` | `0x00b4` | 180 | unknown | variable | Campo de dados para maker race |  |  |
| `mat_index` | `0x00b0` | 176 | unknown | variable | Campo de dados para mat index |  |  |
| `mat_type` | `0x00ac` | 172 | unknown | variable | Campo de dados para mat type |  |  |
| `quality` | `0x00b6` | 182 | unknown | variable | Qualidade do item (obra-prima, superior, etc.) |  |  |
| `stack_size` | `0x0078` | 120 | uint32 | 4 | Quantidade de itens na pilha |  |  |
| `wear` | `0x009c` | 156 | unknown | variable | Nível de desgaste ou deterioração |  |  |

### Detalhes dos Offsets


## 🔧 item_subtype_offsets

**Total de offsets:** 7

| Offset | Hex | Dec | Tipo | Tamanho | Significado | Valores Possíveis | Exemplos |
|--------|-----|-----|------|---------|-------------|-------------------|----------|
| `adjective` | `0x00a8` | 168 | unknown | variable | Campo de dados para adjective |  |  |
| `base_flags` | `0x0030` | 48 | bool | 1 | Flag booleana indicando bases |  |  |
| `name` | `0x0068` | 104 | unknown | variable | Estrutura complexa contendo primeiro nome, apelido e sobrenome |  |  |
| `name_plural` | `0x0088` | 136 | unknown | variable | Campo de dados para name plural |  |  |
| `sub_type` | `0x0028` | 40 | unknown | variable | Campo de dados para sub type |  |  |
| `tool_adjective` | `0x00d8` | 216 | unknown | variable | Campo de dados para tool adjective |  |  |
| `tool_flags` | `0x00a8` | 168 | bool | 1 | Flag booleana indicando tools |  |  |

### Detalhes dos Offsets


## 🔧 job_details

**Total de offsets:** 7

| Offset | Hex | Dec | Tipo | Tamanho | Significado | Valores Possíveis | Exemplos |
|--------|-----|-----|------|---------|-------------|-------------------|----------|
| `id` | `0x0014` | 20 | uint32 | 4 | ID único da unidade (32-bit integer, usado como chave primária) |  |  |
| `mat_category` | `0x0048` | 72 | unknown | variable | Campo de dados para mat category |  |  |
| `mat_index` | `0x0034` | 52 | unknown | variable | Campo de dados para mat index |  |  |
| `mat_type` | `0x0030` | 48 | unknown | variable | Campo de dados para mat type |  |  |
| `reaction` | `0x0020` | 32 | unknown | variable | Campo de dados para reaction |  |  |
| `reaction_skill` | `0x0080` | 128 | unknown | variable | Campo de dados para reaction skill |  |  |
| `sub_job_id` | `0x0050` | 80 | uint32 | 4 | Identificador único para sub job |  |  |

### Detalhes dos Offsets


## 🔧 material_offsets

**Total de offsets:** 11

| Offset | Hex | Dec | Tipo | Tamanho | Significado | Valores Possíveis | Exemplos |
|--------|-----|-----|------|---------|-------------|-------------------|----------|
| `flags` | `0x0290` | 656 | bool | 1 | Flag booleana indicando flags |  |  |
| `gas_name` | `0x00f8` | 248 | unknown | variable | Campo de dados para gas name |  |  |
| `inorganic_flags` | `0x0038` | 56 | bool | 1 | Flag booleana indicando inorganics |  |  |
| `inorganic_materials_vector` | `0x01a8` | 424 | std::vector<> | 24 | Vetor contendo coleção de inorganic materials |  |  |
| `liquid_name` | `0x00d8` | 216 | unknown | variable | Identificador único para liquid name |  |  |
| `paste_name` | `0x0138` | 312 | unknown | variable | Campo de dados para paste name |  |  |
| `powder_name` | `0x0118` | 280 | unknown | variable | Campo de dados para powder name |  |  |
| `prefix` | `0x0520` | 1312 | unknown | variable | Campo de dados para prefix |  |  |
| `pressed_name` | `0x0158` | 344 | unknown | variable | Campo de dados para pressed name |  |  |
| `reaction_class` | `0x04a8` | 1192 | unknown | variable | Campo de dados para reaction class |  |  |
| `solid_name` | `0x00b8` | 184 | unknown | variable | Identificador único para solid name |  |  |

### Detalhes dos Offsets


## 🔧 need_offsets

**Total de offsets:** 4

| Offset | Hex | Dec | Tipo | Tamanho | Significado | Valores Possíveis | Exemplos |
|--------|-----|-----|------|---------|-------------|-------------------|----------|
| `deity_id` | `0x0004` | 4 | uint32 | 4 | Identificador único para deity |  |  |
| `focus_level` | `0x0008` | 8 | unknown | variable | Campo de dados para focus level |  |  |
| `id` | `0x0000` | 0 | uint32 | 4 | ID único da unidade (32-bit integer, usado como chave primária) |  |  |
| `need_level` | `0x000c` | 12 | unknown | variable | Campo de dados para need level |  |  |

### Detalhes dos Offsets


## 🔧 offsets

**Total de offsets:** 1

| Offset | Hex | Dec | Tipo | Tamanho | Significado | Valores Possíveis | Exemplos |
|--------|-----|-----|------|---------|-------------|-------------------|----------|
| `word_table` | `0x0050` | 80 | unknown | variable | Campo de dados para word table |  |  |

### Detalhes dos Offsets


## 🔧 plant_offsets

**Total de offsets:** 6

| Offset | Hex | Dec | Tipo | Tamanho | Significado | Valores Possíveis | Exemplos |
|--------|-----|-----|------|---------|-------------|-------------------|----------|
| `flags` | `0x0040` | 64 | bool | 1 | Flag booleana indicando flags |  |  |
| `materials_vector` | `0x02a0` | 672 | std::vector<> | 24 | Vetor contendo coleção de materials |  |  |
| `name` | `0x0050` | 80 | unknown | variable | Estrutura complexa contendo primeiro nome, apelido e sobrenome |  |  |
| `name_leaf_plural` | `0x0110` | 272 | unknown | variable | Campo de dados para name leaf plural |  |  |
| `name_plural` | `0x0070` | 112 | unknown | variable | Campo de dados para name plural |  |  |
| `name_seed_plural` | `0x00d0` | 208 | unknown | variable | Campo de dados para name seed plural |  |  |

### Detalhes dos Offsets


## 🔧 race_offsets

**Descrição:** Offsets para definições de raças - anões, elfos, humanos, goblins

**Total de offsets:** 13

| Offset | Hex | Dec | Tipo | Tamanho | Significado | Valores Possíveis | Exemplos |
|--------|-----|-----|------|---------|-------------|-------------------|----------|
| `adjective` | `0x0060` | 96 | unknown | variable | Campo de dados para adjective |  |  |
| `baby_name_plural` | `0x00a0` | 160 | unknown | variable | Campo de dados para baby name plural |  |  |
| `baby_name_singular` | `0x0080` | 128 | unknown | variable | Campo de dados para baby name singular |  |  |
| `castes_vector` | `0x0178` | 376 | std::vector<> | 24 | Vetor contendo coleção de castes |  |  |
| `child_name_plural` | `0x00e0` | 224 | unknown | variable | Campo de dados para child name plural |  |  |
| `child_name_singular` | `0x00c0` | 192 | unknown | variable | Campo de dados para child name singular |  |  |
| `flags` | `0x01a8` | 424 | bool | 1 | Flag booleana indicando flags |  |  |
| `materials_vector` | `0x01f0` | 496 | std::vector<> | 24 | Vetor contendo coleção de materials |  |  |
| `name_plural` | `0x0040` | 64 | unknown | variable | Campo de dados para name plural |  |  |
| `name_singular` | `0x0020` | 32 | unknown | variable | Campo de dados para name singular |  |  |
| `pop_ratio_vector` | `0x0190` | 400 | std::vector<> | 24 | Vetor contendo coleção de pop ratio |  |  |
| `pref_string_vector` | `0x0148` | 328 | std::vector<> | 24 | Vetor contendo coleção de pref string |  |  |
| `tissues_vector` | `0x0208` | 520 | std::vector<> | 24 | Vetor contendo coleção de tissues |  |  |

### Detalhes dos Offsets


## 🔧 soul_details

**Total de offsets:** 17

| Offset | Hex | Dec | Tipo | Tamanho | Significado | Valores Possíveis | Exemplos |
|--------|-----|-----|------|---------|-------------|-------------------|----------|
| `beliefs` | `0x0000` | 0 | unknown | variable | Campo de dados para beliefs |  |  |
| `combat_hardened` | `0x0130` | 304 | unknown | variable | Campo de dados para combat hardened |  |  |
| `current_focus` | `0x0184` | 388 | unknown | variable | Campo de dados para current focus |  |  |
| `emotions` | `0x0030` | 48 | unknown | variable | Campo de dados para emotions |  |  |
| `goal_realized` | `0x0028` | 40 | unknown | variable | Campo de dados para goal realized |  |  |
| `goals` | `0x0048` | 72 | unknown | variable | Campo de dados para goals |  |  |
| `likes_outdoors` | `0x012c` | 300 | unknown | variable | Campo de dados para likes outdoors |  |  |
| `mental_attrs` | `0x00ac` | 172 | unknown | variable | Campo de dados para mental attrs |  |  |
| `name` | `0x0008` | 8 | unknown | variable | Estrutura complexa contendo primeiro nome, apelido e sobrenome |  |  |
| `needs` | `0x0138` | 312 | unknown | variable | Campo de dados para needs |  |  |
| `orientation` | `0x0088` | 136 | unknown | variable | Campo de dados para orientation |  |  |
| `personality` | `0x0248` | 584 | unknown | variable | Campo de dados para personality |  |  |
| `preferences` | `0x0230` | 560 | unknown | variable | Campo de dados para preferences |  |  |
| `skills` | `0x0218` | 536 | unknown | variable | Campo de dados para skills |  |  |
| `stress_level` | `0x0120` | 288 | unknown | variable | Campo de dados para stress level |  |  |
| `traits` | `0x0080` | 128 | unknown | variable | Campo de dados para traits |  |  |
| `undistracted_focus` | `0x0188` | 392 | unknown | variable | Campo de dados para undistracted focus |  |  |

### Detalhes dos Offsets


## 🔧 squad_offsets

**Descrição:** Offsets para esquadrões militares - organização, membros, ordens

**Total de offsets:** 33

| Offset | Hex | Dec | Tipo | Tamanho | Significado | Valores Possíveis | Exemplos |
|--------|-----|-----|------|---------|-------------|-------------------|----------|
| `alert` | `0x00e8` | 232 | unknown | variable | Estado de alerta atual do esquadrão |  |  |
| `alias` | `0x0080` | 128 | unknown | variable | Campo de dados para alias |  |  |
| `ammunition` | `0x0140` | 320 | unknown | variable | Campo de dados para ammunition |  |  |
| `ammunition_qty` | `0x000c` | 12 | unknown | variable | Campo de dados para ammunition qty |  |  |
| `armor_vector` | `0x0080` | 128 | std::vector<> | 24 | Vetor de todas as armaduras existentes |  |  |
| `backpack` | `0x016c` | 364 | unknown | variable | Campo de dados para backpack |  |  |
| `carry_food` | `0x01c0` | 448 | unknown | variable | Campo de dados para carry food |  |  |
| `carry_water` | `0x01c2` | 450 | unknown | variable | Campo de dados para carry water |  |  |
| `equipment_update` | `0x01b8` | 440 | unknown | variable | Campo de dados para equipment update |  |  |
| `flask` | `0x0170` | 368 | unknown | variable | Campo de dados para flask |  |  |
| `gloves_vector` | `0x00c8` | 200 | std::vector<> | 24 | Vetor contendo coleção de gloves |  |  |
| `helm_vector` | `0x0098` | 152 | std::vector<> | 24 | Vetor contendo coleção de helm |  |  |
| `id` | `0x0000` | 0 | uint32 | 4 | ID único da unidade (32-bit integer, usado como chave primária) |  |  |
| `members` | `0x00a0` | 160 | unknown | variable | Vetor de membros do esquadrão |  |  |
| `name` | `0x0008` | 8 | unknown | variable | Estrutura complexa contendo primeiro nome, apelido e sobrenome |  |  |
| `orders` | `0x00b8` | 184 | unknown | variable | Ordens militares ativas |  |  |
| `pants_vector` | `0x00b0` | 176 | std::vector<> | 24 | Vetor contendo coleção de pants |  |  |
| `quiver` | `0x0168` | 360 | unknown | variable | Campo de dados para quiver |  |  |
| `sched_assign` | `0x0040` | 64 | unknown | variable | Campo de dados para sched assign |  |  |
| `sched_orders` | `0x0028` | 40 | unknown | variable | Campo de dados para sched orders |  |  |
| `sched_size` | `0x0058` | 88 | uint32 | 4 | Tamanho em bytes de sched |  |  |
| `schedules` | `0x00d0` | 208 | unknown | variable | Campo de dados para schedules |  |  |
| `shield_vector` | `0x00f8` | 248 | std::vector<> | 24 | Vetor contendo coleção de shield |  |  |
| `shoes_vector` | `0x00e0` | 224 | std::vector<> | 24 | Vetor contendo coleção de shoes |  |  |
| `uniform_indiv_choice` | `0x0030` | 48 | unknown | variable | Campo de dados para uniform indiv choice |  |  |
| `uniform_item_filter` | `0x0004` | 4 | unknown | variable | Campo de dados para uniform item filter |  |  |
| `uniform_spec_item_subtype` | `0x0006` | 6 | unknown | variable | Campo de dados para uniform spec item subtype |  |  |
| `uniform_spec_item_type` | `0x0004` | 4 | unknown | variable | Campo de dados para uniform spec item type |  |  |
| `uniform_spec_mat_class` | `0x0008` | 8 | unknown | variable | Campo de dados para uniform spec mat class |  |  |
| `uniform_spec_mat_index` | `0x000c` | 12 | unknown | variable | Campo de dados para uniform spec mat index |  |  |
| `uniform_spec_mat_type` | `0x000a` | 10 | unknown | variable | Campo de dados para uniform spec mat type |  |  |
| `uniform_spec_uniform_item_filter` | `0x0004` | 4 | unknown | variable | Campo de dados para uniform spec uniform item filter |  |  |
| `weapon_vector` | `0x0110` | 272 | std::vector<> | 24 | Vetor contendo coleção de weapon |  |  |

### Detalhes dos Offsets


## 🔧 syndrome_offsets

**Total de offsets:** 7

| Offset | Hex | Dec | Tipo | Tamanho | Significado | Valores Possíveis | Exemplos |
|--------|-----|-----|------|---------|-------------|-------------------|----------|
| `cie_effects` | `0x0020` | 32 | unknown | variable | Campo de dados para cie effects |  |  |
| `cie_end` | `0x0018` | 24 | unknown | variable | Campo de dados para cie end |  |  |
| `cie_first_perc` | `0x0098` | 152 | unknown | variable | Campo de dados para cie first perc |  |  |
| `cie_ment` | `0x00cc` | 204 | unknown | variable | Campo de dados para cie ment |  |  |
| `cie_phys` | `0x00b0` | 176 | unknown | variable | Campo de dados para cie phys |  |  |
| `syn_classes_vector` | `0x00c8` | 200 | std::vector<> | 24 | Vetor contendo coleção de syn classes |  |  |
| `trans_race_vec` | `0x00e0` | 224 | unknown | variable | Campo de dados para trans race vec |  |  |

### Detalhes dos Offsets


## 🔧 unit_wound_offsets

**Total de offsets:** 11

| Offset | Hex | Dec | Tipo | Tamanho | Significado | Valores Possíveis | Exemplos |
|--------|-----|-----|------|---------|-------------|-------------------|----------|
| `bleeding` | `0x006c` | 108 | bool | 1 | Estado e intensidade do sangramento |  |  |
| `cur_pen` | `0x0098` | 152 | unknown | variable | Campo de dados para cur pen |  |  |
| `effects_vector` | `0x0048` | 72 | std::vector<> | 24 | Vetor contendo coleção de effects |  |  |
| `flags1` | `0x0064` | 100 | uint32 | 4 | Flags primárias de estado (ativo, vivo, cidadão, etc.) |  |  |
| `flags2` | `0x0068` | 104 | uint32 | 4 | Flags secundárias de estado (ferido, inconsciente, etc.) |  |  |
| `general_flags` | `0x002c` | 44 | bool | 1 | Flag booleana indicando generals |  |  |
| `id` | `0x0004` | 4 | uint32 | 4 | ID único da unidade (32-bit integer, usado como chave primária) |  |  |
| `layer` | `0x0006` | 6 | uint16 | 2 | Camada corporal afetada (pele, músculo, osso) |  |  |
| `max_pen` | `0x009a` | 154 | unknown | variable | Campo de dados para max pen |  |  |
| `pain` | `0x0070` | 112 | uint32 | 4 | Nível de dor causado pelo ferimento |  |  |
| `parts` | `0x0008` | 8 | unknown | variable | Partes do corpo afetadas pelo ferimento |  |  |

### Detalhes dos Offsets


## 🔧 viewscreen_offsets

**Total de offsets:** 3

| Offset | Hex | Dec | Tipo | Tamanho | Significado | Valores Possíveis | Exemplos |
|--------|-----|-----|------|---------|-------------|-------------------|----------|
| `child` | `0x0008` | 8 | unknown | variable | Campo de dados para child |  |  |
| `setupdwarfgame_units` | `0x1e98` | 7832 | unknown | variable | Campo de dados para setupdwarfgame units |  |  |
| `view` | `0x0008` | 8 | unknown | variable | Campo de dados para view |  |  |

### Detalhes dos Offsets


## 🔧 weapon_subtype_offsets

**Total de offsets:** 5

| Offset | Hex | Dec | Tipo | Tamanho | Significado | Valores Possíveis | Exemplos |
|--------|-----|-----|------|---------|-------------|-------------------|----------|
| `ammo` | `0x00d8` | 216 | unknown | variable | Campo de dados para ammo |  |  |
| `melee_skill` | `0x00d0` | 208 | unknown | variable | Campo de dados para melee skill |  |  |
| `multi_size` | `0x00fc` | 252 | uint32 | 4 | Tamanho em bytes de multi |  |  |
| `ranged_skill` | `0x00d2` | 210 | unknown | variable | Campo de dados para ranged skill |  |  |
| `single_size` | `0x00f8` | 248 | uint32 | 4 | Tamanho em bytes de single |  |  |

### Detalhes dos Offsets


## 🔧 word_offsets

**Total de offsets:** 14

| Offset | Hex | Dec | Tipo | Tamanho | Significado | Valores Possíveis | Exemplos |
|--------|-----|-----|------|---------|-------------|-------------------|----------|
| `adjective` | `0x0060` | 96 | unknown | variable | Campo de dados para adjective |  |  |
| `base` | `0x0000` | 0 | unknown | variable | Campo de dados para base |  |  |
| `first_name` | `0x0000` | 0 | unknown | variable | Campo de dados para first name |  |  |
| `language_id` | `0x006c` | 108 | uint32 | 4 | Identificador único para language |  |  |
| `nickname` | `0x0020` | 32 | unknown | variable | Campo de dados para nickname |  |  |
| `noun_plural` | `0x0040` | 64 | unknown | variable | Campo de dados para noun plural |  |  |
| `noun_singular` | `0x0020` | 32 | unknown | variable | Campo de dados para noun singular |  |  |
| `past_participle_verb` | `0x0100` | 256 | unknown | variable | Campo de dados para past participle verb |  |  |
| `past_simple_verb` | `0x00e0` | 224 | unknown | variable | Campo de dados para past simple verb |  |  |
| `present_participle_verb` | `0x0120` | 288 | unknown | variable | Campo de dados para present participle verb |  |  |
| `present_simple_verb` | `0x00c0` | 192 | unknown | variable | Campo de dados para present simple verb |  |  |
| `verb` | `0x00a0` | 160 | unknown | variable | Campo de dados para verb |  |  |
| `word_type` | `0x005c` | 92 | unknown | variable | Campo de dados para word type |  |  |
| `words` | `0x0040` | 64 | unknown | variable | Campo de dados para words |  |  |

### Detalhes dos Offsets


## 📚 Apêndices

### A. Enums Encontrados no Código

**GENDER_TYPE:**
- SEX_UNK
- SEX_F
- SEX_M

**SEX_ORIENT_TYPE:**
- ORIENT_ASEXUAL
- ORIENT_BISEXUAL
- ORIENT_HOMO
- ORIENT_HETERO

**SEX_COMMITMENT:**
- COMMIT_UNINTERESTED
- COMMIT_LOVER
- COMMIT_MARRIAGE

**MISC_STATES:**
- STATE_MIGRANT
- STATE_CAVE_ADAPT

**TRAINED_LEVEL:**
- none
- semi_wild
- trained
- well_trained
- skillfully_trained
- expertly_trained
- exceptionally_trained
- masterfully_trained
- domesticated
- unknown_trained
- ... e mais 2 valores

**UNIT_OCCUPATION:**
- OCC_NONE
- OCC_TAVERN
- OCC_PERFORMER
- OCC_SCHOLAR
- OCC_MERC
- OCC_MONSTER
- OCC_SCRIBE
- OCC_MESSENGER
- OCC_DOCTOR
- OCC_DIAGNOSTICIAN
- ... e mais 2 valores

**GenderInfoOption:**
- Option_SexOnly
- Option_ShowOrientation
- Option_ShowCommitment

**FOCUS_DEGREE:**
- FOCUS_BADLY_DISTRACTED
- FOCUS_DISTRACTED
- FOCUS_UNFOCUSED
- FOCUS_UNTROUBLED
- FOCUS_SOMEWHAT_FOCUSED
- FOCUS_QUITE_FOCUSED
- FOCUS_VERY_FOCUSED
- FOCUS_DEGREE_COUNT

**Aspects:**
- Attributes
- Facets
- Beliefs
- Goals
- Needs
- Skills
- Preferences
- AspectCount

**unnamed:**
- GCOL_ACTIVE
- GCOL_PENDING
- GCOL_DISABLED

### B. Uso no Código Fonte

**dwarf_offsets.temp_mood:** usado em dwarf.cpp
**dwarf_offsets.animal_type:** usado em dwarf.cpp
**dwarf_offsets.pet_owner_id:** usado em dwarf.cpp
**dwarf_offsets.states:** usado em dwarf.cpp
**dwarf_offsets.meeting:** usado em dwarf.cpp

### C. Guia de Tipos de Dados

| Tipo | Tamanho | Descrição |
|------|---------|----------|
| `uint32` | 4 bytes | Inteiro sem sinal 32-bit (0 a 4,294,967,295) |
| `int32` | 4 bytes | Inteiro com sinal 32-bit (-2,147,483,648 a 2,147,483,647) |
| `uint16` | 2 bytes | Inteiro sem sinal 16-bit (0 a 65,535) |
| `int16` | 2 bytes | Inteiro com sinal 16-bit (-32,768 a 32,767) |
| `bool` | 1 byte | Valor booleano (0=false, 1=true) |
| `void*` | 8 bytes | Ponteiro de memória (64-bit) |
| `std::vector<>` | 24+ bytes | Container dinâmico C++ |
| `bitfield` | variável | Campo de bits para flags múltiplas |
