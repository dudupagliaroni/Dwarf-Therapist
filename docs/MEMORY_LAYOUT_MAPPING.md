# Dwarf Therapist - Mapeamento de Memory Layout v0.53.10

**Data:** 2026-01-16  
**Versão DF:** v0.53.10 win64 STEAM  
**Checksum:** `0x69637830`

---

## Visão Geral da Arquitetura de Dados

O Dwarf Therapist lê dados diretamente da memória do Dwarf Fortress usando offsets definidos em arquivos INI. A estrutura principal segue esta hierarquia:

```
┌─────────────────────────────────────────────────────────────────┐
│                    MEMÓRIA DO DWARF FORTRESS                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [addresses]                                                     │
│       │                                                          │
│       ├── creature_vector (0x1423a0400)                         │
│       │       └── Array de ponteiros para Unit structs          │
│       │                                                          │
│       ├── active_creature_vector (0x1423a0418)                  │
│       │       └── Apenas criaturas ativas (visíveis)            │
│       │                                                          │
│       ├── races_vector (0x1424a7db8)                            │
│       │       └── Definições de raças (Dwarf, Elf, etc)         │
│       │                                                          │
│       ├── squad_vector (0x14249eb10)                            │
│       │       └── Esquadrões militares                          │
│       │                                                          │
│       └── historical_figures_vector (0x1424b5060)               │
│               └── Figuras históricas                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Estrutura de uma Unidade (Dwarf)

Cada entrada no `creature_vector` aponta para uma estrutura de unidade:

```
Unit Struct (Dwarf)
├── 0x0008  name                    → Nome completo (df_string)
├── 0x0080  custom_profession       → Profissão personalizada
├── 0x00a0  profession              → ID da profissão (WORD)
├── 0x00a4  race                    → ID da raça (WORD)
├── 0x012c  caste                   → ID do caste (BYTE)
├── 0x012e  sex                     → Sexo (BYTE: 0=F, 1=M)
├── 0x0130  id                      → ID único da unidade (DWORD)
├── 0x0140  civ                     → ID da civilização
├── 0x0110  flags1                  → Flags de estado 1
├── 0x0114  flags2                  → Flags de estado 2
├── 0x0118  flags3                  → Flags de estado 3
├── 0x01f0  squad_id                → ID do esquadrão (-1 se nenhum)
├── 0x01f4  squad_position          → Posição no esquadrão
├── 0x0360  mood                    → Estado de humor/mood
├── 0x038c  birth_year              → Ano de nascimento
├── 0x0390  birth_time              → Tick de nascimento
├── 0x03bc  pet_owner_id            → ID do dono (se for pet)
├── 0x0408  inventory               → Vector de itens equipados
├── 0x04d8  current_job             → Ponteiro para job atual
├── 0x0604  physical_attrs          → Array de atributos físicos
├── 0x06c4  blood                   → Nível de sangue
├── 0x06e8  body_size               → Tamanho corporal (cm³)
├── 0x0a80  souls                   → Vector de almas (geralmente 1)
├── 0x0ab8  labors                  → Bitfield de labors (94 labors)
├── 0x0c30  hist_id                 → ID da figura histórica
├── 0x0ca0  active_syndrome_vector  → Síndromes ativas
├── 0x0d48  unit_health_info        → Informações de saúde
└── 0x05b0  wounds_vector           → Vector de ferimentos
```

---

## Estrutura da Alma (Soul)

Cada unidade tem um vetor de almas (offset `0x0a80`). A alma contém personalidade, skills e emoções:

```
Soul Struct
├── 0x0008  name                → Nome da alma
├── 0x0088  orientation         → Orientação sexual
├── 0x00ac  mental_attrs        → Array de atributos mentais
│
├── 0x0218  skills              → VECTOR de Skills
│           └── Skill Struct
│               ├── id          → ID do skill (ver game_data.ini)
│               ├── level       → Nível (0-20+)
│               └── experience  → XP atual
│
├── 0x0230  preferences         → VECTOR de Preferências
│           └── Preference Struct
│               ├── type        → Tipo (material, item, creature, etc)
│               ├── item_type   → Subtipo do item
│               └── matflags    → Flags de material
│
├── 0x0248  personality         → Estrutura de Personalidade
│           ├── 0x0000 beliefs  → VECTOR de crenças
│           ├── 0x0030 emotions → VECTOR de emoções recentes
│           ├── 0x0048 goals    → VECTOR de objetivos de vida
│           └── 0x0080 traits   → Array de traits (50 valores)
│
├── 0x0120  stress_level        → Nível de stress (INT32)
├── 0x0138  needs               → VECTOR de necessidades
├── 0x0184  current_focus       → Foco atual (INT32)
├── 0x0188  undistracted_focus  → Foco sem distrações
├── 0x012c  likes_outdoors      → Preferência por ar livre
└── 0x0130  combat_hardened     → Nível de endurecimento
```

---

## Mapeamento do Painel de Detalhes do Dwarf Therapist

### Seção: Informações Básicas

| Campo na UI | Offset | Seção INI | Tipo |
|-------------|--------|-----------|------|
| Nome (Rovod Ralbisek) | `0x0008` | `[dwarf_offsets] name` | df_string |
| Caste (Dwarf) | `0x012c` | `[dwarf_offsets] caste` | BYTE → races_vector |
| Age (39 Years Old) | `0x038c` | `[dwarf_offsets] birth_year` | Calculado: current_year - birth_year |
| Size (67,540 cm³) | `0x06e8` | `[dwarf_offsets] body_size` | DWORD |
| Profession (Miner) | `0x00a0` | `[dwarf_offsets] profession` | BYTE → game_data.ini |
| Happiness | `souls→0x0120` | `[soul_details] stress_level` | INT32 (negativo = feliz) |

### Seção: Thoughts & Emotions

Origem: `souls` → `personality` → `emotions` vector

| Campo | Offset Chain | Descrição |
|-------|--------------|-----------|
| Emotion Type | `souls→personality→emotions[i]→0x0000` | Tipo da emoção (enum) |
| Thought ID | `souls→personality→emotions[i]→0x000c` | ID do pensamento |
| Strength | `souls→personality→emotions[i]→0x0008` | Intensidade |
| Year | `souls→personality→emotions[i]→0x0020` | Ano do evento |
| Year Tick | `souls→personality→emotions[i]→0x0024` | Tick do evento |

**Exemplos de pensamentos mostrados:**
- "uneasiness after being unable to acquire something"
- "boredom after being unable to pray"
- "delight after watching a performance"
- "euphoric due to inebriation"
- "satisfied upon improving mining"

### Seção: Personality

Origem: `souls` → `personality` → `traits` (array de 50 INT16)

| Trait Index | Nome | Valores |
|-------------|------|---------|
| 0 | ANXIETY_PROPENSITY | -100 a 100 |
| 1 | ANGER_PROPENSITY | -100 a 100 |
| 2 | DEPRESSION_PROPENSITY | -100 a 100 |
| ... | ... | ... |

**Mapeamento de texto:**
- "Can handle stress" → ANXIETY_PROPENSITY baixo
- "Is very greedy" → GREED alto
- "Likes to brawl" → VIOLENT alto
- "Does not have a great aesthetic sensitivity" → AESTHETIC baixo

### Seção: Preferences

Origem: `souls` → `preferences` vector

| Campo | Descrição |
|-------|-----------|
| Material prefs | "Likes rutile, steel, jasper opal" |
| Creature prefs | "cats, giant hippos, figurines" |
| Plant prefs | "bambara groundnut plants" |
| Food prefs | "tiger shark and sunshine" |
| Hate prefs | "Hates purring maggots" |

### Seção: Skills

Origem: `souls` → `skills` vector

| Skill na UI | Estrutura |
|-------------|-----------|
| [18] Legendary +3 Miner | level=18, id=0 (MINING) |
| [7] Adept Furnace Operator | level=7, id=X |
| [3] Competent Speaker | level=3, id=X |

---

## Endereços Globais Importantes

```ini
[addresses]
# Tempo do jogo
cur_year_tick=0x14233e724      # Tick atual do ano
current_year=0x14232ae40       # Ano atual

