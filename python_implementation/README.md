# Dwarf Therapist - Python Implementation

Uma implementação completa em Python para leitura direta da memória do Dwarf Fortress, fornecendo acesso aos dados dos anões sem modificar o jogo.

## 📁 Estrutura do Projeto

```
python_implementation/
├── src/                    # Código fonte principal
│   ├── complete_dwarf_reader.py      # Implementação completa e otimizada
│   ├── dwarf_therapist_verbose.py    # Versão com logging detalhado
│   └── dwarf_therapist_python.py     # Versão inicial básica
├── analysis/               # Scripts de análise de dados
│   ├── analyze_json.py               # Análise estatística dos dados
│   ├── analyze_insights.py           # Geração de insights
│   ├── analyze_memory_data.py        # Análise dos layouts de memória
│   └── complete_memory_analysis.py   # Análise completa dos layouts
├── tools/                  # Ferramentas utilitárias
│   ├── decode_professions.py         # Decodificação de profissões
│   └── decode_skills.py              # Decodificação de habilidades
├── data/                   # Arquivos de dados
│   ├── complete_dwarves_data.json    # Dataset completo (243 anões)
│   └── complete_memory_layout_analysis.json  # Análise dos layouts
├── docs/                   # Documentação
│   ├── ANALISE_COMPLETA.md           # Relatório técnico completo
│   └── README_PROJETO.md             # Documentação do projeto
└── logs/                   # Arquivos de log
```

## 🚀 Início Rápido

### Pré-requisitos

- Python 3.12+
- Dwarf Fortress rodando no Windows
- Ambiente virtual Python (recomendado)

### Instalação

```powershell
# Criar ambiente virtual
python -m venv venv
venv\Scripts\activate

# Instalar dependências
pip install psutil
```

### Uso Básico

```powershell
# Executar o leitor completo
python src\complete_dwarf_reader.py

# Analisar dados extraídos
python analysis\analyze_json.py

# Decodificar habilidades
python tools\decode_skills.py
```

## 📊 Recursos Implementados

### ✅ Leitura de Memória
- Conexão direta com processo do Dwarf Fortress
- Leitura de layouts de memória (77 versões suportadas)
- Extração de dados de anões em tempo real

### ✅ Dados Extraídos
- **Informações Básicas**: Nome, idade, sexo, raça
- **Atributos**: Força, agilidade, resistência, etc.
- **Habilidades**: 199+ habilidades diferentes
- **Profissões**: Militares, civis, administrativas
- **Status**: Humor, necessidades, relacionamentos
- **Equipamentos**: Armas, armaduras, itens

### ✅ Análise de Dados
- Estatísticas demográficas completas
- Análise de habilidades e profissões
- Identificação de padrões sociais
- Geração de relatórios técnicos

## 📈 Estatísticas do Dataset

- **243 anões** extraídos com sucesso
- **14.355 pontos de dados** totais
- **35 categorias** de informação por anão
- **2.277KB** de dados estruturados em JSON

### Top Habilidades Descobertas
1. **Teaching** (199 anões) - Ensino
2. **Speaking** (199 anões) - Oratória  
3. **Flattery** (199 anões) - Bajulação
4. **Leadership** (194 anões) - Liderança

## 🔧 Arquivos Principais

### `src/complete_dwarf_reader.py`
Implementação completa otimizada que:
- Conecta com Dwarf Fortress automaticamente
- Lê todos os dados disponíveis dos anões
- Exporta para JSON estruturado
- Inclui tratamento robusto de erros

### `analysis/analyze_json.py` 
Script de análise que gera:
- Estatísticas demográficas
- Distribuição de habilidades
- Análise de profissões
- Insights sobre a sociedade dos anões

### `tools/decode_*.py`
Ferramentas de decodificação que:
- Convertem IDs numéricos em nomes legíveis
- Mapeiam habilidades e profissões
- Revelam estruturas de dados ocultas

## 📋 Próximos Passos

- [ ] Interface gráfica (GUI) em PyQt5
- [ ] Sistema de filtros avançados
- [ ] Exportação para outros formatos
- [ ] Integração com API REST
- [ ] Monitoramento em tempo real

## 🎯 Descobertas Importantes

A análise revelou que a sociedade dos anões é:
- **Altamente Social**: Top habilidades são sociais, não militares
- **Bem Educada**: 199/243 anões têm habilidade de ensino
- **Diplomaticamente Sofisticada**: Alta prevalência de oratória e bajulação
- **Militarmente Organizada**: Sistema de profissões bem definido

## 📄 Licença

Este projeto segue a mesma licença do Dwarf Therapist original.

## 🤝 Contribuição

Contribuições são bem-vindas! Por favor:
1. Fork o repositório
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Abra um Pull Request

---

**Nota**: Esta implementação foi desenvolvida para fins educacionais e de pesquisa. Use responsavelmente!