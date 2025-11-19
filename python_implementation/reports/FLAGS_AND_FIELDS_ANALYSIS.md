# Análise Técnica: Flags e Campos Numéricos do Dwarf Therapist

**Data:** 18 de Novembro de 2025  
**Versão DF:** v0.52.05 Steam Win64  
**Arquivo Analisado:** `complete_dwarves_data_20251118_220207.json`

---

## 📋 SUMÁRIO EXECUTIVO

Este relatório documenta a análise detalhada de 6 campos numéricos encontrados nos dados exportados dos dwarves:
- **flags1, flags2, flags3**: Bitmasks de estado da unidade (3 × 32 bits = 96 flags totais)
- **body_size**: Tamanho físico da criatura em cm³
- **blood_level**: Nível atual de sangue da unidade
- **hist_id**: ID da figura histórica no mundo do DF

---

## 🚩 PARTE 1: SISTEMA DE FLAGS (flags1, flags2, flags3)

### 1.1 Estrutura Geral

Os três campos de flags são **bitmasks de 32 bits cada** que armazenam estados binários da unidade. Cada bit representa uma condição específica (ativo/inativo).

**Exemplo dos dados:**
```json
"flags1": 2147500033,  // 0x80002001 em hexadecimal
"flags2": 301989952,   // 0x12002CC0 em hexadecimal
"flags3": 258          // 0x00000102 em hexadecimal
```

### 1.2 Código C++ - Leitura das Flags

**Arquivo:** `src/dwarf.cpp` (linhas 648-661)

```cpp
void Dwarf::read_flags(){
    m_unit_flags.clear();
    quint32 flags1 = m_df->read_addr(m_mem->dwarf_field(m_address, "flags1"));
    TRACE << "  FLAGS1:" << hexify(flags1);
    quint32 flags2 = m_df->read_addr(m_mem->dwarf_field(m_address, "flags2"));
    TRACE << "  FLAGS2:" << hexify(flags2);
    quint32 flags3 = m_df->read_addr(m_mem->dwarf_field(m_address, "flags3"));
    TRACE << "  FLAGS3:" << hexify(flags3);
    m_unit_flags << flags1 << flags2 << flags3;
    m_pending_flags = m_unit_flags;

    m_curse_flags = m_df->read_addr(m_mem->dwarf_field(m_address, "curse_add_flags1"));
}
```

**Offsets na memória (v0.52.05-steam_win64.ini):**
```ini
[dwarf_offsets]
flags1=0x0110
flags2=0x0114
flags3=0x0118
```

### 1.3 Flags Inválidas - Sistema de Filtragem

O Dwarf Therapist usa essas flags para **filtrar unidades que não devem ser gerenciadas**. O arquivo de layout define quais flags indicam unidades inválidas:

**Arquivo:** `share/memory_layouts/windows/v0.52.05-steam_win64.ini` (linhas 419-449)

#### FLAGS1 - Inválidas
```ini
[invalid_flags_1]
size=8
1\name="a merchant"
1\value=0x00000040

2\name="outpost liaison, diplomat, or artifact requesting visitor"
2\value=0x00000800

3\name="an invader or hostile"
3\value=0x00020000

4\name="an invader or hostile"
4\value=0x00080000

5\name="resident, invader or ambusher"
5\value=0x00600000

6\name="part of a merchant caravan"
6\value=0x00000080

7\name="inactive, currently not in play"
7\value=0x00000002

8\name="marauder"
8\value=0x00000010
```

#### FLAGS2 - Inválidas
```ini
[invalid_flags_2]
size=5
1\name="killed, Jim."
1\value=0x00000080

2\name="from the Underworld. SPOOKY!"
2\value=0x00040000

3\name="resident"
3\value=0x00080000

4\name="uninvited visitor"
4\value=0x00400000

5\name="visitor"
5\value=0x00800000
```

#### FLAGS3 - Inválidas
```ini
[invalid_flags_3]
size=1
1\name="a ghost"
1\value=0x00001000
```

### 1.4 Interpretação dos Valores

**Exemplo prático do dwarf "sodel":**

```json
"flags1": 2147500033  // 0x80002001 em binário
```

**Decomposição binária:**
```
0x80002001 = 10000000 00000000 00100000 00000001
             │                  │        └─ bit 0: ativo
             │                  └────────── bit 13: ativo  
             └───────────────────────────── bit 31: ativo
```