# Civilização do jogador
dwarf_civ_index=0x14234ea00    # ID da civilização dwarf
dwarf_race_index=0x14234ea0c   # ID da raça dwarf

# Vetores principais
creature_vector=0x1423a0400     # TODAS as criaturas
active_creature_vector=0x1423a0418  # Criaturas ativas

# Itens e equipamentos
weapons_vector=0x1423a07e8
armor_vector=0x1423a1388
shields_vector=0x1423a0878

# Definições de raças e materiais
races_vector=0x1424a7db8
inorganics_vector=0x1424a7c18  # Materiais inorgânicos
plants_vector=0x1424a7c48

# Esquadrões e atividades
squad_vector=0x14249eb10
activities_vector=0x14249eb70
```

---

## Flags de Filtro

### invalid_flags_1 (Criaturas a ignorar)

| Flag | Valor | Descrição |
|------|-------|-----------|
| Merchant | 0x00000040 | Mercadores |
| Diplomat | 0x00000800 | Diplomatas/Liaison |
| Invader | 0x00020000 | Invasores |
| Hostile | 0x00080000 | Hostis |
| Ambusher | 0x00600000 | Emboscadores |
| Caravan | 0x00000080 | Parte de caravana |
| Inactive | 0x00000002 | Não em jogo |
| Marauder | 0x00000010 | Saqueadores |

### invalid_flags_2

| Flag | Valor | Descrição |
|------|-------|-----------|
| Dead | 0x00000080 | Morto |
| Underworld | 0x00040000 | Do submundo |
| Resident | 0x00080000 | Residente (não cidadão) |
| Visitor | 0x00800000 | Visitante |

---

## Diferenças v0.52.05 → v0.53.10

| Offset | v0.52.05 | v0.53.10 | Delta |
|--------|----------|----------|-------|
| creature_vector | 0x14234d370 | 0x1423a0400 | +0x53090 |
| specific_refs | 0x01a8 | 0x01c0 | +0x18 |
| squad_id | 0x01d8 | 0x01f0 | +0x18 |
| mood | 0x0348 | 0x0360 | +0x18 |
| birth_year | 0x0374 | 0x038c | +0x18 |
| current_job | 0x04b8 | 0x04d8 | +0x20 |
| physical_attrs | 0x05e4 | 0x0604 | +0x20 |
| souls | 0x0a60 | 0x0a80 | +0x20 |
| labors | 0x0a98 | 0x0ab8 | +0x20 |
| skill_rates | 0x08c0 | 0x08d8 | +0x18 |

**Padrão observado:** A maioria dos offsets de dwarf aumentou entre 0x18-0x20 bytes, sugerindo adição de novos campos na estrutura de unidade.

---

## Referências

- **game_data.ini:** Definições de skills, profissões, labors
- **Código fonte:** `src/dwarf.cpp`, `src/dfinstance.cpp`, `src/memorylayout.cpp`
- **DFHack df-structures:** https://github.com/DFHack/df-structures
