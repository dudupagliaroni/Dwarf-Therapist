# Dwarf Therapist Python Edition

Uma implementação em Python que lê diretamente a memória do Dwarf Fortress, baseada no código original do Dwarf Therapist.

## Recursos

### Versão Básica (`dwarf_therapist_python.py`)
- Conecta automaticamente ao processo do Dwarf Fortress
- Lê informações básicas dos anões (nome, idade, profissão, humor)
- Carrega layouts de memória automaticamente
- Suporte para Windows 64-bit

### Versão Avançada (`advanced_dwarf_therapist.py`)
- Todas as funcionalidades da versão básica
- Leitura de habilidades (skills)
- Leitura de atributos físicos e mentais
- Gerenciamento de trabalhos (labors)
- Dados de felicidade e stress
- Funcionalidade para ativar/desativar trabalhos

## Requisitos

- Python 3.7+
- Windows (testado no Windows 10/11)
- Dwarf Fortress em execução
- Privilégios para acessar memória de processo

## Instalação

1. Clone o repositório ou baixe os arquivos
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

### Versão Básica
```bash
python dwarf_therapist_python.py
```

### Versão Avançada
```bash
python advanced_dwarf_therapist.py
```

## Como Funciona

O sistema funciona da seguinte forma:

1. **Detecção do Processo**: Localiza o processo "Dwarf Fortress.exe" em execução
2. **Abertura da Memória**: Abre um handle para ler/escrever na memória do processo
3. **Leitura do PE Header**: Determina a arquitetura e endereço base do executável
4. **Carregamento do Layout**: Carrega o arquivo de layout de memória apropriado
5. **Leitura de Dados**: Lê estruturas de dados diretamente da memória

### Layouts de Memória

Os layouts de memória são arquivos INI que mapeiam as estruturas internas do DF:
- Localizados em `share/memory_layouts/windows/`
- Contêm offsets para diferentes versões do DF
- Incluem endereços globais e offsets de estruturas

Exemplo de layout:
```ini
[addresses]
creature_vector=0x141e6f020
current_year=0x14188a2ac

[dwarf_offsets]
name=0x0008
profession=0x00a0
age=0x0374
```

## Estrutura do Código

### Classes Principais

- **`MemoryReader`**: Funcionalidades de baixo nível para leitura de memória
- **`MemoryLayout`**: Parser e acesso aos layouts de memória
- **`DFInstance`**: Interface principal para interação com o DF
- **`DwarfData`**: Estrutura de dados representando um anão
- **`AdvancedDwarfData`**: Extensão com skills, atributos e labors

### Padrões de Acesso à Memória

```python
# Leitura de inteiro 32-bit
value = memory_reader.read_int32(address)

# Leitura de ponteiro
pointer = memory_reader.read_pointer(address, pointer_size)

# Leitura de string do DF (std::string)
text = memory_reader.read_df_string(address, pointer_size)

# Leitura de vetor
start_ptr = memory_reader.read_pointer(vector_addr, pointer_size)
end_ptr = memory_reader.read_pointer(vector_addr + pointer_size, pointer_size)
count = (end_ptr - start_ptr) // pointer_size
```

## Limitações Atuais

1. **Apenas Windows**: Atualmente só funciona no Windows
2. **Layouts Fixos**: Usa layouts pré-definidos, não detecta automaticamente a versão
3. **Funcionalidade Limitada**: Nem todas as funcionalidades do DT original estão implementadas
4. **Sem Interface Gráfica**: Apenas interface de linha de comando

## Desenvolvimento Futuro

### Funcionalidades Planejadas
- [ ] Detecção automática da versão do DF
- [ ] Suporte para Linux e macOS
- [ ] Interface gráfica usando tkinter ou PyQt
- [ ] Exportação de dados para CSV/JSON
- [ ] Sistema de backup antes de modificações
- [ ] Leitura de mais dados (equipamentos, relacionamentos, etc.)

### Melhorias de Código
- [ ] Tratamento de erros mais robusto
- [ ] Cache de dados lidos
- [ ] Logging mais detalhado
- [ ] Testes unitários
- [ ] Documentação de API

## Segurança

⚠️ **Aviso**: Este código acessa diretamente a memória do processo do Dwarf Fortress. Use por sua conta e risco:

- Sempre faça backup dos seus saves antes de usar
- Modificações incorretas podem corromper o jogo
- Teste em saves descartáveis primeiro
- Feche o script se o jogo começar a se comportar estranhamente

## Comparação com o DT Original

| Funcionalidade | DT Original | Python Edition |
|----------------|-------------|----------------|
| Leitura de Anões | ✅ | ✅ |
| Interface Gráfica | ✅ | ❌ |
| Edição de Labors | ✅ | ✅ (básico) |
| Profissões Customizadas | ✅ | ❌ |
| Grid Views | ✅ | ❌ |
| Multi-plataforma | ✅ | ❌ (só Windows) |
| Detecção Auto de Versão | ✅ | ❌ |

## Contribuindo

Contribuições são bem-vindas! Áreas que precisam de ajuda:

1. Suporte para Linux/macOS
2. Interface gráfica
3. Detecção automática de versões
4. Mais funcionalidades de leitura de dados
5. Testes e documentação

## Licença

Este projeto é baseado no Dwarf Therapist original e mantém a mesma licença MIT.

## Suporte

Para problemas e dúvidas:
1. Verifique se o Dwarf Fortress está em execução
2. Certifique-se de ter privilégios de administrador
3. Teste com diferentes versões de layout se necessário
4. Consulte os logs de erro para debugging