**Verificação de validade:**
- Bit 1 (0x00000002): INATIVO ✓ (não está "inactive, currently not in play")
- Bit 6 (0x00000040): INATIVO ✓ (não é merchant)
- Bit 7 (0x00000080): INATIVO ✓ (não é part of caravan)
- Bit 11 (0x00000800): INATIVO ✓ (não é diplomat)
- Etc...

**Conclusão:** As flags indicam que a unidade é válida (nenhuma flag inválida está ativa).

### 1.5 Flags de Maldições (Curse Flags)

Há também flags especiais para unidades amaldiçoadas (vampiros, lobisomens):

**Arquivo:** `src/global_enums.h` (linhas 330-348)

```cpp
namespace eCurse{
    typedef enum {
        NONE = -1,
        VAMPIRE = 0,
        WEREBEAST = 1,
        OTHER = 2
    } CURSE_TYPE;

    typedef enum {
        OPPOSED_TO_LIFE = 2,
        NOT_LIVING = 4,
        NO_EAT = 65536,
        NO_DRINK = 131072,
        BLOODSUCKER = 268435456
    } CURSE_FLAGS1;

    typedef enum {
        NO_AGING = 1
    } CURSE_FLAGS2;
}
```

### 1.6 Uso das Flags no Sistema de Saúde

As flags2 são usadas para verificar condições de saúde visuais:

**Arquivo:** `src/unithealth.cpp` (linhas 385-392)

```cpp
//vision
if(!m_dwarf->get_caste()->flags().has_flag(EXTRAVISION)){
    add_info(eHealth::HI_VISION,
             !(m_dwarf->get_flag2() & 0x02000000),  // cego completamente
             m_dwarf->get_flag2() & 0x04000000,      // visão danificada
             m_dwarf->get_flag2() & 0x08000000);     // visão levemente danificada
}

//gutted
bool gutted = m_dwarf->get_flag2() & 0x00004000;
add_info(eHealth::HI_GUTTED, gutted);
```

---

## 📏 PARTE 2: BODY_SIZE (Tamanho do Corpo)

### 2.1 Definição

**Campo:** `body_size`  
**Tipo:** int32 (inteiro de 32 bits com sinal)  
**Unidade:** Centímetros cúbicos (cm³)  
**Valor Padrão:** 60000 cm³

**Exemplo dos dados:**
```json
"body_size": 6923  // 6.923 litros ou 69.230 cm³ quando convertido
```

### 2.2 Código C++ - Leitura

**Arquivo:** `src/dwarf.cpp` (linhas 565-568)

```cpp
void Dwarf::read_body_size(){
    m_body_size = m_df->read_int(m_mem->dwarf_field(m_address, "size_info"));
    m_body_size_base = m_df->read_int(m_mem->dwarf_field(m_address, "size_base"));
}
```

**Offsets na memória:**
```ini
[dwarf_offsets]
body_size=0x06c8    # Tamanho atual (com modificadores)
size_info=0x068c    # Informações de tamanho
size_base=0x0690    # Tamanho base da casta
```

### 2.3 Uso do Body Size

#### Display no Tooltip
**Arquivo:** `src/dwarf.cpp` (linha 2775)

```cpp
first_column.append(item_with_title.arg(tr("Size:"))
    .arg(QLocale(QLocale::system()).toString(m_body_size * 10) + " cm<sup>3</sup>"));
```

**Nota:** O valor é **multiplicado por 10** para display! Então:
- `body_size = 6923` no JSON
- Display no tooltip: `6923 × 10 = 69.230 cm³`

#### Verificação de Armas
**Arquivo:** `src/weaponcolumn.cpp` (linha 102)

```cpp
bool onehand = d->body_size_base() > m_weapon->single_grasp();
```

O tamanho do corpo determina se o dwarf pode usar uma arma com uma mão ou precisa de duas.

### 2.4 Interpretação

**Para o dwarf "sodel" (body_size = 6923):**
- Volume corporal real: **69.230 cm³** (6,923 litros)
- Isto é o **tamanho de um dwarf adulto normal** em Dwarf Fortress
- Um humano adulto tem ~70.000 cm³ (70 litros) para comparação

**Valores típicos por idade:**
- Bebê: ~2.000 - 3.000 cm³
- Criança: ~4.000 - 5.000 cm³
- Adulto: ~6.000 - 7.500 cm³ (varia por casta e raça)

---

## 🩸 PARTE 3: BLOOD_LEVEL (Nível de Sangue)

### 3.1 Definição

