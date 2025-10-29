# Dicionário de Offsets - Dwarf Therapist

**Gerado em:** 2025-10-28 23:49:52

**Total de seções:** 29
**Total de offsets:** 353

## 📋 Índice

- [activity_offsets](#activity-offsets) (13 offsets)
- [addresses](#addresses) (62 offsets)
- [armor_subtype_offsets](#armor-subtype-offsets) (8 offsets)
- [art_offsets](#art-offsets) (1 offsets)
- [caste_offsets](#caste-offsets) (14 offsets)
- [descriptor_offsets](#descriptor-offsets) (2 offsets)
- [dwarf_offsets](#dwarf-offsets) (52 offsets)
- [emotion_offsets](#emotion-offsets) (7 offsets)
- [general_ref_offsets](#general-ref-offsets) (3 offsets)
- [health_offsets](#health-offsets) (10 offsets)
- [hist_entity_offsets](#hist-entity-offsets) (11 offsets)
- [hist_event_offsets](#hist-event-offsets) (3 offsets)
- [hist_figure_offsets](#hist-figure-offsets) (13 offsets)
- [item_filter_offsets](#item-filter-offsets) (4 offsets)
- [item_offsets](#item-offsets) (11 offsets)
- [item_subtype_offsets](#item-subtype-offsets) (7 offsets)
- [job_details](#job-details) (7 offsets)
- [material_offsets](#material-offsets) (11 offsets)
- [need_offsets](#need-offsets) (4 offsets)
- [offsets](#offsets) (1 offsets)
- [plant_offsets](#plant-offsets) (6 offsets)
- [race_offsets](#race-offsets) (13 offsets)
- [soul_details](#soul-details) (17 offsets)
- [squad_offsets](#squad-offsets) (33 offsets)
- [syndrome_offsets](#syndrome-offsets) (7 offsets)
- [unit_wound_offsets](#unit-wound-offsets) (11 offsets)
- [viewscreen_offsets](#viewscreen-offsets) (3 offsets)
- [weapon_subtype_offsets](#weapon-subtype-offsets) (5 offsets)
- [word_offsets](#word-offsets) (14 offsets)

## 📖 Descrição das Categorias

**addresses:** Endereços globais do jogo (ponteiros para estruturas principais)

**dwarf_offsets:** Offsets para dados de unidades/criaturas (anões, animais, invasores)

**squad_offsets:** Offsets para dados de esquadrões militares

**word_offsets:** Offsets para estruturas de palavras e linguagem

**race_offsets:** Offsets para dados de raças (anão, elfo, humano, etc.)

**caste_offsets:** Offsets para dados de castas (subtipos de raça)

**hist_figure_offsets:** Offsets para figuras históricas

**hist_event_offsets:** Offsets para eventos históricos

**hist_entity_offsets:** Offsets para entidades históricas (civilizações)

**item_offsets:** Offsets para itens genéricos

**weapon_subtype_offsets:** Offsets para subtipos de armas

**armor_subtype_offsets:** Offsets para subtipos de armaduras

**material_offsets:** Offsets para dados de materiais

**plant_offsets:** Offsets para dados de plantas

**syndrome_offsets:** Offsets para síndromes (doenças, maldições)

**emotion_offsets:** Offsets para estados emocionais

**activity_offsets:** Offsets para atividades das unidades

**health_offsets:** Offsets para informações de saúde

**unit_wound_offsets:** Offsets para ferimentos de unidades

**general_ref_offsets:** Offsets para referências gerais

**art_offsets:** Offsets para objetos de arte

**job_details:** Offsets para trabalhos/tarefas

**soul_details:** Offsets para dados da alma

**need_offsets:** Offsets para necessidades das unidades

**viewscreen_offsets:** Offsets para telas do jogo

**offsets:** Offsets diversos de linguagem

## 🔧 Seções de Offsets

### activity_offsets

**Descrição:** Offsets para atividades das unidades

**Total de offsets:** 13

| Offset | Valor (Hex) | Valor (Dec) | Significado | Plataformas | Versões |
|--------|-------------|-------------|-------------|-------------|---------|
| `activity_type` | `0x0004` | 4 | Campo activity type | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `events` | `0x0008` | 8 | Campo events | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `knowledge_category` | `0x00c0` | 192 | Campo knowledge category | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `knowledge_flag` | `0x00c4` | 196 | Flag de knowledge | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `participants` | `0x0048` | 72 | Participantes da atividade | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `perf_histfig` | `0x000c` | 12 | Campo perf histfig | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `perf_participants` | `0x00e0` | 224 | Campo perf participants | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `perf_type` | `0x00b0` | 176 | Campo perf type | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `pray_deity` | `0x00b0` | 176 | Campo pray deity | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `pray_sphere` | `0x00b4` | 180 | Campo pray sphere | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `sq_lead` | `0x00b4` | 180 | Campo sq lead | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `sq_skill` | `0x00bc` | 188 | Campo sq skill | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `sq_train_rounds` | `0x00c8` | 200 | Campo sq train rounds | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |

---

### addresses

**Descrição:** Endereços globais do jogo (ponteiros para estruturas principais)

**Total de offsets:** 62

| Offset | Valor (Hex) | Valor (Dec) | Significado | Plataformas | Versões |
|--------|-------------|-------------|-------------|-------------|---------|
| `active_creature_vector` | `0x021960b8` | 35217592 | Vetor de criaturas ativas | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `active_sites_vector` | `0x000483d0` | 295888 | Vetor de sites ativos | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `activities_vector` | `0x02294798` | 36259736 | Vetor de atividades | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `all_syndromes_vector` | `0x022aa3f0` | 36348912 | Vetor de all syndromes | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `ammo_vector` | `0x021965d0` | 35218896 | Vetor de ammo | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `armor_vector` | `0x02197008` | 35221512 | Vetor de armor | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `artifacts_vector` | `0x021970f8` | 35221752 | Vetor de artefatos | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `backpacks_vector` | `0x021965b8` | 35218872 | Vetor de backpacks | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `base_materials` | `0x022a8f10` | 36343568 | Campo base materials | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `colors_vector` | `0x022a7ed8` | 36339416 | Vetor de colors | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `creature_vector` | `0x021960a0` | 35217568 | Vetor de todas as criaturas | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `crutches_vector` | `0x021965a0` | 35218848 | Vetor de crutches | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `cur_year_tick` | `0x0240423c` | 37765692 | Tick atual no ano | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `current_year` | `0x02404244` | 37765700 | Ano atual do jogo | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `dance_forms_vector` | `0x02298e38` | 36277816 | Vetor de dance forms | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `dwarf_civ_index` | `0x023fd280` | 37737088 | Campo dwarf civ index | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `dwarf_race_index` | `0x023fd28c` | 37737100 | Índice da raça dos anões | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `events_vector` | `0x022aaa90` | 36350608 | Vetor de events | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `external_flag` | `0x021824c4` | 35136708 | Flag de external | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `fake_identities_vector` | `0x02298c10` | 36277264 | Vetor de fake identities | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `flasks_vector` | `0x02196888` | 35219592 | Vetor de flasks | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `fortress_entity` | `0x02403bd0` | 37764048 | Entidade da fortaleza | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `global_equipment_update` | `0x024033f8` | 37762040 | Campo global equipment update | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `gloves_vector` | `0x02197050` | 35221584 | Vetor de gloves | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `gview` | `0x029fbac0` | 44022464 | Campo gview | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `helms_vector` | `0x02197038` | 35221560 | Vetor de helms | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `historical_entities_vector` | `0x021827e8` | 35137512 | Vetor de entidades históricas | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `historical_figures_vector` | `0x022aaaf0` | 36350704 | Vetor de figuras históricas | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `inorganics_vector` | `0x0229d7a8` | 36296616 | Vetor de inorganics | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `itemdef_ammo_vector` | `0x0229dcc8` | 36297928 | Vetor de itemdef ammo | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `itemdef_armor_vector` | `0x0229dcb0` | 36297904 | Vetor de itemdef armor | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `itemdef_food_vector` | `0x0229dd70` | 36298096 | Vetor de itemdef food | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `itemdef_glove_vector` | `0x0229dcf8` | 36297976 | Vetor de itemdef glove | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `itemdef_helm_vector` | `0x0229dd40` | 36298048 | Vetor de itemdef helm | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `itemdef_instrument_vector` | `0x0229dc98` | 36297880 | Vetor de itemdef instrument | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `itemdef_pant_vector` | `0x0229dd58` | 36298072 | Vetor de itemdef pant | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `itemdef_shield_vector` | `0x0229dd28` | 36298024 | Vetor de itemdef shield | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `itemdef_shoe_vector` | `0x0229dd10` | 36298000 | Vetor de itemdef shoe | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `itemdef_siegeammo_vector` | `0x0229dce0` | 36297952 | Vetor de itemdef siegeammo | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `itemdef_tool_vector` | `0x0229da10` | 36297232 | Vetor de itemdef tool | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `itemdef_toy_vector` | `0x0229d9f8` | 36297208 | Vetor de itemdef toy | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `itemdef_trap_vector` | `0x0229d9e0` | 36297184 | Vetor de itemdef trap | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `itemdef_weapons_vector` | `0x0229d9c8` | 36297160 | Vetor de itemdef weapons | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `language_vector` | `0x0229e590` | 36300176 | Vetor de language | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `material_templates_vector` | `0x0229d790` | 36296592 | Vetor de material templates | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `musical_forms_vector` | `0x02298e08` | 36277768 | Vetor de musical forms | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `occupations_vector` | `0x02298ec8` | 36277960 | Vetor de occupations | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `pants_vector` | `0x02196fa8` | 35221416 | Vetor de pants | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `plants_vector` | `0x0229d7d8` | 36296664 | Vetor de plants | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `poetic_forms_vector` | `0x02298dd8` | 36277720 | Vetor de poetic forms | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `quivers_vector` | `0x02196558` | 35218776 | Vetor de quivers | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `races_vector` | `0x0229d948` | 36297032 | Vetor de races | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `reactions_vector` | `0x022a8070` | 36339824 | Vetor de reactions | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `shapes_vector` | `0x022a7ef0` | 36339440 | Vetor de shapes | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `shields_vector` | `0x02196510` | 35218704 | Vetor de shields | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `shoes_vector` | `0x02197020` | 35221536 | Vetor de shoes | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `squad_vector` | `0x02294738` | 36259640 | Vetor de esquadrões | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `translation_vector` | `0x0229e5c0` | 36300224 | Vetor de translation | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `viewscreen_setupdwarfgame_vtable` | `0x01f21580` | 32642432 | Campo viewscreen setupdwarfgame vtable | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `weapons_vector` | `0x02196480` | 35218560 | Vetor de weapons | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `world_data` | `0x0229ca68` | 36293224 | Ponteiro para dados do mundo | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `world_site_type` | `0x0080` | 128 | Tipo de site mundial | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |

---

### armor_subtype_offsets

**Descrição:** Offsets para subtipos de armaduras

**Total de offsets:** 8

| Offset | Valor (Hex) | Valor (Dec) | Significado | Plataformas | Versões |
|--------|-------------|-------------|-------------|-------------|---------|
| `armor_adjective` | `0x00e8` | 232 | Campo armor adjective | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `armor_level` | `0x010c` | 268 | Campo armor level | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `chest_armor_properties` | `0x0118` | 280 | Campo chest armor properties | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `layer` | `0x0010` | 16 | Camada afetada | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `mat_name` | `0x00c8` | 200 | Campo mat name | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `other_armor_level` | `0x00cc` | 204 | Campo other armor level | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `other_armor_properties` | `0x00e8` | 232 | Campo other armor properties | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `pants_armor_properties` | `0x0128` | 296 | Campo pants armor properties | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |

---

### art_offsets

**Descrição:** Offsets para objetos de arte

**Total de offsets:** 1

| Offset | Valor (Hex) | Valor (Dec) | Significado | Plataformas | Versões |
|--------|-------------|-------------|-------------|-------------|---------|
| `name` | `0x0008` | 8 | Nome do esquadrão | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |

---

### caste_offsets

**Descrição:** Offsets para dados de castas (subtipos de raça)

**Total de offsets:** 14

| Offset | Valor (Hex) | Valor (Dec) | Significado | Plataformas | Versões |
|--------|-------------|-------------|-------------|-------------|---------|
| `adult_size` | `0x04d8` | 1240 | Tamanho de adult | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `baby_age` | `0x04c0` | 1216 | Campo baby age | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `body_info` | `0x06c0` | 1728 | Campo body info | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `caste_att_caps` | `0x1554` | 5460 | Campo caste att caps | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `caste_att_rates` | `0x1424` | 5156 | Campo caste att rates | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `caste_descr` | `0x0220` | 544 | Campo caste descr | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `caste_name` | `0x0020` | 32 | Campo caste name | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `caste_phys_att_ranges` | `0x1210` | 4624 | Campo caste phys att ranges | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `caste_trait_ranges` | `0x057c` | 1404 | Campo caste trait ranges | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `child_age` | `0x04c4` | 1220 | Campo child age | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `extracts` | `0x39e0` | 14816 | Campo extracts | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `flags` | `0x06a8` | 1704 | Flag de flags | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `shearable_tissues_vector` | `0x16e0` | 5856 | Vetor de shearable tissues | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `skill_rates` | `0x08c0` | 2240 | Campo skill rates | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |

---

### descriptor_offsets

**Total de offsets:** 2

| Offset | Valor (Hex) | Valor (Dec) | Significado | Plataformas | Versões |
|--------|-------------|-------------|-------------|-------------|---------|
| `color_name` | `0x0050` | 80 | Campo color name | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `shape_name_plural` | `0x0070` | 112 | Campo shape name plural | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |

---

### dwarf_offsets

**Descrição:** Offsets para dados de unidades/criaturas (anões, animais, invasores)

**Total de offsets:** 52

| Offset | Valor (Hex) | Valor (Dec) | Significado | Plataformas | Versões |
|--------|-------------|-------------|-------------|-------------|---------|
| `active_syndrome_vector` | `0x0c80` | 3200 | Vetor de active syndrome | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `affection_level` | `0x000c` | 12 | Campo affection level | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `animal_type` | `0x0138` | 312 | Tipo de animal (se for animal) | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `artifact_name` | `0x09e8` | 2536 | Campo artifact name | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `birth_time` | `0x0378` | 888 | Tick de nascimento no ano | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `birth_year` | `0x0374` | 884 | Ano de nascimento | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `blood` | `0x06a4` | 1700 | Nível de sangue | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `body_component_info` | `0x04d0` | 1232 | Campo body component info | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `body_size` | `0x06c8` | 1736 | Tamanho do corpo | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `caste` | `0x012c` | 300 | ID da casta (sub-raça) | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `civ` | `0x0140` | 320 | ID da civilização | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `counters1` | `0x07e0` | 2016 | Contadores diversos grupo 1 | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `counters2` | `0x07fc` | 2044 | Contadores diversos grupo 2 | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `counters3` | `0x0958` | 2392 | Contadores diversos grupo 3 | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `current_job` | `0x04b8` | 1208 | Ponteiro para o trabalho atual | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `curse` | `0x0820` | 2080 | Informações sobre maldições | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `curse_add_flags1` | `0x080c` | 2060 | Flag de curse adds1 | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `custom_profession` | `0x0080` | 128 | Campo custom profession | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `flags1` | `0x0110` | 272 | Flags de estado primárias | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `flags2` | `0x0114` | 276 | Flags de estado secundárias | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `flags3` | `0x0118` | 280 | Flags de estado terciárias | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `hist_id` | `0x0c10` | 3088 | ID da figura histórica | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `id` | `0x0130` | 304 | ID da necessidade | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `inventory` | `0x03f0` | 1008 | Vetor de itens no inventário | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `inventory_item_bodypart` | `0x000a` | 10 | Campo inventory item bodypart | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `inventory_item_mode` | `0x0008` | 8 | Campo inventory item mode | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `labors` | `0x0a98` | 2712 | Array de trabalhos habilitados | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `layer_status_vector` | `0x0048` | 72 | Vetor de layer status | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `limb_counters` | `0x0c18` | 3096 | Contador de limbers | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `meeting` | `0x0120` | 288 | Informações de reunião/encontro | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `mood` | `0x0348` | 840 | Estado de humor atual | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `mood_skill` | `0x04c0` | 1216 | Campo mood skill | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `name` | `0x0008` | 8 | Nome do esquadrão | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `pet_owner_id` | `0x03a4` | 932 | ID do dono (se for pet) | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `physical_attrs` | `0x05e4` | 1508 | Atributos físicos (força, agilidade, etc.) | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `profession` | `0x00a0` | 160 | Campo profession | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `race` | `0x00a4` | 164 | ID da raça da criatura | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `recheck_equipment` | `0x0268` | 616 | Campo recheck equipment | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `sex` | `0x012e` | 302 | Gênero (0=fêmea, 1=macho) | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `size_base` | `0x0690` | 1680 | Tamanho de size base | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `size_info` | `0x068c` | 1676 | Informações de tamanho | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `souls` | `0x0a60` | 2656 | Vetor de almas | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `specific_refs` | `0x01a8` | 424 | Campo specific refs | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `squad_id` | `0x01d8` | 472 | ID do esquadrão militar | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `squad_position` | `0x01dc` | 476 | Posição no esquadrão | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `states` | `0x0988` | 2440 | Estados especiais (migrante, adaptado caverna) | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `syn_sick_flag` | `0x004c` | 76 | Flag de syn sick | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `temp_mood` | `0x07f8` | 2040 | Humor temporário | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `turn_count` | `0x0920` | 2336 | Contador de turnos | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `unit_health_info` | `0x0d28` | 3368 | Campo unit health info | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `used_items_vector` | `0x0d30` | 3376 | Vetor de used items | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `wounds_vector` | `0x0590` | 1424 | Vetor de wounds | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |

---

### emotion_offsets

**Descrição:** Offsets para estados emocionais

**Total de offsets:** 7

| Offset | Valor (Hex) | Valor (Dec) | Significado | Plataformas | Versões |
|--------|-------------|-------------|-------------|-------------|---------|
| `emotion_type` | `0x0000` | 0 | Campo emotion type | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `level` | `0x0014` | 20 | Nível da necessidade | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `strength` | `0x0008` | 8 | Intensidade da emoção | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `sub_id` | `0x0010` | 16 | ID de sub | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `thought_id` | `0x000c` | 12 | ID de thought | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `year` | `0x0020` | 32 | Ano da emoção | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `year_tick` | `0x0024` | 36 | Ano de year tick | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |

---

### general_ref_offsets

**Descrição:** Offsets para referências gerais

**Total de offsets:** 3

| Offset | Valor (Hex) | Valor (Dec) | Significado | Plataformas | Versões |
|--------|-------------|-------------|-------------|-------------|---------|
| `artifact_id` | `0x0008` | 8 | ID de artifact | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `item_id` | `0x0008` | 8 | ID de item | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `ref_type` | `0x0010` | 16 | Campo ref type | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |

---

### health_offsets

**Descrição:** Offsets para informações de saúde

**Total de offsets:** 10

| Offset | Valor (Hex) | Valor (Dec) | Significado | Plataformas | Versões |
|--------|-------------|-------------|-------------|-------------|---------|
| `body_part_flags` | `0x0048` | 72 | Flag de body parts | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `layer_global_id` | `0x0068` | 104 | ID de layer global | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `layer_tissue` | `0x0020` | 32 | Campo layer tissue | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `layers_vector` | `0x0058` | 88 | Vetor de layers | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `names_plural_vector` | `0x00a8` | 168 | Vetor de names plural | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `names_vector` | `0x0090` | 144 | Vetor de names | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `number` | `0x0084` | 132 | Campo number | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `parent_id` | `0x0040` | 64 | ID de parent | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `tissue_flags` | `0x0020` | 32 | Flag de tissues | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `tissue_name` | `0x0030` | 48 | Campo tissue name | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |

---

### hist_entity_offsets

**Descrição:** Offsets para entidades históricas (civilizações)

**Total de offsets:** 11

| Offset | Valor (Hex) | Valor (Dec) | Significado | Plataformas | Versões |
|--------|-------------|-------------|-------------|-------------|---------|
| `assign_hist_id` | `0x0004` | 4 | ID de assign hist | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `assign_position_id` | `0x000c` | 12 | ID de assign position | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `assignments` | `0x1110` | 4368 | Campo assignments | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `beliefs` | `0x0d18` | 3352 | Campo beliefs | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `histfigs` | `0x00e8` | 232 | Campo histfigs | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `position_female_name` | `0x00d8` | 216 | Campo position female name | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `position_id` | `0x0020` | 32 | ID de position | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `position_male_name` | `0x0118` | 280 | Campo position male name | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `position_name` | `0x0098` | 152 | Campo position name | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `positions` | `0x10c0` | 4288 | Posições no esquadrão | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `squads` | `0x11c8` | 4552 | Campo squads | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |

---

### hist_event_offsets

**Descrição:** Offsets para eventos históricos

**Total de offsets:** 3

| Offset | Valor (Hex) | Valor (Dec) | Significado | Plataformas | Versões |
|--------|-------------|-------------|-------------|-------------|---------|
| `event_year` | `0x0008` | 8 | Ano de event | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `id` | `0x0020` | 32 | ID da necessidade | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `killed_hist_id` | `0x0024` | 36 | ID de killed hist | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |

---

### hist_figure_offsets

**Descrição:** Offsets para figuras históricas

**Total de offsets:** 13

| Offset | Valor (Hex) | Valor (Dec) | Significado | Plataformas | Versões |
|--------|-------------|-------------|-------------|-------------|---------|
| `current_ident` | `0x0030` | 48 | ID de currentent | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `fake_birth_time` | `0x0098` | 152 | Tempo de fake birth | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `fake_birth_year` | `0x0094` | 148 | Ano de fake birth | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `fake_name` | `0x0008` | 8 | Campo fake name | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `hist_fig_info` | `0x0130` | 304 | Campo hist fig info | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `hist_name` | `0x0038` | 56 | Campo hist name | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `hist_race` | `0x0002` | 2 | Campo hist race | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `id` | `0x00e0` | 224 | ID da necessidade | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `killed_counts_vector` | `0x00a8` | 168 | Vetor de killed counts | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `killed_race_vector` | `0x0018` | 24 | Vetor de killed race | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `killed_undead_vector` | `0x0090` | 144 | Vetor de killed undead | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `kills` | `0x0030` | 48 | Campo kills | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `reputation` | `0x0058` | 88 | Campo reputation | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |

---

### item_filter_offsets

**Total de offsets:** 4

| Offset | Valor (Hex) | Valor (Dec) | Significado | Plataformas | Versões |
|--------|-------------|-------------|-------------|-------------|---------|
| `item_subtype` | `0x0002` | 2 | Subtipo do item | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `mat_class` | `0x0004` | 4 | Campo mat class | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `mat_index` | `0x0008` | 8 | Campo mat index | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `mat_type` | `0x0006` | 6 | Campo mat type | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |

---

### item_offsets

**Descrição:** Offsets para itens genéricos

**Total de offsets:** 11

| Offset | Valor (Hex) | Valor (Dec) | Significado | Plataformas | Versões |
|--------|-------------|-------------|-------------|-------------|---------|
| `artifact_id` | `0x0000` | 0 | ID de artifact | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `artifact_name` | `0x0008` | 8 | Campo artifact name | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `general_refs` | `0x0038` | 56 | Campo general refs | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `id` | `0x001c` | 28 | ID da necessidade | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `item_def` | `0x00e0` | 224 | Campo item def | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `maker_race` | `0x00b4` | 180 | Campo maker race | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `mat_index` | `0x00b0` | 176 | Campo mat index | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `mat_type` | `0x00ac` | 172 | Campo mat type | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `quality` | `0x00b6` | 182 | Qualidade do item | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `stack_size` | `0x0078` | 120 | Tamanho da pilha | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `wear` | `0x009c` | 156 | Nível de desgaste | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |

---

### item_subtype_offsets

**Total de offsets:** 7

| Offset | Valor (Hex) | Valor (Dec) | Significado | Plataformas | Versões |
|--------|-------------|-------------|-------------|-------------|---------|
| `adjective` | `0x00a8` | 168 | Campo adjective | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `base_flags` | `0x0030` | 48 | Flag de bases | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `name` | `0x0068` | 104 | Nome do esquadrão | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `name_plural` | `0x0088` | 136 | Campo name plural | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `sub_type` | `0x0028` | 40 | Campo sub type | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `tool_adjective` | `0x00d8` | 216 | Campo tool adjective | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `tool_flags` | `0x00a8` | 168 | Flag de tools | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |

---

### job_details

**Descrição:** Offsets para trabalhos/tarefas

**Total de offsets:** 7

| Offset | Valor (Hex) | Valor (Dec) | Significado | Plataformas | Versões |
|--------|-------------|-------------|-------------|-------------|---------|
| `id` | `0x0014` | 20 | ID da necessidade | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `mat_category` | `0x0048` | 72 | Campo mat category | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `mat_index` | `0x0034` | 52 | Campo mat index | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `mat_type` | `0x0030` | 48 | Campo mat type | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `reaction` | `0x0020` | 32 | Campo reaction | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `reaction_skill` | `0x0080` | 128 | Campo reaction skill | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `sub_job_id` | `0x0050` | 80 | ID de sub job | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |

---

### material_offsets

**Descrição:** Offsets para dados de materiais

**Total de offsets:** 11

| Offset | Valor (Hex) | Valor (Dec) | Significado | Plataformas | Versões |
|--------|-------------|-------------|-------------|-------------|---------|
| `flags` | `0x0290` | 656 | Flag de flags | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `gas_name` | `0x00f8` | 248 | Campo gas name | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `inorganic_flags` | `0x0038` | 56 | Flag de inorganics | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `inorganic_materials_vector` | `0x01a8` | 424 | Vetor de inorganic materials | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `liquid_name` | `0x00d8` | 216 | ID de liquid name | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `paste_name` | `0x0138` | 312 | Campo paste name | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `powder_name` | `0x0118` | 280 | Campo powder name | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `prefix` | `0x0520` | 1312 | Campo prefix | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `pressed_name` | `0x0158` | 344 | Campo pressed name | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `reaction_class` | `0x04a8` | 1192 | Campo reaction class | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `solid_name` | `0x00b8` | 184 | ID de solid name | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |

---

### need_offsets

**Descrição:** Offsets para necessidades das unidades

**Total de offsets:** 4

| Offset | Valor (Hex) | Valor (Dec) | Significado | Plataformas | Versões |
|--------|-------------|-------------|-------------|-------------|---------|
| `deity_id` | `0x0004` | 4 | ID de deity | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `focus_level` | `0x0008` | 8 | Campo focus level | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `id` | `0x0000` | 0 | ID da necessidade | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `need_level` | `0x000c` | 12 | Campo need level | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |

---

### offsets

**Descrição:** Offsets diversos de linguagem

**Total de offsets:** 1

| Offset | Valor (Hex) | Valor (Dec) | Significado | Plataformas | Versões |
|--------|-------------|-------------|-------------|-------------|---------|
| `word_table` | `0x0050` | 80 | Campo word table | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |

---

### plant_offsets

**Descrição:** Offsets para dados de plantas

**Total de offsets:** 6

| Offset | Valor (Hex) | Valor (Dec) | Significado | Plataformas | Versões |
|--------|-------------|-------------|-------------|-------------|---------|
| `flags` | `0x0040` | 64 | Flag de flags | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `materials_vector` | `0x02a0` | 672 | Vetor de materials | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `name` | `0x0050` | 80 | Nome do esquadrão | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `name_leaf_plural` | `0x0110` | 272 | Campo name leaf plural | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `name_plural` | `0x0070` | 112 | Campo name plural | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `name_seed_plural` | `0x00d0` | 208 | Campo name seed plural | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |

---

### race_offsets

**Descrição:** Offsets para dados de raças (anão, elfo, humano, etc.)

**Total de offsets:** 13

| Offset | Valor (Hex) | Valor (Dec) | Significado | Plataformas | Versões |
|--------|-------------|-------------|-------------|-------------|---------|
| `adjective` | `0x0060` | 96 | Campo adjective | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `baby_name_plural` | `0x00a0` | 160 | Campo baby name plural | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `baby_name_singular` | `0x0080` | 128 | Campo baby name singular | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `castes_vector` | `0x0178` | 376 | Vetor de castes | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `child_name_plural` | `0x00e0` | 224 | Campo child name plural | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `child_name_singular` | `0x00c0` | 192 | Campo child name singular | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `flags` | `0x01a8` | 424 | Flag de flags | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `materials_vector` | `0x01f0` | 496 | Vetor de materials | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `name_plural` | `0x0040` | 64 | Campo name plural | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `name_singular` | `0x0020` | 32 | Campo name singular | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `pop_ratio_vector` | `0x0190` | 400 | Vetor de pop ratio | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `pref_string_vector` | `0x0148` | 328 | Vetor de pref string | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `tissues_vector` | `0x0208` | 520 | Vetor de tissues | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |

---

### soul_details

**Descrição:** Offsets para dados da alma

**Total de offsets:** 17

| Offset | Valor (Hex) | Valor (Dec) | Significado | Plataformas | Versões |
|--------|-------------|-------------|-------------|-------------|---------|
| `beliefs` | `0x0000` | 0 | Campo beliefs | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `combat_hardened` | `0x0130` | 304 | Campo combat hardened | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `current_focus` | `0x0184` | 388 | Campo current focus | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `emotions` | `0x0030` | 48 | Campo emotions | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `goal_realized` | `0x0028` | 40 | Campo goal realized | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `goals` | `0x0048` | 72 | Campo goals | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `likes_outdoors` | `0x012c` | 300 | Campo likes outdoors | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `mental_attrs` | `0x00ac` | 172 | Atributos mentais (inteligência, foco, etc.) | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `name` | `0x0008` | 8 | Nome do esquadrão | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `needs` | `0x0138` | 312 | Campo needs | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `orientation` | `0x0088` | 136 | Campo orientation | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `personality` | `0x0248` | 584 | Campo personality | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `preferences` | `0x0230` | 560 | Campo preferences | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `skills` | `0x0218` | 536 | Vetor de habilidades | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `stress_level` | `0x0120` | 288 | Campo stress level | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `traits` | `0x0080` | 128 | Campo traits | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `undistracted_focus` | `0x0188` | 392 | Campo undistracted focus | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |

---

### squad_offsets

**Descrição:** Offsets para dados de esquadrões militares

**Total de offsets:** 33

| Offset | Valor (Hex) | Valor (Dec) | Significado | Plataformas | Versões |
|--------|-------------|-------------|-------------|-------------|---------|
| `alert` | `0x00e8` | 232 | Estado de alerta | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `alias` | `0x0080` | 128 | Campo alias | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `ammunition` | `0x0140` | 320 | Campo ammunition | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `ammunition_qty` | `0x000c` | 12 | Campo ammunition qty | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `armor_vector` | `0x0080` | 128 | Vetor de armor | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `backpack` | `0x016c` | 364 | Campo backpack | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `carry_food` | `0x01c0` | 448 | Campo carry food | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `carry_water` | `0x01c2` | 450 | Campo carry water | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `equipment_update` | `0x01b8` | 440 | Campo equipment update | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `flask` | `0x0170` | 368 | Campo flask | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `gloves_vector` | `0x00c8` | 200 | Vetor de gloves | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `helm_vector` | `0x0098` | 152 | Vetor de helm | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `id` | `0x0000` | 0 | ID da necessidade | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `members` | `0x00a0` | 160 | Vetor de membros | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `name` | `0x0008` | 8 | Nome do esquadrão | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `orders` | `0x00b8` | 184 | Ordens atuais | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `pants_vector` | `0x00b0` | 176 | Vetor de pants | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `quiver` | `0x0168` | 360 | Campo quiver | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `sched_assign` | `0x0040` | 64 | Campo sched assign | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `sched_orders` | `0x0028` | 40 | Campo sched orders | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `sched_size` | `0x0058` | 88 | Tamanho de sched | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `schedules` | `0x00d0` | 208 | Campo schedules | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `shield_vector` | `0x00f8` | 248 | Vetor de shield | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `shoes_vector` | `0x00e0` | 224 | Vetor de shoes | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `uniform_indiv_choice` | `0x0030` | 48 | Campo uniform indiv choice | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `uniform_item_filter` | `0x0004` | 4 | Campo uniform item filter | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `uniform_spec_item_subtype` | `0x0006` | 6 | Campo uniform spec item subtype | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `uniform_spec_item_type` | `0x0004` | 4 | Campo uniform spec item type | linux, windows | v0.50.13-classic_linux64, v0.50.13-itch_linux64... |
| `uniform_spec_mat_class` | `0x0008` | 8 | Campo uniform spec mat class | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `uniform_spec_mat_index` | `0x000c` | 12 | Campo uniform spec mat index | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `uniform_spec_mat_type` | `0x000a` | 10 | Campo uniform spec mat type | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `uniform_spec_uniform_item_filter` | `0x0004` | 4 | Campo uniform spec uniform item filter | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `weapon_vector` | `0x0110` | 272 | Vetor de weapon | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |

---

### syndrome_offsets

**Descrição:** Offsets para síndromes (doenças, maldições)

**Total de offsets:** 7

| Offset | Valor (Hex) | Valor (Dec) | Significado | Plataformas | Versões |
|--------|-------------|-------------|-------------|-------------|---------|
| `cie_effects` | `0x0020` | 32 | Efeitos da síndrome | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `cie_end` | `0x0018` | 24 | Fim da síndrome | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `cie_first_perc` | `0x0098` | 152 | Campo cie first perc | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `cie_ment` | `0x00cc` | 204 | Campo cie ment | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `cie_phys` | `0x00b0` | 176 | Campo cie phys | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `syn_classes_vector` | `0x00c8` | 200 | Vetor de syn classes | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `trans_race_vec` | `0x00e0` | 224 | Campo trans race vec | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |

---

### unit_wound_offsets

**Descrição:** Offsets para ferimentos de unidades

**Total de offsets:** 11

| Offset | Valor (Hex) | Valor (Dec) | Significado | Plataformas | Versões |
|--------|-------------|-------------|-------------|-------------|---------|
| `bleeding` | `0x006c` | 108 | Estado de sangramento | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `cur_pen` | `0x0098` | 152 | Campo cur pen | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `effects_vector` | `0x0048` | 72 | Vetor de effects | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `flags1` | `0x0064` | 100 | Flags de estado primárias | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `flags2` | `0x0068` | 104 | Flags de estado secundárias | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `general_flags` | `0x002c` | 44 | Flag de generals | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `id` | `0x0004` | 4 | ID da necessidade | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `layer` | `0x0006` | 6 | Camada afetada | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `max_pen` | `0x009a` | 154 | Campo max pen | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `pain` | `0x0070` | 112 | Nível de dor | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `parts` | `0x0008` | 8 | Partes do corpo afetadas | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |

---

### viewscreen_offsets

**Descrição:** Offsets para telas do jogo

**Total de offsets:** 3

| Offset | Valor (Hex) | Valor (Dec) | Significado | Plataformas | Versões |
|--------|-------------|-------------|-------------|-------------|---------|
| `child` | `0x0008` | 8 | Campo child | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `setupdwarfgame_units` | `0x1e98` | 7832 | Campo setupdwarfgame units | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `view` | `0x0008` | 8 | Campo view | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |

---

### weapon_subtype_offsets

**Descrição:** Offsets para subtipos de armas

**Total de offsets:** 5

| Offset | Valor (Hex) | Valor (Dec) | Significado | Plataformas | Versões |
|--------|-------------|-------------|-------------|-------------|---------|
| `ammo` | `0x00d8` | 216 | Campo ammo | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `melee_skill` | `0x00d0` | 208 | Campo melee skill | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `multi_size` | `0x00fc` | 252 | Tamanho de multi | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `ranged_skill` | `0x00d2` | 210 | Campo ranged skill | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `single_size` | `0x00f8` | 248 | Tamanho de single | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |

---

### word_offsets

**Descrição:** Offsets para estruturas de palavras e linguagem

**Total de offsets:** 14

| Offset | Valor (Hex) | Valor (Dec) | Significado | Plataformas | Versões |
|--------|-------------|-------------|-------------|-------------|---------|
| `adjective` | `0x0060` | 96 | Campo adjective | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `base` | `0x0000` | 0 | Campo base | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `first_name` | `0x0000` | 0 | Primeiro nome | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `language_id` | `0x006c` | 108 | ID de language | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `nickname` | `0x0020` | 32 | Apelido | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `noun_plural` | `0x0040` | 64 | Campo noun plural | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `noun_singular` | `0x0020` | 32 | Campo noun singular | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `past_participle_verb` | `0x0100` | 256 | Campo past participle verb | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `past_simple_verb` | `0x00e0` | 224 | Campo past simple verb | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `present_participle_verb` | `0x0120` | 288 | Campo present participle verb | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `present_simple_verb` | `0x00c0` | 192 | Campo present simple verb | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `verb` | `0x00a0` | 160 | Campo verb | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `word_type` | `0x005c` | 92 | Campo word type | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |
| `words` | `0x0040` | 64 | Campo words | linux, windows | v0.50.10-classic_linux64, v0.50.10-itch_linux64... |

---

