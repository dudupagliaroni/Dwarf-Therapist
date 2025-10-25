# Data Directory

Esta pasta contém os dados extraídos e analisados do Dwarf Fortress.

## Estrutura

```
data/
├── README.md                                    # Este arquivo
├── complete_dwarves_data.json                   # Dataset principal (IGNORADO)
├── complete_memory_layout_analysis.json         # Análise layouts (IGNORADO)
└── dwarves_data.json                           # Dataset anterior (IGNORADO)
```

## Arquivos Principais

### `complete_dwarves_data.json`
- **Tamanho**: ~2.3MB (104.192 linhas)
- **Conteúdo**: 243 anões com dados completos
- **Estrutura**: JSON com metadata + array de dwarves
- **Pontos de dados**: 8.280 pontos únicos
- **Categorias**: habilidades, atributos, equipamentos, ferimentos

### `complete_memory_layout_analysis.json`
- **Tamanho**: ~195KB
- **Conteúdo**: Análise completa dos layouts de memória
- **Cobertura**: 77 versões diferentes do Dwarf Fortress
- **Plataformas**: Windows, Linux, macOS

## Git Ignore

Os arquivos JSON são ignorados pelo git devido ao tamanho e natureza sensível (dados de processo).

Para gerar os dados:
```bash
python ../src/complete_dwarf_reader.py
```

Para analisar os dados:
```bash
python ../analysis/analyze_json_simple.py
```

## Formatos Suportados

- **JSON**: Formato principal para intercâmbio
- **CSV**: Exportação disponível via scripts de análise
- **Pickle**: Cache para análises complexas (não commitado)

## Segurança

⚠️ **Importante**: Estes arquivos contêm dados extraídos da memória do processo Dwarf Fortress. Não devem ser compartilhados publicamente por questões de privacidade e segurança.