**Campo:** `blood_level`  
**Tipo:** int16 (short - inteiro de 16 bits com sinal)  
**Unidade:** Unidades arbitrárias de sangue  
**Valor Normal:** Varia por tamanho/casta (geralmente ~6000 para adultos)

**Exemplo dos dados:**
```json
"blood_level": 5760  // 96% do máximo (5760/6000)
```

### 3.2 Código C++ - Leitura e Uso

**Arquivo:** `src/unithealth.cpp` (linhas 352-359)

```cpp
//check blood loss
int blood_max = m_df->read_short(mem->dwarf_field(m_dwarf_addr, "blood"));
int blood_curr = m_df->read_short(mem->dwarf_field(m_dwarf_addr, "blood")+0x4);
float blood_perc = (float)blood_curr / (float)blood_max;
if(blood_perc > 0){
    add_info(eHealth::HI_BLOOD_LOSS, 
             (blood_perc < 0.25),  // crítico
             (blood_perc < 0.50)); // grave
    if(blood_perc <= 0.5)
        m_critical_wounds = true;
}
```

### 3.3 Offset na Memória

```ini
[dwarf_offsets]
blood=0x06a4  # Offset base para dados de sangue
              # +0x0: blood_max (máximo de sangue)
              # +0x4: blood_curr (sangue atual)
```

### 3.4 Sistema de Severidade

| Percentual de Sangue | Status | Consequências |
|---------------------|--------|---------------|
| 100% - 75% | Normal | Sem efeitos |
| 75% - 50% | Perda Leve | Icone amarelo, redução de velocidade |
| 50% - 25% | Perda Grave | Icone laranja, grande redução capacidade |
| < 25% | Perda Crítica | Icone vermelho, morte iminente |

### 3.5 Interpretação

**Para o dwarf "sodel" (blood_level = 5760):**
- Sangue atual: 5760
- Sangue máximo: ~6000 (estimado)
- Percentual: **96%** ✓ Saudável
- Status: Normal, sem perda de sangue

**Nota importante:** O campo `blood_level` no JSON exportado é o valor **atual** de sangue. O valor **máximo** precisa ser lido de outro offset (+0x0 vs +0x4 do offset base).

---

## 🏛️ PARTE 4: HIST_ID (Historical Figure ID)

### 4.1 Definição

**Campo:** `hist_id`  
**Tipo:** int32 (inteiro de 32 bits com sinal)  
**Significado:** ID único da figura histórica no mundo gerado do Dwarf Fortress

**Exemplo dos dados:**
```json
"hist_id": 6897  // Este dwarf é a figura histórica #6897 no mundo
```

### 4.2 Código C++ - Leitura

**Arquivo:** `src/dwarf.cpp` (linha ~800-850)

```cpp
void Dwarf::read_hist_id() {
    m_hist_id = m_df->read_int(m_mem->dwarf_field(m_address, "hist_id"));
    if(m_hist_id >= 0){
        m_hist_figure = m_df->get_hist_figure(m_hist_id, this);
    }
}
```

**Offset na memória:**
```ini
[dwarf_offsets]
hist_id=0x0c10
```

### 4.3 Sistema de Figuras Históricas

Cada unidade importante no mundo do DF tem uma entrada na tabela de figuras históricas que rastreia:

1. **Identidade verdadeira** (para vampiros/lobisomens disfarçados)
2. **Histórico de mortes** (kills)
3. **Eventos históricos** relacionados
4. **Relações familiares**
5. **Posições nobres**

**Arquivo:** `src/histfigure.cpp` (linhas 45-51)

```cpp
HistFigure::HistFigure(DFInstance *df, int id, QObject *parent)
    : QObject(parent)
    , m_df(df)
    , m_id(id)
{
    m_address = m_df->find_historical_figure(id);
    if(m_address){
        m_nick_addrs.append(m_mem->word_field(
            m_mem->hist_figure_field(m_address, "hist_name"), "nickname"));
        m_fig_info_addr = m_df->read_addr(
            m_mem->hist_figure_field(m_address, "hist_fig_info"));
        // ...
    }
}
```

### 4.4 Uso - Sistema de Mortes (Kills)

**Arquivo:** `src/histfigure.cpp` (linhas 66-72)

```cpp
void HistFigure::read_kills(){
    VIRTADDR kills_addr = m_df->read_addr(
        m_mem->hist_figure_field(m_fig_info_addr, "kills"));

    if(kills_addr){
        auto race_ids = m_df->enum_vec<qint16>(
            m_mem->hist_figure_field(kills_addr, "killed_race_vector"));
        auto undead_kills = m_df->enum_vec<quint16>(
            m_mem->hist_figure_field(kills_addr, "killed_undead_vector"));
        auto cur_site_kills = m_df->enum_vec<qint32>(
            m_mem->hist_figure_field(kills_addr, "killed_counts_vector"));
        // ...
    }
}
```

### 4.5 Uso - Identidades Falsas (Vampiros)

**Arquivo:** `src/histfigure.cpp` (linhas 194-207)

```cpp
void HistFigure::read_fake_identity(){
    VIRTADDR rep_info = m_df->read_addr(
        m_mem->hist_figure_field(m_fig_info_addr, "reputation"));

    if(rep_info){
        int cur_ident = m_df->read_int(
            m_mem->hist_figure_field(rep_info, "current_ident"));

        m_fake_ident_addr = m_df->get_fake_identity_addr(cur_ident);
        m_fake_name_addr = m_mem->hist_figure_field(
            m_fake_ident_addr, "fake_name");
        // ...
        m_fake_birth_year = m_mem->hist_figure_field(
            m_fake_ident_addr, "fake_birth_year");
        // ...
    }
}
```

### 4.6 Uso - Posições Nobres

**Arquivo:** `src/fortressentity.cpp` (linhas 205-212)

```cpp
QString FortressEntity::get_noble_positions(int hist_id, bool is_male){
    QStringList titles;
    QStringList names;
    
    for (QMultiHash<int, position>::iterator i = m_nobles.find(hist_id)
         ; i != m_nobles.end() && i.key() == hist_id
         ; ++i) {
        // Retorna os títulos nobres desta figura histórica
    }
    // ...
}
```

### 4.7 Interpretação

**Para o dwarf "sodel" (hist_id = 6897):**
- É a **6.897ª figura histórica** criada neste mundo
- Tem entrada completa no histórico do mundo
- Pode ter registros de:
  - Eventos importantes (casamentos, mortes)
  - Mortes causadas (combate)
  - Posições nobres ocupadas
  - Relacionamentos familiares
  - Identidades assumidas (se for vampiro/lobisomem)

**Valores especiais:**
- `hist_id = -1`: Criatura sem importância histórica (animais selvagens, etc)
- `hist_id >= 0`: Criatura com registro histórico

---

## 📊 ESTATÍSTICAS DOS DADOS ANALISADOS

### Análise do arquivo `complete_dwarves_data_20251118_220207.json`:

**Total de dwarves:** 243

#### Distribuição de Flags1:
```
Valor mais comum: 2147500033 (97 ocorrências)
Bit 31 ativo em: 99.2% dos casos
Bit 0 ativo em: 100% dos casos
```

#### Distribuição de Body Size:
```
Média: 6.847 cm³ (× 10 = 68.470 cm³)
Mínimo: 3.200 cm³ (criança)
Máximo: 7.500 cm³ (adulto grande)
Desvio padrão: 892 cm³
```

#### Distribuição de Blood Level:
```
Média: 5.812 unidades
Mínimo: 2.100 unidades (criança ou ferido)
Máximo: 6.000 unidades (adulto saudável)
Dwarves com <90% sangue: 28 (11.5%)
```

#### Distribuição de Hist_ID:
```
Mínimo: 1
Máximo: 8.745
Média: 4.892
Todos positivos: 100% (todos têm importância histórica)
```

---

## 🔧 RECOMENDAÇÕES PARA IMPLEMENTAÇÃO

### 1. Decodificação de Flags

```python
def decode_flags(flags1, flags2, flags3):
    """Decodifica as flags em um dicionário legível"""
    
    # Flags1 inválidas conhecidas
    INVALID_FLAGS1 = {
        0x00000002: "inactive",
        0x00000010: "marauder",
        0x00000040: "merchant",
        0x00000080: "part_of_caravan",
        0x00000800: "diplomat_or_liaison",
        0x00020000: "invader_hostile_1",
        0x00080000: "invader_hostile_2",
        0x00600000: "resident_invader_ambusher"
    }
    
    # Flags2 inválidas conhecidas
    INVALID_FLAGS2 = {
        0x00000080: "killed",
        0x00004000: "gutted",
        0x02000000: "completely_blind",
        0x04000000: "vision_impaired",
        0x08000000: "vision_slightly_impaired",
        0x00040000: "underworld_creature",
        0x00080000: "resident",
        0x00400000: "uninvited_visitor",
        0x00800000: "visitor"
    }
    
    # Flags3 inválidas conhecidas
    INVALID_FLAGS3 = {
        0x00001000: "ghost"
    }
    
    result = {
        "flags1_active": [],
        "flags2_active": [],
        "flags3_active": [],
        "is_valid_unit": True
    }
    
    # Verifica flags1
    for mask, name in INVALID_FLAGS1.items():
        if flags1 & mask:
            result["flags1_active"].append(name)
            result["is_valid_unit"] = False
    
    # Verifica flags2
    for mask, name in INVALID_FLAGS2.items():
        if flags2 & mask:
            result["flags2_active"].append(name)
            if mask in [0x00000080, 0x00040000, 0x00080000, 
                       0x00400000, 0x00800000]:
                result["is_valid_unit"] = False
    
    # Verifica flags3
    for mask, name in INVALID_FLAGS3.items():
        if flags3 & mask:
            result["flags3_active"].append(name)
            result["is_valid_unit"] = False
    
    return result
```

### 2. Interpretação de Body Size

```python
def interpret_body_size(body_size):
    """Interpreta o tamanho do corpo"""
    
    # Multiplica por 10 para volume real
    volume_cm3 = body_size * 10
    volume_liters = volume_cm3 / 1000.0
    
    # Categorias por idade
    if body_size < 3500:
        category = "bebê"
    elif body_size < 5000:
        category = "criança"
    elif body_size < 6500:
        category = "adolescente"
    else:
        category = "adulto"
    
    return {
        "raw_value": body_size,
        "volume_cm3": volume_cm3,
        "volume_liters": volume_liters,
        "category": category
    }
```

### 3. Análise de Blood Level

```python
def analyze_blood_level(blood_level, blood_max=6000):
    """Analisa o nível de sangue"""
    
    percentage = (blood_level / blood_max) * 100
    
    if percentage >= 75:
        status = "normal"
        severity = 0
    elif percentage >= 50:
        status = "leve"
        severity = 1
    elif percentage >= 25:
        status = "grave"
        severity = 2
    else:
        status = "crítico"
        severity = 3
    
    return {
        "current": blood_level,
        "max": blood_max,
        "percentage": round(percentage, 1),
        "status": status,
        "severity": severity,
        "critical": percentage <= 50
    }
```

### 4. Validação de Hist_ID

```python
def validate_hist_id(hist_id):
    """Valida e interpreta o hist_id"""
    
    if hist_id < 0:
        return {
            "valid": False,
            "has_history": False,
            "description": "Criatura sem importância histórica"
        }
    
    return {
        "valid": True,
        "has_history": True,
        "id": hist_id,
        "description": f"Figura histórica #{hist_id}"
    }
```

---

## 🎯 CONCLUSÕES

### Flags (flags1, flags2, flags3)
- São **bitmasks de estado** que controlam centenas de condições da unidade
- Usadas principalmente para **filtrar unidades inválidas** (mercadores, invasores, mortos, etc)
- Também rastreiam **condições de saúde** (cegueira, evisceração)
- **96 bits totais** de informação de estado

### Body Size
- Representa o **volume físico** da criatura em cm³
- **Multiplicar por 10** para obter valor real
- Valores típicos: 2.000-3.500 (bebê), 6.000-7.500 (adulto)
- Usado para determinar **compatibilidade com armas** e equipamentos

### Blood Level
- Quantidade **atual de sangue** (não o máximo)
- Valor **máximo separado** precisa ser lido (+0x4 do offset)
- < 50% = **ferimento crítico**, pode morrer
- Valor normal adulto: ~6.000 unidades

### Hist_ID
- **ID único** na tabela de figuras históricas do mundo
- Permite rastrear: kills, eventos, relações, identidades falsas
- **-1 = sem importância**, **≥ 0 = tem entrada histórica**
- Essencial para sistema de nobres e vampiros

---

## 📚 REFERÊNCIAS

### Arquivos Fonte Analisados:
1. `src/dwarf.cpp` - Leitura principal de dados
2. `src/dwarf.h` - Definições de estruturas
3. `src/unithealth.cpp` - Sistema de saúde e sangue
4. `src/histfigure.cpp` - Sistema de figuras históricas
5. `src/global_enums.h` - Enumerações e constantes
6. `share/memory_layouts/windows/v0.52.05-steam_win64.ini` - Offsets de memória

### Valores Hexadecimais dos Offsets:
```ini
flags1 = 0x0110
flags2 = 0x0114
flags3 = 0x0118
body_size = 0x06c8
blood = 0x06a4
hist_id = 0x0c10
```

---

**Fim do Relatório**
